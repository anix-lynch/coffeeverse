# Azure Authentication & Free Tier Setup Guide

> **Project**: Coffeeverse Azure ETL Pipeline  
> **Goal**: $0/month deployment using Azure Free Tier  
> **Status**: Setup guide for first-time Azure users

---

## 🎯 Overview

This guide walks you through setting up Azure credentials and deploying Coffeeverse **100% within Azure Free Tier** limits.

---

## 🆓 Step 1: Create Azure Free Account

### Sign Up
1. Go to [https://azure.microsoft.com/free](https://azure.microsoft.com/free)
2. Click "Start free"
3. Sign in with Microsoft account (or create one)
4. Provide:
   - Credit card (for verification only, **won't be charged**)
   - Phone number for SMS verification
   - Basic profile information

### What You Get
- **$200 credit** for 30 days (any service)
- **55+ services** always free (limited usage)
- **25+ services** free for 12 months

### Free Tier Services for Coffeeverse
| Service | Free Tier | Coffeeverse Usage |
|---------|-----------|-------------------|
| Blob Storage | 5 GB + 20K reads + 10K writes/month | ✅ Raw data storage |
| Azure Functions | 1M executions/month | ✅ Serverless transform |
| Cosmos DB | 1000 RU/s + 25 GB free forever | ✅ NoSQL database |
| SQL Database | 100K vCore-sec + 32 GB/month | ✅ Optional warehouse |
| Data Factory | 5 activities/month | ✅ Pipeline orchestration |
| Container Instances | 1M vCore-sec + 1.5 GB RAM | ✅ Docker deployment |

**Total: $0/month** ✅

---

## 🔐 Step 2: Azure CLI Authentication

### Install Azure CLI

**macOS (Homebrew):**
```bash
brew update && brew install azure-cli
```

**Windows:**
```powershell
# Download from: https://aka.ms/installazurecliwindows
# Or use winget:
winget install -e --id Microsoft.AzureCLI
```

**Linux:**
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### Login to Azure
```bash
# Interactive browser login
az login

# You'll see output like:
# [
#   {
#     "cloudName": "AzureCloud",
#     "id": "12345678-1234-1234-1234-123456789012",
#     "isDefault": true,
#     "name": "Pay-As-You-Go",
#     "state": "Enabled",
#     "tenantId": "87654321-4321-4321-4321-210987654321",
#     "user": {
#       "name": "your-email@example.com",
#       "type": "user"
#     }
#   }
# ]
```

### Set Default Subscription
```bash
# List subscriptions
az account list --output table

# Set active subscription
az account set --subscription "Your-Subscription-Name"

# Verify
az account show
```

---

## 🗝️ Step 3: Create Service Principal (for automation)

### Why Service Principal?
- Automate deployments without interactive login
- Secure credentials for CI/CD
- Fine-grained permissions

### Create Service Principal
```bash
# Get your subscription ID
SUBSCRIPTION_ID=$(az account show --query id --output tsv)

# Create service principal
az ad sp create-for-rbac \
  --name "coffeeverse-sp" \
  --role contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID \
  --sdk-auth

# Output (SAVE THIS!):
# {
#   "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#   "clientSecret": "your-secret-here",
#   "subscriptionId": "12345678-1234-1234-1234-123456789012",
#   "tenantId": "87654321-4321-4321-4321-210987654321",
#   "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
#   "resourceManagerEndpointUrl": "https://management.azure.com/",
#   "activeDirectoryGraphResourceId": "https://graph.windows.net/",
#   "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
#   "galleryEndpointUrl": "https://gallery.azure.com/",
#   "managementEndpointUrl": "https://management.core.windows.net/"
# }
```

---

## 📁 Step 4: Store Credentials Securely

### Create Global Config
```bash
# Create secrets directory
mkdir -p ~/.config/secrets

# Create Azure credentials file
cat > ~/.config/secrets/azure.env << 'EOF'
# Azure Service Principal Credentials
AZURE_SUBSCRIPTION_ID="your-subscription-id"
AZURE_TENANT_ID="your-tenant-id"
AZURE_CLIENT_ID="your-client-id"
AZURE_CLIENT_SECRET="your-client-secret"

# Azure Resource Configuration
AZURE_RESOURCE_GROUP="coffeeverse-rg"
AZURE_LOCATION="eastus"
AZURE_STORAGE_ACCOUNT="coffeeversedata"
AZURE_FUNCTION_APP="coffeeverse-func"
AZURE_COSMOSDB_ACCOUNT="coffeeverse-cosmos"
EOF

# Secure the file
chmod 600 ~/.config/secrets/azure.env
```

### Update .gitignore
```bash
# Add to your project's .gitignore
cat >> .gitignore << 'EOF'

# Azure Credentials (CRITICAL - NEVER COMMIT)
azure.env
*.env
.azure/
.azcli/
.azure_secrets/
EOF
```

### Load Credentials
```bash
# Source credentials before deployment
source ~/.config/secrets/azure.env

# Verify
echo $AZURE_SUBSCRIPTION_ID
```

---

## 💰 Step 5: Cost Control Setup

### Set Up Cost Alerts
```bash
# Create budget alert ($5 threshold)
az consumption budget create \
  --budget-name "coffeeverse-budget" \
  --amount 5 \
  --time-grain Monthly \
  --time-period start-date=$(date +%Y-%m-01) \
  --notifications \
    notification1="{\"enabled\":true,\"operator\":\"GreaterThan\",\"threshold\":80,\"contactEmails\":[\"your-email@example.com\"]}"
```

### Enable Cost Analysis
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to "Cost Management + Billing"
3. Click "Cost analysis"
4. Set up custom views for:
   - Daily costs
   - Service breakdown
   - Resource group trends

### Set Spending Limit
```bash
# List spending limits
az consumption reservation summary list

# Azure Free Account has auto spending limit
# After $200 credit expires, services pause automatically
```

---

## 🧪 Step 6: Verify Setup

### Test Authentication
```bash
# Test Azure CLI
az account show

# Test creating a resource group (free operation)
az group create \
  --name coffeeverse-test-rg \
  --location eastus

# List resource groups
az group list --output table

# Clean up test
az group delete --name coffeeverse-test-rg --yes --no-wait
```

### Test Service Principal
```bash
# Login with service principal
az login --service-principal \
  --username $AZURE_CLIENT_ID \
  --password $AZURE_CLIENT_SECRET \
  --tenant $AZURE_TENANT_ID

# Verify access
az account show
```

---

## 📊 Step 7: Monitor Free Tier Usage

### Check Current Usage
```bash
# List all resources
az resource list --output table

# Check storage usage
az storage account show-usage --location eastus

# Check Cosmos DB usage
az cosmosdb show \
  --resource-group coffeeverse-rg \
  --name coffeeverse-cosmos \
  --query "{throughput:properties.capabilities[0].name, freeThreshold:properties.freeThreshold}"
```

### Set Up Usage Dashboard
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to "Azure Advisor"
3. Review "Cost" recommendations
4. Enable "Advisor Cost Alerts"

---

## 🚨 Common Issues & Fixes

### Issue: "Subscription not found"
```bash
# Solution: Ensure you're logged in
az login
az account set --subscription "Your-Subscription-ID"
```

### Issue: "Insufficient permissions"
```bash
# Solution: Grant contributor role to service principal
az role assignment create \
  --assignee $AZURE_CLIENT_ID \
  --role Contributor \
  --scope /subscriptions/$AZURE_SUBSCRIPTION_ID
```

### Issue: "Resource quota exceeded"
```bash
# Solution: Check and request quota increase
az vm list-usage --location eastus --output table

# Request increase in Azure Portal:
# Portal → Subscriptions → Usage + quotas → Request increase
```

### Issue: "Credit card verification failed"
```bash
# Solution: Use a valid credit/debit card
# Note: You won't be charged during free trial
# Card is only for identity verification
```

---

## ✅ Pre-Deployment Checklist

Before running `deploy/deploy.sh`, ensure:

- [ ] Azure CLI installed and working (`az --version`)
- [ ] Successfully logged in (`az account show`)
- [ ] Service principal created and saved
- [ ] Credentials stored in `~/.config/secrets/azure.env`
- [ ] `.gitignore` includes credential files
- [ ] Cost alerts configured
- [ ] Free tier limits understood
- [ ] Resource group name chosen (e.g., `coffeeverse-rg`)
- [ ] Location selected (e.g., `eastus`)

---

## 🎓 Free Tier Best Practices

### DO:
✅ Use **serverless** services (Functions, Cosmos DB serverless)  
✅ Enable **auto-pause** for SQL Database  
✅ Set up **cost alerts** immediately  
✅ Use **lifecycle policies** for Blob Storage  
✅ Monitor **RU consumption** in Cosmos DB  
✅ Deploy to **free tier regions** (eastus, westus, westeurope)

### DON'T:
❌ Create multiple resource groups (harder to track)  
❌ Use **premium** tiers (App Service, Storage)  
❌ Leave **idle resources** running  
❌ Exceed **1000 RU/s** in Cosmos DB  
❌ Store > 5GB in Blob Storage  
❌ Create more than **5 Data Factory activities**

---

## 📚 Additional Resources

- [Azure Free Tier Details](https://azure.microsoft.com/en-us/pricing/free-services)
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
- [Cost Management Best Practices](https://learn.microsoft.com/en-us/azure/cost-management-billing/)
- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)
- [Service Principal Guide](https://learn.microsoft.com/en-us/entra/identity-platform/howto-create-service-principal-portal)

---

## 🔗 Next Steps

Once your Azure account is set up:

1. Review the [Deployment Guide](./DEPLOYMENT.md)
2. Deploy infrastructure: `./deploy/deploy.sh`
3. Load sample data: `python load_sample_data.py`
4. Deploy dashboard to Streamlit Cloud
5. Monitor costs in Azure Portal

---

**Last Updated**: November 15, 2025  
**Status**: ✅ Ready for Azure Free Tier deployment

