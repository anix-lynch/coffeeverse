# Coffeeverse Runbook

## Quick Start

### Prerequisites
- Azure CLI installed and authenticated
- Python 3.10+
- Docker (optional)

### Local Development

```bash
# 1. Clone and setup
git clone https://github.com/anix-lynch/coffeeverse
cd coffeeverse
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# 2. Run Streamlit app locally
streamlit run src/app/streamlit_app.py

# 3. Test Azure Functions locally
cd src/pipelines
func start
```

## Deployment

### 1. Deploy Infrastructure

```bash
# Login to Azure
az login
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# Deploy resources
cd infrastructure/scripts
chmod +x deploy.sh
./deploy.sh

# Note the output values:
# - Storage Account Name
# - Cosmos DB Endpoint
# - Function App Name
```

### 2. Deploy Functions

```bash
cd src/pipelines
func azure functionapp publish <FUNCTION_APP_NAME>
```

### 3. Deploy Streamlit App

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect GitHub repo: `anix-lynch/coffeeverse`
3. Set main file: `src/app/streamlit_app.py`
4. Add secrets (from Azure deployment output)
5. Deploy

### 4. Run dbt Models

```bash
cd dbt
dbt run --profiles-dir .
dbt test
```

## Configuration

### Environment Variables

Create `.env` file (never commit):

```bash
# Azure Storage
AZURE_STORAGE_ACCOUNT=your_account_name
AZURE_STORAGE_KEY=your_key

# Cosmos DB
AZURE_COSMOS_URL=https://your-account.documents.azure.com:443/
AZURE_COSMOS_KEY=your_key

# Azure Functions
STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...
```

### Streamlit Secrets

Add to Streamlit Cloud (Settings → Secrets):

```toml
AZURE_STORAGE_ACCOUNT = "your_account"
AZURE_STORAGE_KEY = "your_key"
AZURE_COSMOS_URL = "https://your-account.documents.azure.com:443/"
AZURE_COSMOS_KEY = "your_key"
```

## Troubleshooting

### Function Not Triggering

**Symptom**: Blob uploaded but function doesn't run

**Fix**:
```bash
# Check function logs
az functionapp logs tail --name <FUNCTION_APP_NAME> --resource-group <RG_NAME>

# Verify storage connection
az storage account show-connection-string --name <STORAGE_ACCOUNT>
```

### Cosmos DB Connection Failed

**Symptom**: `CosmosHttpResponseError`

**Fix**:
```bash
# Verify endpoint and key
az cosmosdb show --name <COSMOS_ACCOUNT> --resource-group <RG_NAME>
az cosmosdb keys list --name <COSMOS_ACCOUNT> --resource-group <RG_NAME>

# Check firewall rules
az cosmosdb update --name <COSMOS_ACCOUNT> --resource-group <RG_NAME> \
  --enable-public-network true
```

### Streamlit App Won't Start

**Symptom**: "Error installing requirements"

**Fix**:
1. Check `requirements.txt` has pinned versions
2. Verify `runtime.txt` specifies `python-3.10`
3. Clear Streamlit Cloud cache: Settings → Advanced → Clear cache
4. Redeploy

### dbt Run Fails

**Symptom**: `Could not connect to Cosmos DB`

**Fix**:
```bash
# Verify profiles.yml has correct credentials
cd dbt
dbt debug

# Test connection
dbt run-operation test_connection
```

## Monitoring

### Check Pipeline Health

```bash
# Function app status
az functionapp show --name <FUNCTION_APP_NAME> --resource-group <RG_NAME> \
  --query "state"

# Recent function executions
az monitor activity-log list --resource-group <RG_NAME> \
  --max-events 10

# Cosmos DB metrics
az cosmosdb show --name <COSMOS_ACCOUNT> --resource-group <RG_NAME> \
  --query "documentEndpoint"
```

### View Logs

```bash
# Function logs (live)
az functionapp logs tail --name <FUNCTION_APP_NAME> --resource-group <RG_NAME>

# Streamlit logs
# Go to share.streamlit.io → Manage app → View logs
```

## Cleanup

### Delete All Resources

```bash
cd infrastructure/scripts
chmod +x destroy.sh
./destroy.sh

# Or manually
az group delete --name <RG_NAME> --yes
```

## Cost Monitoring

```bash
# Check current month costs
az consumption usage list --start-date $(date -d "1 month ago" +%Y-%m-%d) \
  --end-date $(date +%Y-%m-%d)

# Set budget alert
az consumption budget create --budget-name coffeeverse-budget \
  --amount 10 --time-grain Monthly --start-date $(date +%Y-%m-01)
```

## Maintenance

### Update Dependencies

```bash
# Update Python packages
pip list --outdated
pip install --upgrade <package>
pip freeze > requirements.txt

# Update Azure Functions runtime
# Edit src/pipelines/host.json → "version": "4.0"
```

### Backup Cosmos DB

```bash
# Export data
az cosmosdb collection export --name <COSMOS_ACCOUNT> \
  --resource-group <RG_NAME> --db-name coffeeverse \
  --collection-name cocktails --output-path ./backup/
```

## Support

- **Issues**: [GitHub Issues](https://github.com/anix-lynch/coffeeverse/issues)
- **Documentation**: See `/docs` folder
- **Contact**: [LinkedIn](https://linkedin.com/in/anixlynch)
