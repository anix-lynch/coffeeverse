# Azure CLI Authentication Success Pattern

**Context**: Successfully authenticated Azure CLI with Free Tier account after initial subscription issues.

## ✅ Authentication Setup (WORKING)

### 1. Initial Login
```bash
az login
# Opens browser for authentication
```

### 2. Set Subscription (CRITICAL - Fixes "SubscriptionNotFound" error)
```bash
az account list --output table  # List all subscriptions
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

**Problem Solved**: The "SubscriptionNotFound" error happens when subscription isn't SET, even if you're logged in. Setting it explicitly fixes this.

### 3. Verify Authentication
```bash
az account show --output table
# Shows current subscription + user info
```

## 🛡️ Cost Protection (Automatic)

**NO CHARGES for Coffeeverse because:**
- ✅ Storage Account: 5GB free/month (we use <1GB)
- ✅ Cosmos DB: 1000 RU/s + 25GB free forever
- ✅ Functions: 1M executions/month free
- ✅ Budget alert set: $10/month max (emails if exceeded)

**Verify**: `az costmanagement query --timeframe "MonthToDate" --type "ActualCost"`

## 🔑 Key Commands for Next AI

```bash
# Set subscription first (ALWAYS)
az account set --subscription "240061ae-eb56-4e65-a6dc-11d4114b7267"

# Verify you're authenticated
az account show

# Create resources
az group create --name my-rg --location eastus
az storage account create --name mystg --resource-group my-rg --sku Standard_LRS

# Get secrets for apps
az storage account keys list --account-name mystg --resource-group my-rg --query "[0].value" -o tsv
```

## ⚠️ Common Pitfalls (Avoid These)

1. **Forgetting to set subscription** → "SubscriptionNotFound"
   - FIX: `az account set --subscription "ID"`

2. **Running in sandbox shell** → Subscription context lost
   - FIX: Use single combined command with `&&` not separate commands

3. **Auth expires in new terminal** → Need to `az login` again
   - FIX: Just login again if needed

## ✅ Success Indicators

- `az account show` returns your subscription info
- `az group create` works without errors
- `az storage account create` succeeds
- Free Tier resources created = $0 cost

---

**Status**: Azure CLI fully authenticated and cost-protected ✅
**For Next AI**: Copy the "Key Commands" section above, always set subscription first

