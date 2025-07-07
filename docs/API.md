# API Documentation

## Overview
The n8n Workflows API provides programmatic access to the workflow collection with advanced search and filtering capabilities.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API is open access. Enterprise authentication features are planned.

## Endpoints

### GET /api/workflows
List workflows with optional filtering.

**Query Parameters:**
- `limit` (int): Maximum number of results (default: 50, max: 500)
- `offset` (int): Number of results to skip (default: 0)
- `search` (string): Full-text search query
- `source` (string): Filter by source (community-collection, business-automation, platform-specific)
- `business_category` (string): Filter by business category
- `platform_category` (string): Filter by platform category
- `complexity` (string): Filter by complexity (beginner, intermediate, advanced)
- `department` (string): Filter by department
- `min_nodes` (int): Minimum number of nodes
- `max_nodes` (int): Maximum number of nodes

**Example:**
```bash
curl "http://localhost:8000/api/workflows?search=email&complexity=beginner&limit=10"
```

### GET /api/workflows/{id}
Get a specific workflow by ID.

**Example:**
```bash
curl "http://localhost:8000/api/workflows/abc123"
```

### GET /api/search
Advanced search with faceted results.

**Query Parameters:**
- `q` (string): Search query
- `facets` (string): Comma-separated list of facets to include

**Example:**
```bash
curl "http://localhost:8000/api/search?q=automation&facets=source,complexity,department"
```

### GET /api/categories
List all available categories and their counts.

**Example:**
```bash
curl "http://localhost:8000/api/categories"
```

### GET /api/stats
Get repository statistics.

**Example:**
```bash
curl "http://localhost:8000/api/stats"
```

## Response Format

### Workflow Object
```json
{
  "id": "workflow-id",
  "name": "Workflow Name",
  "description": "Workflow description",
  "source": "community-collection",
  "category": {
    "business": "ai-ml",
    "platform": "gmail",
    "type": "automation"
  },
  "metadata": {
    "complexity": "intermediate",
    "department": "IT",
    "nodes_count": 12,
    "integrations": ["gmail", "openai", "slack"],
    "estimated_cost": "medium",
    "security_level": "public"
  },
  "tags": ["email", "ai", "automation"],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T00:00:00Z",
  "version": "1.0.0"
}
```

### Search Response
```json
{
  "results": [
    {
      "workflow": { /* workflow object */ },
      "score": 0.95,
      "highlights": {
        "name": "Email <mark>automation</mark>",
        "description": "Automate email processing with <mark>AI</mark>"
      }
    }
  ],
  "facets": {
    "source": {
      "community-collection": 1500,
      "business-automation": 200,
      "platform-specific": 100
    },
    "complexity": {
      "beginner": 400,
      "intermediate": 800,
      "advanced": 600
    }
  },
  "total": 1800,
  "page": 1,
  "per_page": 50
}
```

## Error Responses

### 404 Not Found
```json
{
  "detail": "Workflow not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["query", "limit"],
      "msg": "ensure this value is less than or equal to 500",
      "type": "value_error.number.not_le",
      "ctx": {"limit_value": 500}
    }
  ]
}
```

## Rate Limiting
- 100 requests per minute per IP
- 1000 requests per hour per IP

## CORS
CORS is enabled for all origins in development mode.