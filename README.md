# 🚀 n8n Workflows - Comprehensive Collection

A professionally organized collection of **2,400+ n8n workflows** with advanced search, documentation, and enterprise-grade features. This repository combines business automation, platform-specific integrations, and community workflows in one searchable location.

## ⚡ Quick Start

### Lightning-Fast Documentation System
Experience 100x performance improvement with our advanced documentation system:

```bash
# Install dependencies
pip install -r requirements.txt

# Start the documentation server
python run.py

# Open in browser
http://localhost:8000
```

**Key Features:**
- ⚡ **Sub-100ms response times** with SQLite FTS5 search
- 🔍 **Advanced filtering** by business category, platform, complexity
- 📱 **Responsive design** - works on all devices
- 🌙 **Dark/light themes** with system preference detection
- 📊 **Live statistics** and analytics
- 🎯 **Enterprise categorization** by department and use case
- 🔐 **Security classification** for enterprise deployment
- 📄 **On-demand JSON viewing** and download
- 🔗 **API endpoints** for programmatic access

## 📂 Repository Structure

### 🏢 Business Automation (200 workflows)
Industry-specific workflows ready for enterprise deployment:
- **AI & Machine Learning** - LLM integrations, vector databases, embeddings
- **Finance & Accounting** - Automated reporting, compliance, analytics
- **Healthcare** - Patient management, compliance, data processing
- **DevOps** - CI/CD, monitoring, deployment automation
- **E-Commerce** - Order processing, inventory, customer service
- **HR & Recruitment** - Candidate screening, onboarding, performance tracking
- **And 14+ more industries**

### 🔗 Platform-Specific (150+ workflows)
Service-focused integrations with detailed use cases:
- **Gmail & Email** - Automated labeling, responses, analysis
- **Discord** - Bots, notifications, content management
- **Slack** - Team automation, reporting, integrations
- **WordPress** - Content automation, SEO, publishing
- **Database & Storage** - Supabase, PostgreSQL, MongoDB operations
- **OpenAI & LLMs** - AI-powered automation and analysis
- **And 20+ more platforms**

### 🌍 Community Collection (2,000+ workflows)
Comprehensive general-purpose workflows:
- **365 unique integrations** across popular platforms
- **29,445 total nodes** with professional categorization
- **Smart categorization** by trigger type and complexity
- **Advanced search** with full-text indexing

## 🎯 Enterprise Features

### Advanced Metadata
Every workflow includes:
- **Business Category**: Industry and use case classification
- **Platform Category**: Service and integration type
- **Complexity Level**: Beginner, intermediate, advanced
- **Department Tags**: Marketing, Sales, IT, HR, etc.
- **Security Level**: Public, internal, confidential
- **Cost Estimation**: Resource usage assessment
- **Integration Count**: Number of external services

### API Access
RESTful API for programmatic access:
- `GET /api/workflows` - List workflows with filtering
- `GET /api/workflows/{id}` - Get specific workflow
- `GET /api/search` - Advanced search with facets
- `GET /api/categories` - List all categories
- `GET /api/stats` - Repository statistics

### Search & Discovery
- **Full-text search** across all workflow content
- **Faceted filtering** by multiple criteria
- **Saved searches** and bookmarks
- **Recommendations** based on usage patterns
- **Analytics dashboard** with usage insights

## 📊 Statistics

| Metric | Count |
|--------|-------|
| **Total Workflows** | 2,400+ |
| **Business Categories** | 20+ |
| **Platform Categories** | 50+ |
| **Unique Integrations** | 500+ |
| **Total Nodes** | 30,000+ |
| **Industries Covered** | 25+ |

## 🚀 Quick Usage

### Find Workflows by Business Need
```bash
# Search for AI workflows in marketing
curl "http://localhost:8000/api/search?category=ai-ml&department=marketing"

# Get all finance automation workflows
curl "http://localhost:8000/api/workflows?business_category=finance"
```

### Browse by Platform
```bash
# All Gmail integrations
curl "http://localhost:8000/api/workflows?platform=gmail"

# Discord bot workflows
curl "http://localhost:8000/api/workflows?platform=discord"
```

### Filter by Complexity
```bash
# Beginner-friendly workflows
curl "http://localhost:8000/api/workflows?complexity=beginner"

# Advanced enterprise workflows
curl "http://localhost:8000/api/workflows?complexity=advanced&security_level=confidential"
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+ (for enhanced features)
- Git

### Local Development
```bash
# Clone the repository
git clone https://github.com/inslyai/n8n-workflows.git
cd n8n-workflows

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (optional)
npm install

# Initialize the database
python scripts/init_database.py

# Start the documentation server
python run.py
```

### Docker Deployment
```bash
# Build and run with Docker
docker build -t n8n-workflows .
docker run -p 8000:8000 n8n-workflows

# Or use Docker Compose
docker-compose up
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

### Adding New Workflows
1. Place JSON files in appropriate category directories
2. Run validation: `python scripts/validate.py`
3. Update metadata: `python scripts/update_metadata.py`
4. Submit a pull request

### Enhancing Documentation
- Documentation system code is in `tools/documentation-system/`
- API code is in `api/`
- Database schema is in `api/database/`

## 📚 Documentation

- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guide](docs/CONTRIBUTING.md)
- [Migration Guide](docs/MIGRATION.md)

## 🔧 Technical Details

### Performance
- **Database**: SQLite with FTS5 full-text search
- **Backend**: FastAPI with async support
- **Frontend**: Vanilla JavaScript with modern CSS
- **Search**: Sub-100ms response times
- **Memory**: <50MB RAM usage

### Security
- **Input validation** for all API endpoints
- **Rate limiting** to prevent abuse
- **CORS configuration** for web security
- **Security headers** following best practices

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This repository combines and enhances workflows from multiple sources:
- Community n8n workflows with advanced documentation system
- Industry-specific business automation templates
- Platform-specific integration examples
- Original creators and contributors

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/inslyai/n8n-workflows/issues)
- **Discussions**: [GitHub Discussions](https://github.com/inslyai/n8n-workflows/discussions)
- **Email**: [Your contact email]

---

⭐ **Star this repository** if you find it useful!

🔄 **Fork and contribute** to help grow the collection!

🚀 **Deploy in your organization** for enterprise automation!