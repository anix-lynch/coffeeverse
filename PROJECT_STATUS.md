# Coffeeverse Project Status

> **Created**: November 15, 2025
> **Status**: 🟡 In Progress (Phase 2 Started - 50% Complete)
> **Goal**: Azure-native ETL pipeline (Azure equivalent of Mocktailverse AWS)

---

## ✅ Completed (Phase 1)

### Documentation
- [x] `README.md` - Full project overview with Azure architecture
- [x] `AZURE_AUTH_SETUP.md` - Complete Azure Free Tier setup guide
- [x] `.gitignore` - Azure credentials protection
- [x] `PROJECT_STATUS.md` - This file

### Core Infrastructure
- [x] `azure_function/function_app.py` - Azure Functions serverless ETL transform
- [x] `requirements.txt` - Python dependencies for Azure SDK

### Project Structure
```
coffeeverse/
├── README.md ✅
├── AZURE_AUTH_SETUP.md ✅
├── PROJECT_STATUS.md ✅
├── .gitignore ✅
├── requirements.txt ✅
├── azure_function/
│   ├── function_app.py ✅
│   ├── host.json (created, needs content)
│   └── requirements.txt (created, needs content)
├── dbt_project/
│   ├── models/
│   │   ├── staging/ (created)
│   │   └── marts/ (created)
├── deploy/ (created)
├── data_factory/ (created)
├── cosmosdb_schema.json (created, needs content)
├── streamlit_app.py (created, needs content)
└── Dockerfile (created, needs content)
```

---

## 🚧 TODO (Phase 2) - For Tomorrow

### Priority 1: Core Files ✅ COMPLETED
- [x] `azure_function/host.json` - Azure Functions config
- [x] `azure_function/requirements.txt` - Function-specific dependencies
- [x] `cosmosdb_schema.json` - Cosmos DB container schema
- [x] `streamlit_app.py` - Monitoring dashboard (adapted from Mocktailverse)

### Priority 2: IaC & Deployment
- [ ] `deploy/main.bicep` - Bicep IaC template
- [ ] `deploy/main.json` - ARM template (alternative)
- [ ] `deploy/deploy.sh` - Deployment automation script
- [ ] `deploy/destroy.sh` - Teardown script

### Priority 3: dbt Transformations
- [ ] `dbt_project/dbt_project.yml` - dbt project config
- [ ] `dbt_project/profiles.yml` - Azure Synapse connection
- [ ] `dbt_project/models/staging/stg_cocktails.sql`
- [ ] `dbt_project/models/marts/mart_cocktail_analytics.sql`

### Priority 4: Data Factory
- [ ] `data_factory/pipeline.json` - ADF pipeline definition
- [ ] `data_factory/linked_services.json` - ADF connections

### Priority 5: Additional Docs
- [ ] `DEPLOYMENT.md` - Step-by-step deployment guide
- [ ] `COST_CONTROL.md` - Azure cost optimization strategies
- [ ] `load_sample_data.py` - Sample data loader

### Priority 6: Testing & Demo
- [ ] Sample data file (margarita_recipes.json or coffee_recipes.json)
- [ ] Test Azure deployment
- [ ] Deploy Streamlit dashboard to Streamlit Cloud
- [ ] Create demo.gif
- [ ] Add to gozeroshot.dev portfolio

---

## 🎯 Azure Stack (Implemented)

| Component | Azure Service | Status | AWS Equivalent |
|-----------|---------------|--------|----------------|
| **Extract** | Blob Storage | 🟡 Planned | S3 |
| **Transform** | Azure Functions | ✅ Code Complete | Lambda |
| **Load** | Cosmos DB | 🟡 Schema Needed | DynamoDB |
| **Orchestrate** | Data Factory | 🟡 Planned | Glue/Airflow |
| **Model** | dbt + Synapse | 🟡 Planned | dbt + Athena |
| **Monitor** | Streamlit | 🟡 Planned | Streamlit |

---

## 💡 Key Decisions Made

1. **API**: Using TheCocktailDB (same as Mocktailverse) since no free Coffee API found
2. **Storage**: Azure Blob Storage (equivalent to S3)
3. **Compute**: Azure Functions (equivalent to AWS Lambda)
4. **Database**: Cosmos DB (equivalent to DynamoDB)
5. **Cost**: Target $0/month using Azure Free Tier

---

## 📝 Notes for Tomorrow

### Azure Function (function_app.py) Features:
- ✅ Blob trigger for automatic processing
- ✅ Cosmos DB integration
- ✅ Data validation & enrichment
- ✅ NDJSON format support
- ✅ Health check endpoint
- ✅ Manual trigger endpoint for testing

### What to Reference:
- Mocktailverse project structure at: `../mocktailverse/`
- AWS deployment patterns: `../mocktailverse/AWS_DEPLOYMENT_SUCCESS.md`
- Use same data transformation logic, just swap AWS → Azure services

### Azure Free Tier Limits (Don't Exceed):
- Blob Storage: 5 GB + 20K reads + 10K writes/month
- Functions: 1M executions/month
- Cosmos DB: 1000 RU/s + 25 GB free forever
- Data Factory: 5 activities/month
- SQL Database: 100K vCore-sec + 32 GB/month

### Quick Start Commands for Tomorrow:
```bash
# 1. Navigate to project
cd /Users/anixlynch/dev/northstar/verses/coffeeverse

# 2. Check what's done
ls -la

# 3. Continue with Priority 1 files
# (Create host.json, cosmosdb_schema.json, streamlit_app.py)

# 4. Test locally (once Azure creds are set up)
source ~/.config/secrets/azure.env
func start  # Test Azure Function locally

# 5. Deploy when ready
./deploy/deploy.sh
```

---

## 🔗 Related Projects

- **Mocktailverse (AWS)**: `/Users/anixlynch/dev/northstar/verses/mocktailverse/`
  - GitHub: https://github.com/anix-lynch/mocktailverse
  - Live: https://mocktailverse.streamlit.app
  - Portfolio: https://gozeroshot.dev/portfolio (✅ deployed)

- **Coffeeverse (Azure)**: This project
  - GitHub: *(to be created tomorrow)*
  - Live: *(to be deployed)*
  - Portfolio: *(to be added)*

---

## 📊 Completion Estimate

- **Phase 1**: 20% complete ✅ (Documentation & Azure Function code)
- **Phase 2**: 50% complete 🟡 (Core schemas & dashboard - IN PROGRESS)
- **Phase 3**: Add IaC, dbt, Data Factory → 80% complete
- **Phase 4**: Test, deploy, add to portfolio → 100% complete

**Estimated Time**: 2-3 hours to complete remaining files + deployment

---

## 🎓 Learning Goals (Same as Mocktailverse)

- Azure serverless architecture (Functions, Cosmos DB)
- Infrastructure as Code (Bicep/ARM)
- Multi-cloud expertise (AWS ✅ | Azure 🚧 | GCP 📋)
- Cost-effective cloud design
- ETL/ELT best practices

---

**Last Updated**: November 16, 2025 11:45 PST
**Next Session**: Priority 2 - IaC templates, then dbt, then Data Factory
**Status**: Continue Phase 2 - 50% complete, making great progress! 🚀

