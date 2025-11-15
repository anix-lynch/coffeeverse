# 🚀 Manual Azure Deployment Guide

Since the automated script has sandbox issues, here's how to manually create your Azure resources and get the secrets for Streamlit Cloud:

## Option 1: Azure Portal (Easiest)

1. **Go to Azure Portal**: https://portal.azure.com
2. **Create Resource Group**:
   - Name: `coffeeverse-rg-dev`
   - Region: `East US`
3. **Create Storage Account**:
   - Name: `coffeeversestorage[random]`
   - Resource Group: `coffeeverse-rg-dev`
   - Account kind: `StorageV2`
   - Performance: `Standard`
   - Replication: `LRS`
4. **Create Cosmos DB Account**:
   - Name: `coffeeverse-cosmos-[random]`
   - API: `Core (SQL)`
   - Resource Group: `coffeeverse-rg-dev`
   - Location: `East US`
   - **Enable Free Tier** ✅
5. **Create Cosmos DB Database**:
   - Database name: `coffeeverse-db`

## Option 2: Using Azure CLI (In Your Terminal)

```bash
# Set your subscription
az account set --subscription "240061ae-eb56-4e65-a6dc-11d4114b7267"

# Create resource group
az group create --name coffeeverse-rg-dev --location eastus

# Create storage account
az storage account create \
  --name coffeeversestorage[random8digits] \
  --resource-group coffeeverse-rg-dev \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2

# Get storage key
az storage account keys list \
  --account-name coffeeversestorage[random] \
  --resource-group coffeeverse-rg-dev \
  --query "[0].value" -o tsv

# Create Cosmos DB
az cosmosdb create \
  --name coffeeverse-cosmos-[random] \
  --resource-group coffeeverse-rg-dev \
  --kind GlobalDocumentDB \
  --enable-free-tier

# Get Cosmos credentials
az cosmosdb show \
  --name coffeeverse-cosmos-[random] \
  --resource-group coffeeverse-rg-dev \
  --query "documentEndpoint" -o tsv

az cosmosdb keys list \
  --name coffeeverse-cosmos-[random] \
  --resource-group coffeeverse-rg-dev \
  --query "primaryMasterKey" -o tsv
```

## 🎯 Extract These Secrets

Once your resources are created, find:

1. **AZURE_STORAGE_ACCOUNT**: Storage account name (e.g., `coffeeversestorage1234`)
2. **AZURE_STORAGE_KEY**: Access key (copy from Storage Account → Access keys)
3. **AZURE_COSMOS_URL**: Document endpoint (copy from Cosmos DB → Keys)
4. **AZURE_COSMOS_KEY**: Primary key (copy from Cosmos DB → Keys)

## 📋 Add to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Deploy from: `anix-lynch/coffeeverse`
3. Go to App Settings → Secrets
4. Add:
```toml
AZURE_STORAGE_ACCOUNT = "your_value"
AZURE_STORAGE_KEY = "your_value"
AZURE_COSMOS_URL = "your_value"
AZURE_COSMOS_KEY = "your_value"
```

5. Click "Save"
6. Your dashboard goes live! 🎉

## 💰 Cost Check
- **Storage**: $0 (Free Tier)
- **Cosmos DB**: $0 (Free Tier)
- **Total**: $0/month

---

**Status**: Ready for manual deployment
**Time**: ~5-10 minutes to create resources + 5 minutes to deploy to Streamlit
