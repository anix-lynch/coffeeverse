# Coffeeverse Architecture

## System Overview

Azure-native ETL pipeline demonstrating enterprise data engineering patterns with serverless compute, NoSQL storage, and orchestrated transformations.

```
┌─────────────────────────────────────────────────────────────────┐
│                         Data Sources                             │
│                    (TheCocktailDB API)                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Azure Blob Storage                            │
│                    (Bronze Layer - Raw)                          │
└────────────────────────┬────────────────────────────────────────┘
                         │ Blob Trigger
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Azure Functions                                │
│              (ETL Pipeline Workers)                              │
│   • Validate schema                                              │
│   • Transform data                                               │
│   • Enrich metadata                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Azure Cosmos DB                                │
│                  (Silver Layer - Cleaned)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        dbt Core                                  │
│                  (Gold Layer - Analytics)                        │
│   • Staging models                                               │
│   • Mart models                                                  │
│   • Business logic                                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Streamlit Dashboard                            │
│                  (Visualization Layer)                           │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Data Ingestion (Bronze)
- **Source**: TheCocktailDB REST API
- **Storage**: Azure Blob Storage (`raw/` container)
- **Format**: NDJSON (newline-delimited JSON)

### 2. ETL Pipeline (Bronze → Silver)
- **Compute**: Azure Functions (Python 3.11)
- **Trigger**: Blob storage events
- **Operations**:
  - Schema validation
  - Data cleaning
  - Metadata enrichment (timestamps, complexity scores)
- **Output**: Azure Cosmos DB

### 3. Transformation (Silver → Gold)
- **Tool**: dbt Core
- **Models**:
  - `stg_cocktails`: Staging layer with basic transformations
  - `mart_cocktail_analytics`: Business metrics and aggregations
- **Orchestration**: Azure Data Factory

### 4. Visualization
- **Framework**: Streamlit
- **Features**:
  - Real-time metrics
  - Interactive charts (Plotly)
  - Cost monitoring
- **Deployment**: Streamlit Cloud

## Infrastructure

### Azure Resources
- **Blob Storage**: 5GB free tier
- **Cosmos DB**: 1000 RU/s + 25GB free tier
- **Functions**: 1M executions/month free tier
- **Data Factory**: Free tier

### Infrastructure as Code
- **Tool**: Bicep
- **Location**: `infrastructure/bicep/main.bicep`
- **Deployment**: Azure CLI

## Data Flow

1. **Extract**: API → Blob Storage (raw JSON)
2. **Transform**: Azure Functions validate & clean
3. **Load**: Write to Cosmos DB (operational store)
4. **Model**: dbt transforms into analytics tables
5. **Serve**: Streamlit reads from Cosmos DB

## Cost Model

**Total: $0/month** (Free tier compliant)

- Storage: < 1GB used (5GB free)
- Cosmos DB: < 1000 RU/s (free tier)
- Functions: < 100K executions/month (1M free)
- Streamlit Cloud: Community tier

## Security

- Secrets managed via Azure Key Vault
- Connection strings in environment variables
- `.gitignore` blocks all credential files
- Cosmos DB uses managed identity

## Scalability

- **Functions**: Auto-scale to 200 instances
- **Cosmos DB**: Can scale to 1M+ RU/s
- **Blob Storage**: Unlimited capacity
- **dbt**: Runs on-demand or scheduled

## Monitoring

- Azure Monitor for Functions
- Cosmos DB metrics dashboard
- Streamlit app health check endpoint
- Deployment logs in Azure Portal
