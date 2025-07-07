# Contributing to n8n Workflows

Thank you for your interest in contributing to the n8n Workflows collection! This guide will help you contribute effectively.

## How to Contribute

### 1. Adding New Workflows

#### Business Automation Workflows
Place workflows in `workflows/business-automation/{category}/`:
- Use descriptive filenames (e.g., `customer-onboarding-automation.json`)
- Include comprehensive metadata
- Test workflows before submission

#### Platform-Specific Workflows  
Place workflows in `workflows/platform-specific/{platform}/`:
- Focus on specific platform integrations
- Include setup instructions in metadata
- Document required credentials

#### Community Workflows
Place general workflows in `workflows/community-collection/{category}/`:
- Use meaningful categorization
- Include complexity assessment
- Add integration information

### 2. Workflow Format

Each workflow should include enhanced metadata:
```json
{
  "id": "unique-workflow-id",
  "name": "Descriptive Workflow Name",
  "nodes": [ /* n8n nodes */ ],
  "connections": { /* n8n connections */ },
  "_metadata": {
    "id": "unique-workflow-id",
    "name": "Descriptive Workflow Name",
    "description": "Detailed description of what this workflow does",
    "source": "business-automation|platform-specific|community-collection",
    "category": {
      "business": "ai-ml|finance|healthcare|etc",
      "platform": "gmail|slack|discord|etc",
      "type": "automation|integration|analysis"
    },
    "metadata": {
      "complexity": "beginner|intermediate|advanced",
      "department": "IT|Marketing|Sales|HR|etc",
      "nodes_count": 12,
      "integrations": ["gmail", "openai", "slack"],
      "estimated_cost": "low|medium|high",
      "security_level": "public|internal|confidential"
    },
    "tags": ["email", "ai", "automation"],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-15T00:00:00Z",
    "version": "1.0.0"
  }
}
```

### 3. Quality Standards

#### Workflow Requirements
- ✅ Must be valid JSON
- ✅ Must include all required metadata
- ✅ Must have descriptive name and description
- ✅ Must specify correct complexity level
- ✅ Must list all integrations used
- ✅ Must be tested and functional

#### Naming Conventions
- Use descriptive, lowercase names with hyphens
- Include primary function and platform if applicable
- Examples:
  - `gmail-ai-email-labeling.json`
  - `slack-daily-standup-reminder.json`
  - `openai-content-generator.json`

### 4. Testing Your Contribution

Before submitting, run the validation scripts:

```bash
# Validate workflow format
python scripts/validate_workflow.py path/to/your/workflow.json

# Update database
python scripts/update_database.py

# Test documentation system
python run.py
```

### 5. Submission Process

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b add-new-workflow`
3. **Add your workflow** to the appropriate directory
4. **Run validation**: `python scripts/validate.py`
5. **Commit your changes**: `git commit -m "Add email automation workflow"`
6. **Push to your fork**: `git push origin add-new-workflow`
7. **Create a Pull Request**

### 6. Pull Request Guidelines

#### PR Title Format
- `Add: [Platform/Category] - Brief description`
- `Fix: [Issue] - Brief description`
- `Update: [Component] - Brief description`

#### PR Description Template
```markdown
## Description
Brief description of the workflow and its purpose.

## Type of Change
- [ ] New workflow
- [ ] Bug fix
- [ ] Documentation update
- [ ] Feature enhancement

## Category
- [ ] Business Automation
- [ ] Platform-Specific
- [ ] Community Collection

## Metadata
- **Complexity**: Beginner/Intermediate/Advanced
- **Department**: IT/Marketing/Sales/HR/etc
- **Integrations**: List of services used
- **Node Count**: Number of nodes

## Testing
- [ ] Workflow validated with validation script
- [ ] Tested in n8n environment
- [ ] Documentation generated successfully
- [ ] No database errors

## Additional Notes
Any additional information about the workflow.
```

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- n8n (for testing workflows)

### Local Development
```bash
# Clone your fork
git clone https://github.com/yourusername/n8n-workflows.git
cd n8n-workflows

# Install dependencies
pip install -r requirements.txt

# Start development server
python run.py

# Run validation
python scripts/validate.py
```

## Code Style

### Python Code
- Follow PEP 8
- Use type hints
- Include docstrings
- Use meaningful variable names

### JSON Workflows
- Use 2-space indentation
- Include all required metadata
- Use consistent naming conventions
- Remove any sensitive information

## Review Process

1. **Automated Checks**: PR will be automatically validated
2. **Code Review**: Maintainers will review code quality
3. **Testing**: Workflows will be tested for functionality
4. **Documentation**: Metadata will be verified
5. **Approval**: PR will be merged after approval

## Getting Help

- **Issues**: Use GitHub Issues for bug reports
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the docs/ directory

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Documentation acknowledgments

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to the n8n Workflows collection! 🚀