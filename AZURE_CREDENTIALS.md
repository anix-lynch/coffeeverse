# 🔐 Coffeeverse Azure Credentials

**⚠️ KEEP THIS FILE PRIVATE - DO NOT COMMIT TO GITHUB**

---

## Azure Subscription Info

```
Subscription ID: 240061ae-eb56-4e65-a6dc-11d4114b7267
Tenant ID: cd8b1986-ff84-47bf-a254-56ccbb7f0951
Account Email: alynch@gozeroshot.dev
Region: eastus
```

---

## Resource Group

```
Name: coffeeverse-rg
Location: eastus
Status: Active
```

---

## Storage Account

```
Name: coffeeversestorage75993
SKU: Standard_LRS
Kind: StorageV2
HTTPS Only: Enabled
```

**To get key:**
```bash
az storage account keys list \
  --resource-group coffeeverse-rg \
  --account-name coffeeversestorage75993 \
  --query "[0].value" -o tsv
```

---

## Cosmos DB

```
Name: coffeeverse-cosmos-12345
Kind: GlobalDocumentDB
Free Tier: Enabled
Default Consistency: Session
RU/s: 1000 (free)
Storage: 25GB (free)
```

**To get endpoint:**
```bash
az cosmosdb show \
  --resource-group coffeeverse-rg \
  --name coffeeverse-cosmos-12345 \
  --query "documentEndpoint" -o tsv
```

**To get key:**
```bash
az cosmosdb keys list \
  --resource-group coffeeverse-rg \
  --name coffeeverse-cosmos-12345 \
  --query "primaryMasterKey" -o tsv
```

---

## Environment Variables to Set

**Location:** `~/.config/secrets/global.env`

```bash
export AZURE_SUBSCRIPTION_ID="240061ae-eb56-4e65-a6dc-11d4114b7267"
export AZURE_STORAGE_ACCOUNT="coffeeversestorage75993"
export AZURE_STORAGE_KEY="[GET VIA SCRIPT]"
export AZURE_COSMOS_URL="[GET VIA SCRIPT]"
export AZURE_COSMOS_KEY="[GET VIA SCRIPT]"
```

---

## How to Get Credentials

**Automated (Recommended):**
```bash
cd /Users/anixlynch/dev/northstar/06_coffeeverse
./deploy/create-azure-resources.sh
```

This will:
- Create resources if they don't exist
- Extract all 3 secrets
- Auto-update ~/.config/secrets/global.env

**Manual (if needed):**
```bash
# Set subscription
az account set --subscription "240061ae-eb56-4e65-a6dc-11d4114b7267"

# Get Storage Key
az storage account keys list \
  --resource-group coffeeverse-rg \
  --account-name coffeeversestorage75993 \
  --query "[0].value" -o tsv

# Get Cosmos URL
az cosmosdb show \
  --resource-group coffeeverse-rg \
  --name coffeeverse-cosmos-12345 \
  --query "documentEndpoint" -o tsv

# Get Cosmos Key
az cosmosdb keys list \
  --resource-group coffeeverse-rg \
  --name coffeeverse-cosmos-12345 \
  --query "primaryMasterKey" -o tsv
```

---

## Security Checklist

- [ ] Credentials stored in `~/.config/secrets/global.env` (LOCAL ONLY)
- [ ] `.gitignore` includes `*.env`, `*.key`, `secrets/`
- [ ] NEVER commit credentials to GitHub
- [ ] NEVER share credential values publicly
- [ ] Only share resource names (this file is safe)
- [ ] Keep backup: `~/.config/secrets/global.env.backup`

---

## For Docker Deployment

```bash
# Load credentials
source ~/.config/secrets/global.env

# Build Docker image
docker build -t anixlynch/coffeeverse:latest .

# Run with credentials
docker-compose up -d

# Verify connection
docker logs coffeeverse-dashboard | grep -i "azure\|cosmos"
```

---

## Cost Monitoring

**Current Spend:** $0.00/month (Azure Free Tier)

**Services:**
- ✅ Storage: 5GB free (using <1GB)
- ✅ Cosmos DB: 1000 RU/s free
- ✅ Functions: 1M executions/month free

**Budget Alert:** $10/month max

---

## Troubleshooting

### "SubscriptionNotFound" Error
```bash
# Always set subscription first!
az account set --subscription "240061ae-eb56-4e65-a6dc-11d4114b7267"
```

### Can't connect to Cosmos DB
```bash
# Verify credentials in ~/.config/secrets/global.env
cat ~/.config/secrets/global.env | grep AZURE

# Test connection from Python
python -c "
from azure.cosmos import CosmosClient
import os
url = os.environ['AZURE_COSMOS_URL']
key = os.environ['AZURE_COSMOS_KEY']
client = CosmosClient(url, credential=key)
print('✅ Connected to Cosmos DB')
"
```

---

## Contact & Support

- **GitHub:** https://github.com/anix-lynch/coffeeverse
- **Documentation:** See AZURE_AUTH_SETUP.md
- **Docker Hub:** https://hub.docker.com/r/anixlynch/coffeeverse

---

**Last Updated:** 2025-11-17  
**Status:** ✅ Ready for Deployment

