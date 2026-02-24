# ☕ Coffeeverse: Azure Cloud ETL Pipeline

![Coffeeverse Demo](https://raw.githubusercontent.com/anix-lynch/www.gozeroshot.dev/main/public/coffeeverse.gif)

## 🚀 Live Demo
**[Try it now →](https://coffeeverse-jhmtq3zhd49jjr5aixnfgl.streamlit.app/)**

## 📊 Overview
Azure-native ETL pipeline demonstrating enterprise Microsoft stack with Blob Storage, Azure Functions, Cosmos DB, orchestrated by Azure Data Factory + dbt. Production-grade serverless architecture running on Azure Free Tier.

### Data Layers
- **Bronze**: Raw ingestion (Blob Storage) - unmodified API data
- **Silver**: Cleaned entities (Cosmos DB + dbt staging) - validated and enriched
- **Gold**: Analytics-ready tables (dbt marts) - business metrics and aggregations

### ✨ Key Features
- **Azure-Native Stack**: Blob Storage, Functions, Cosmos DB, Data Factory
- **Serverless Transformation**: Event-driven data processing
- **Docker Deployment**: Containerized dashboard
- **Infrastructure as Code**: Bicep templates
- **Real Cosmos DB**: Live NoSQL database integration
- **$0/month**: Runs entirely on Azure Free Tier

### 🛠️ Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat&logo=microsoftazure&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Cosmos DB](https://img.shields.io/badge/Cosmos_DB-0078D4?style=flat&logo=microsoftazure&logoColor=white)

- **Storage**: Azure Blob Storage
- **Compute**: Azure Functions
- **Database**: Azure Cosmos DB
- **Orchestration**: Azure Data Factory + dbt
- **Visualization**: Streamlit
- **IaC**: Bicep
- **Deployment**: Docker

## 📁 Project Structure
```
coffeeverse/
├── src/
│   ├── app/             # Streamlit dashboard (serving layer)
│   ├── pipelines/       # Azure Functions (ETL workers)
│   └── common/          # Shared utilities & schemas
├── infrastructure/
│   ├── bicep/           # IaC templates
│   ├── data_factory/    # ADF orchestration
│   └── scripts/         # Deployment scripts
├── dbt/                 # Data transformations (Silver/Gold)
├── data/
│   ├── bronze/          # Raw sample data
│   ├── silver/          # Cleaned sample data
│   ├── gold/            # Analytics sample data
│   └── schemas/         # Data contracts (JSON Schema)
├── docker/              # Container configs
├── docs/                # Architecture & runbooks
├── tests/               # Unit & integration tests
├── Makefile             # One-liner commands
└── README.md
```

## 🚀 Quick Start

```bash
# Setup environment
make setup

# Run locally
make run-app

# Deploy to Azure
make deploy-infra
make deploy-functions

# Run tests
make test
```

See [docs/RUNBOOK.md](docs/RUNBOOK.md) for detailed instructions.

## 🎯 Use Cases
- Learn Azure cloud data engineering
- Build enterprise ETL pipelines
- Master Azure serverless architecture
- Deploy production analytics dashboards

## 👨‍💻 Author
**Anix Lynch** - Data Scientist & ML Engineer

[![Portfolio](https://img.shields.io/badge/Portfolio-gozeroshot.dev-blue)](https://gozeroshot.dev)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-anixlynch-0077B5?logo=linkedin)](https://linkedin.com/in/anixlynch)
[![GitHub](https://img.shields.io/badge/GitHub-anix--lynch-181717?logo=github)](https://github.com/anix-lynch)

---

⭐ **Star this repo** if you find it useful!