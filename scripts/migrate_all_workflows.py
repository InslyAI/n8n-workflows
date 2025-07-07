#!/usr/bin/env python3
"""
Migration script to combine workflows from three source repositories:
1. n8n-workflows (community collection)
2. n8n-free-templates (business automation)
3. awesome-n8n-templates (platform-specific)
"""

import os
import json
import shutil
import sqlite3
from pathlib import Path
from typing import Dict, Any, List
import hashlib
import re
from datetime import datetime

class WorkflowMigrator:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.source_path = Path("/tmp/n8n-analysis")
        self.workflows_db = {}
        self.duplicates = []
        self.stats = {
            'total_processed': 0,
            'community_collection': 0,
            'business_automation': 0,
            'platform_specific': 0,
            'duplicates_found': 0,
            'errors': 0
        }
        
    def setup_directories(self):
        """Create directory structure"""
        directories = [
            "workflows/business-automation",
            "workflows/platform-specific", 
            "workflows/community-collection",
            "tools/documentation-system",
            "api/database",
            "api/static"
        ]
        
        for directory in directories:
            (self.base_path / directory).mkdir(parents=True, exist_ok=True)
            
    def get_workflow_hash(self, workflow_data: Dict) -> str:
        """Generate hash for workflow deduplication"""
        # Use name and key nodes for hashing
        content = f"{workflow_data.get('name', '')}"
        if 'nodes' in workflow_data:
            # Sort nodes by type and parameters for consistent hashing
            nodes_signature = []
            for node in workflow_data['nodes']:
                node_sig = f"{node.get('type', '')}{node.get('name', '')}"
                nodes_signature.append(node_sig)
            content += "".join(sorted(nodes_signature))
        
        return hashlib.md5(content.encode()).hexdigest()
    
    def extract_metadata(self, workflow_data: Dict, source: str, category: str = None) -> Dict:
        """Extract and enhance metadata from workflow"""
        metadata = {
            'id': workflow_data.get('id', ''),
            'name': workflow_data.get('name', 'Untitled Workflow'),
            'description': '',
            'source': source,
            'category': {
                'business': '',
                'platform': '',
                'type': 'automation'
            },
            'metadata': {
                'complexity': 'intermediate',
                'department': '',
                'nodes_count': len(workflow_data.get('nodes', [])),
                'integrations': [],
                'estimated_cost': 'medium',
                'security_level': 'public'
            },
            'tags': workflow_data.get('tags', []),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        
        # Extract integrations from nodes
        if 'nodes' in workflow_data:
            integrations = set()
            for node in workflow_data['nodes']:
                node_type = node.get('type', '')
                if node_type.startswith('n8n-nodes-base.'):
                    service = node_type.replace('n8n-nodes-base.', '')
                    integrations.add(service)
            metadata['metadata']['integrations'] = list(integrations)
        
        # Set complexity based on node count
        node_count = metadata['metadata']['nodes_count']
        if node_count <= 5:
            metadata['metadata']['complexity'] = 'beginner'
        elif node_count <= 15:
            metadata['metadata']['complexity'] = 'intermediate'
        else:
            metadata['metadata']['complexity'] = 'advanced'
            
        # Set category based on source and path
        if category:
            if source == 'n8n-free-templates':
                metadata['category']['business'] = category.lower().replace('_', '-')
            elif source == 'awesome-n8n-templates':
                metadata['category']['platform'] = category.lower().replace('_', '-')
                
        return metadata
    
    def migrate_community_collection(self):
        """Migrate workflows from n8n-workflows (community collection)"""
        print("🔄 Migrating community collection...")
        source_dir = self.source_path / "n8n-workflows" / "workflows"
        target_dir = self.base_path / "workflows" / "community-collection"
        
        if not source_dir.exists():
            print("❌ Community collection source not found")
            return
            
        # Copy all JSON files
        for json_file in source_dir.rglob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    workflow_data = json.load(f)
                
                # Generate hash for deduplication
                workflow_hash = self.get_workflow_hash(workflow_data)
                
                if workflow_hash in self.workflows_db:
                    self.duplicates.append(f"Community: {json_file.name}")
                    self.stats['duplicates_found'] += 1
                    continue
                    
                # Extract metadata
                relative_path = json_file.relative_to(source_dir)
                category = relative_path.parts[0] if len(relative_path.parts) > 1 else 'general'
                
                metadata = self.extract_metadata(workflow_data, 'community-collection', category)
                
                # Create target directory
                target_file_dir = target_dir / relative_path.parent
                target_file_dir.mkdir(parents=True, exist_ok=True)
                
                # Save workflow with enhanced metadata
                enhanced_workflow = {
                    **workflow_data,
                    '_metadata': metadata
                }
                
                target_file = target_file_dir / json_file.name
                with open(target_file, 'w', encoding='utf-8') as f:
                    json.dump(enhanced_workflow, f, indent=2, ensure_ascii=False)
                
                self.workflows_db[workflow_hash] = {
                    'path': str(target_file),
                    'metadata': metadata
                }
                
                self.stats['community_collection'] += 1
                self.stats['total_processed'] += 1
                
            except Exception as e:
                print(f"❌ Error processing {json_file}: {e}")
                self.stats['errors'] += 1
                
        print(f"✅ Community collection: {self.stats['community_collection']} workflows migrated")
    
    def migrate_business_automation(self):
        """Migrate workflows from n8n-free-templates (business automation)"""
        print("🔄 Migrating business automation...")
        source_dir = self.source_path / "n8n-free-templates"
        target_dir = self.base_path / "workflows" / "business-automation"
        
        if not source_dir.exists():
            print("❌ Business automation source not found")
            return
            
        # Process each category directory
        for category_dir in source_dir.iterdir():
            if category_dir.is_dir() and category_dir.name not in ['.git', '__pycache__']:
                category_name = category_dir.name
                target_category_dir = target_dir / category_name.lower().replace('_', '-')
                target_category_dir.mkdir(parents=True, exist_ok=True)
                
                # Process JSON files in category
                for json_file in category_dir.glob("*.json"):
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            workflow_data = json.load(f)
                        
                        # Generate hash for deduplication
                        workflow_hash = self.get_workflow_hash(workflow_data)
                        
                        if workflow_hash in self.workflows_db:
                            self.duplicates.append(f"Business: {json_file.name}")
                            self.stats['duplicates_found'] += 1
                            continue
                            
                        # Extract metadata
                        metadata = self.extract_metadata(workflow_data, 'business-automation', category_name)
                        
                        # Map category to department
                        department_mapping = {
                            'AI_ML': 'IT',
                            'Finance_Accounting': 'Finance',
                            'HR': 'HR',
                            'Healthcare': 'Healthcare',
                            'DevOps': 'IT',
                            'E_Commerce_Retail': 'Sales',
                            'Social_Media': 'Marketing',
                            'Email_Automation': 'Marketing',
                            'Education': 'Education',
                            'Legal_Tech': 'Legal'
                        }
                        metadata['metadata']['department'] = department_mapping.get(category_name, 'General')
                        
                        # Enhanced workflow
                        enhanced_workflow = {
                            **workflow_data,
                            '_metadata': metadata
                        }
                        
                        target_file = target_category_dir / json_file.name
                        with open(target_file, 'w', encoding='utf-8') as f:
                            json.dump(enhanced_workflow, f, indent=2, ensure_ascii=False)
                        
                        self.workflows_db[workflow_hash] = {
                            'path': str(target_file),
                            'metadata': metadata
                        }
                        
                        self.stats['business_automation'] += 1
                        self.stats['total_processed'] += 1
                        
                    except Exception as e:
                        print(f"❌ Error processing {json_file}: {e}")
                        self.stats['errors'] += 1
                        
        print(f"✅ Business automation: {self.stats['business_automation']} workflows migrated")
    
    def migrate_platform_specific(self):
        """Migrate workflows from awesome-n8n-templates (platform-specific)"""
        print("🔄 Migrating platform-specific workflows...")
        source_dir = self.source_path / "awesome-n8n-templates"
        target_dir = self.base_path / "workflows" / "platform-specific"
        
        if not source_dir.exists():
            print("❌ Platform-specific source not found")
            return
            
        # Process each platform directory
        for platform_dir in source_dir.iterdir():
            if platform_dir.is_dir() and platform_dir.name not in ['.git', '__pycache__', 'img']:
                platform_name = platform_dir.name
                target_platform_dir = target_dir / platform_name.lower().replace('_', '-')
                target_platform_dir.mkdir(parents=True, exist_ok=True)
                
                # Process .txt files containing JSON
                for txt_file in platform_dir.glob("*.txt"):
                    try:
                        with open(txt_file, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                        
                        # Try to parse as JSON
                        workflow_data = json.loads(content)
                        
                        # Generate hash for deduplication
                        workflow_hash = self.get_workflow_hash(workflow_data)
                        
                        if workflow_hash in self.workflows_db:
                            self.duplicates.append(f"Platform: {txt_file.name}")
                            self.stats['duplicates_found'] += 1
                            continue
                            
                        # Extract metadata
                        metadata = self.extract_metadata(workflow_data, 'platform-specific', platform_name)
                        
                        # Set department based on platform
                        department_mapping = {
                            'Gmail_and_Email_Automation': 'Marketing',
                            'Discord': 'IT',
                            'Slack': 'IT',
                            'WordPress': 'Marketing',
                            'OpenAI_and_LLMs': 'IT',
                            'Database_and_Storage': 'IT',
                            'HR_and_Recruitment': 'HR',
                            'Instagram_Twitter_Social_Media': 'Marketing'
                        }
                        metadata['metadata']['department'] = department_mapping.get(platform_name, 'General')
                        
                        # Enhanced workflow
                        enhanced_workflow = {
                            **workflow_data,
                            '_metadata': metadata
                        }
                        
                        # Save as JSON file
                        json_filename = txt_file.stem + '.json'
                        target_file = target_platform_dir / json_filename
                        
                        with open(target_file, 'w', encoding='utf-8') as f:
                            json.dump(enhanced_workflow, f, indent=2, ensure_ascii=False)
                        
                        self.workflows_db[workflow_hash] = {
                            'path': str(target_file),
                            'metadata': metadata
                        }
                        
                        self.stats['platform_specific'] += 1
                        self.stats['total_processed'] += 1
                        
                    except json.JSONDecodeError:
                        print(f"❌ Invalid JSON in {txt_file}")
                        self.stats['errors'] += 1
                    except Exception as e:
                        print(f"❌ Error processing {txt_file}: {e}")
                        self.stats['errors'] += 1
                        
        print(f"✅ Platform-specific: {self.stats['platform_specific']} workflows migrated")
    
    def copy_documentation_system(self):
        """Copy and enhance the documentation system from n8n-workflows"""
        print("🔄 Copying documentation system...")
        source_files = [
            "run.py",
            "api_server.py", 
            "workflow_db.py",
            "requirements.txt",
            "static",
            "src"
        ]
        
        source_dir = self.source_path / "n8n-workflows"
        
        for item in source_files:
            source_item = source_dir / item
            if source_item.exists():
                if source_item.is_file():
                    shutil.copy2(source_item, self.base_path / item)
                else:
                    shutil.copytree(source_item, self.base_path / item, dirs_exist_ok=True)
        
        print("✅ Documentation system copied")
    
    def generate_database(self):
        """Generate SQLite database with all workflows"""
        print("🔄 Generating database...")
        
        db_path = self.base_path / "api" / "database" / "workflows.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create enhanced table schema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflows (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                source TEXT,
                business_category TEXT,
                platform_category TEXT,
                workflow_type TEXT,
                complexity TEXT,
                department TEXT,
                nodes_count INTEGER,
                integrations TEXT,
                estimated_cost TEXT,
                security_level TEXT,
                tags TEXT,
                json_content TEXT,
                file_path TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                version TEXT
            )
        """)
        
        # Create FTS5 search index
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS workflows_fts USING fts5(
                name, description, tags, integrations, department,
                content='workflows'
            )
        """)
        
        # Insert all workflows
        for workflow_hash, workflow_info in self.workflows_db.items():
            metadata = workflow_info['metadata']
            
            # Read JSON content
            with open(workflow_info['path'], 'r', encoding='utf-8') as f:
                json_content = f.read()
            
            cursor.execute("""
                INSERT OR REPLACE INTO workflows VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """, (
                metadata['id'] or workflow_hash,
                metadata['name'],
                metadata['description'],
                metadata['source'],
                metadata['category']['business'],
                metadata['category']['platform'],
                metadata['category']['type'],
                metadata['metadata']['complexity'],
                metadata['metadata']['department'],
                metadata['metadata']['nodes_count'],
                json.dumps(metadata['metadata']['integrations']),
                metadata['metadata']['estimated_cost'],
                metadata['metadata']['security_level'],
                json.dumps(metadata['tags']),
                json_content,
                workflow_info['path'],
                metadata['created_at'],
                metadata['updated_at'],
                metadata['version']
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database generated with {len(self.workflows_db)} workflows")
    
    def print_summary(self):
        """Print migration summary"""
        print("\n" + "="*50)
        print("📊 MIGRATION SUMMARY")
        print("="*50)
        print(f"Total workflows processed: {self.stats['total_processed']}")
        print(f"Community collection: {self.stats['community_collection']}")
        print(f"Business automation: {self.stats['business_automation']}")
        print(f"Platform-specific: {self.stats['platform_specific']}")
        print(f"Duplicates found: {self.stats['duplicates_found']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Unique workflows: {len(self.workflows_db)}")
        
        if self.duplicates:
            print(f"\n📋 Duplicates found:")
            for dup in self.duplicates[:10]:  # Show first 10
                print(f"  - {dup}")
            if len(self.duplicates) > 10:
                print(f"  ... and {len(self.duplicates) - 10} more")
        
        print("\n🎉 Migration completed successfully!")
        print("Next steps:")
        print("1. Run: python run.py")
        print("2. Open: http://localhost:8000")
        print("3. Explore your unified workflow collection!")
    
    def run_migration(self):
        """Run the complete migration process"""
        print("🚀 Starting n8n workflows migration...")
        
        # Setup
        self.setup_directories()
        
        # Migrate from all sources
        self.migrate_community_collection()
        self.migrate_business_automation()
        self.migrate_platform_specific()
        
        # Copy documentation system
        self.copy_documentation_system()
        
        # Generate database
        self.generate_database()
        
        # Print summary
        self.print_summary()

if __name__ == "__main__":
    migrator = WorkflowMigrator("/tmp/n8n-workflows")
    migrator.run_migration()