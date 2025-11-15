# 🍵 Coffeeverse: Azure ETL Pipeline

An end-to-end Azure-native ETL/ELT pipeline demonstrating enterprise-grade data engineering practices with serverless technologies.

![Demo](demo.gif)

🔗 **Live Dashboard**: [coffeeverse.streamlit.app](https://coffeeverse.streamlit.app) *(Coming Soon)*

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Azure Blob    │    │ Azure Functions │    │  Cosmos DB      │
│   Storage       │───▶│   (Transform)   │───▶│   (Load)        │
│   (Extract)     │    │   Python ETL    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Azure Data      │    │ Azure Data      │    │     dbt-core    │
│ Factory         │    │ Factory         │    │   (Modeling)    │
│ (Orchestration) │    │ (Pipelines)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Azure CLI configured with appropriate permissions
- Docker (optional, for containerized deployment)
- Python 3.11+

### 1. Clone and Setup
```bash
git clone https://github.com/anix-lynch/coffeeverse
cd coffeeverse
pip install -r requirements.txt
```

### 2. Configure Azure Credentials
```bash
# Login to Azure
az login

# Set your subscription
az account set --subscription "Your-Subscription-ID"

# Create service principal for automation
az ad sp create-for-rbac --name "coffeeverse-sp" --role contributor \
  --scopes /subscriptions/{subscription-id}
```

### 3. Deploy Infrastructure
```bash
# Deploy ARM templates
./deploy/deploy.sh

# Or use Bicep
az deployment group create \
  --resource-group coffeeverse-rg \
  --template-file deploy/main.bicep
```

### 4. Run ETL Pipeline
```bash
# Trigger Azure Data Factory pipeline
az datafactory pipeline create-run \
  --resource-group coffeeverse-rg \
  --factory-name coffeeverse-adf \
  --name coffeeverse-etl-pipeline
```

## 📁 Project Structure

```
coffeeverse/
├── azure_function/              # Azure Functions (serverless)
│   ├── function_app.py
│   ├── host.json
│   └── requirements.txt
├── data_factory/                # Azure Data Factory pipelines
│   ├── pipeline.json
│   └── linked_services.json
├── dbt_project/                 # dbt data transformation project
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       ├── staging/
│       └── marts/
├── cosmosdb_schema.json         # Cosmos DB container schema
├── deploy/                      # Infrastructure as Code
│   ├── main.bicep               # Bicep template
│   ├── main.json                # ARM template
│   ├── deploy.sh                # Deployment script
│   └── destroy.sh               # Teardown script
├── streamlit_app.py             # Monitoring dashboard
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container configuration
└── README.md                    # This file
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Extract** | Azure Blob Storage | Raw data storage and ingestion |
| **Transform** | Azure Functions | Serverless data processing |
| **Load** | Azure Cosmos DB | NoSQL data storage |
| **Model** | dbt-core + Azure Synapse | Data modeling and analytics |
| **Orchestrate** | Azure Data Factory | Pipeline orchestration |

## 🎯 Key Features

### Enterprise ETL Capabilities
- **Serverless Architecture**: No servers to manage, automatic scaling
- **Azure-Native**: Full integration with Azure ecosystem
- **Data Quality**: Automated validation and monitoring
- **Incremental Processing**: Efficient handling of new data
- **Error Handling**: Robust retry mechanisms and monitoring

### Azure Free Tier Compliant
- **Azure Functions**: 1M executions/month free
- **Cosmos DB**: 1000 RU/s + 25GB storage free
- **Blob Storage**: 5GB + 20K reads + 10K writes/month free
- **Data Factory**: 5 activities/month free
- **SQL Database**: 100K vCore seconds + 32GB storage/month free

**Target Monthly Cost: $0** (within free tier limits)

## 💰 Cost Comparison

### Free Tier Limits
| Service | Free Tier | Est. Monthly Cost |
|---------|-----------|-------------------|
| Blob Storage | 5GB + 20K GET + 10K PUT | $0 |
| Functions | 1M executions | $0 |
| Cosmos DB | 1000 RU/s + 25GB | $0 |
| Data Factory | 5 activities | $0 |
| SQL Database | 32GB + 100K vCore-sec | $0 |
| **Total** | - | **$0/month** |

### Cost Optimization Strategies
1. Use serverless tiers (Azure Functions, Cosmos DB serverless)
2. Implement auto-pause for SQL Database
3. Use lifecycle management for Blob Storage
4. Set up cost alerts and budgets
5. Monitor RU consumption in Cosmos DB

## 📊 AI Model Selection

### Azure AI Services
- **Azure OpenAI Service**: GPT-4 for text generation
- **Azure Cognitive Search**: Vector search and indexing
- **Azure ML**: Custom model training and deployment

## 🗂️ Azure vs AWS vs GCP Comparison

### Service Equivalents

| AWS | GCP | **Azure** | Purpose |
|-----|-----|----------|---------|
| S3 | Cloud Storage | **Blob Storage** | Object storage |
| Lambda | Cloud Functions | **Azure Functions** | Serverless compute |
| DynamoDB | Firestore | **Cosmos DB** | NoSQL database |
| Glue | Dataflow | **Data Factory** | ETL orchestration |
| Athena | BigQuery | **Synapse Analytics** | Data warehouse |

## 📚 Documentation

- [Azure Free Account Setup](./docs/AZURE_SETUP.md)
- [Cost Control Best Practices](./docs/COST_CONTROL.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)
- [Architecture Deep Dive](./docs/ARCHITECTURE.md)
- [dbt Transformations](./dbt_project/README.md)

## 🛤️ Roadmap

- [x] Azure Blob Storage setup
- [x] Azure Functions implementation
- [x] Cosmos DB schema design
- [x] Data Factory pipeline
- [x] dbt transformations
- [ ] Azure Synapse integration
- [ ] Power BI dashboard
- [ ] CI/CD with Azure DevOps
- [ ] Terraform/Bicep IaC
- [ ] Cost monitoring automation

## 🎓 Learning Goals

This project demonstrates:
- Azure serverless architecture
- Infrastructure as Code (ARM/Bicep)
- Data engineering best practices
- Cost-effective cloud design
- Multi-cloud expertise (AWS/GCP/Azure)

## 🤝 Contributing

Feel free to open issues or submit PRs. For major changes, please open an issue first.

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

---

**Part of the "Verses" Portfolio**: [Mocktailverse (AWS)](../mocktailverse) | **Coffeeverse (Azure)** | [Smoothieverse (GCP)](../smoothieverse)

**Author**: Anix Lynch | [Portfolio](https://gozeroshot.dev) | [GitHub](https://github.com/anix-lynch)

