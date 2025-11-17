# 🐳 Coffeeverse Docker Image

**Container**: `anixlynch/coffeeverse:latest`

## Quick Start

```bash
docker pull anixlynch/coffeeverse:latest
docker run -p 8501:8501 anixlynch/coffeeverse:latest
```

Then visit: **http://localhost:8501**

## What's Included

✅ **Streamlit Dashboard** - Real-time ETL monitoring
✅ **Plotly Charts** - 4 interactive visualizations  
✅ **Mock Cocktail Data** - 50 samples pre-loaded
✅ **Azure Ready** - Add credentials to connect real data
✅ **Production Ready** - Optimized image, ~1.4GB

## Features

- **Spirit Distribution Chart** - Pie chart of cocktail types
- **Complexity Analysis** - Histogram distribution
- **Calories vs Complexity** - Scatter plot insights
- **Data Table** - Browse sample cocktails
- **Pipeline Status** - Monitor ETL health
- **Cost Breakdown** - Azure Free Tier pricing

## Environment Variables (Optional)

Connect to real Azure data by setting:

```bash
docker run -p 8501:8501 \
  -e AZURE_STORAGE_ACCOUNT=your_account \
  -e AZURE_STORAGE_KEY=your_key \
  -e AZURE_COSMOS_URL=your_url \
  -e AZURE_COSMOS_KEY=your_key \
  anixlynch/coffeeverse:latest
```

## Local Development

```bash
git clone https://github.com/anix-lynch/coffeeverse
cd coffeeverse
docker-compose up -d
```

## Technology Stack

- **Python 3.11** - Runtime
- **Streamlit** - Dashboard framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **Docker** - Containerization

## Links

- 📖 **GitHub**: https://github.com/anix-lynch/coffeeverse
- 🏗️ **Architecture**: Azure Blob Storage → Functions → Cosmos DB
- 💰 **Cost**: $0/month (Azure Free Tier)
- 🎯 **Purpose**: Demonstrate Azure ETL + Data Engineering skills

## Architecture

```
Azure Blob Storage (Extract)
    ↓
Azure Functions (Transform)  
    ↓
Cosmos DB (Load)
    ↓
Streamlit Dashboard (Visualize)
```

**Orchestration**: Azure Data Factory  
**Modeling**: dbt-core + Azure Synapse

## For Recruiters

This Docker image showcases:
- ✅ Containerization & DevOps skills
- ✅ Cloud architecture (Azure native)
- ✅ Data engineering best practices
- ✅ Python + data visualization
- ✅ ETL/ELT pipeline design
- ✅ Production-ready code

Just `docker run` and you'll see a working dashboard! 🚀

---

**Author**: Anix Lynch  
**Portfolio**: https://gozeroshot.dev  
**GitHub**: https://github.com/anix-lynch

