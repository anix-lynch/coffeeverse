#!/bin/bash
# Coffeeverse Azure Resource Creation Script
# Run this locally: ./deploy/create-azure-resources.sh

set -e

SUBSCRIPTION_ID="240061ae-eb56-4e65-a6dc-11d4114b7267"
RESOURCE_GROUP="coffeeverse-rg"
LOCATION="eastus"
STORAGE_ACCOUNT="coffeeversestorage75993"
COSMOS_ACCOUNT="coffeeverse-cosmos-12345"

echo "🚀 COFFEEVERSE - Azure Resource Creation"
echo "========================================"
echo ""

# Step 1: Verify subscription
echo "Step 1: Verifying subscription..."
az account show --output table --subscription "$SUBSCRIPTION_ID"
echo ""

# Step 2: Create resource group (if doesn't exist)
echo "Step 2: Creating/verifying resource group..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --subscription "$SUBSCRIPTION_ID" || echo "Resource group already exists"
echo ""

# Step 3: Create Storage Account
echo "Step 3: Creating Storage Account ($STORAGE_ACCOUNT)..."
az storage account create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$STORAGE_ACCOUNT" \
  --sku Standard_LRS \
  --kind StorageV2 \
  --https-only true \
  --output table
echo ""

# Step 4: Create Cosmos DB
echo "Step 4: Creating Cosmos DB ($COSMOS_ACCOUNT)..."
az cosmosdb create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$COSMOS_ACCOUNT" \
  --kind GlobalDocumentDB \
  --enable-free-tier true \
  --output table
echo ""

# Step 5: Get credentials
echo "Step 5: Extracting credentials..."
echo ""

STORAGE_KEY=$(az storage account keys list \
  --resource-group "$RESOURCE_GROUP" \
  --account-name "$STORAGE_ACCOUNT" \
  --query "[0].value" \
  -o tsv)

COSMOS_URL=$(az cosmosdb show \
  --resource-group "$RESOURCE_GROUP" \
  --name "$COSMOS_ACCOUNT" \
  --query "documentEndpoint" \
  -o tsv)

COSMOS_KEY=$(az cosmosdb keys list \
  --resource-group "$RESOURCE_GROUP" \
  --name "$COSMOS_ACCOUNT" \
  --query "primaryMasterKey" \
  -o tsv)

echo ""
echo "✅ CREDENTIALS EXTRACTED!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Add these to ~/.config/secrets/global.env:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "export AZURE_STORAGE_ACCOUNT=\"$STORAGE_ACCOUNT\""
echo "export AZURE_STORAGE_KEY=\"$STORAGE_KEY\""
echo "export AZURE_COSMOS_URL=\"$COSMOS_URL\""
echo "export AZURE_COSMOS_KEY=\"$COSMOS_KEY\""
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 6: Update ~/.config/secrets/global.env
echo "Step 6: Updating ~/.config/secrets/global.env..."
if [ -f ~/.config/secrets/global.env ]; then
  # Backup original
  cp ~/.config/secrets/global.env ~/.config/secrets/global.env.backup
  
  # Update credentials (using | as delimiter since values contain /)
  sed -i '' "s|export AZURE_STORAGE_ACCOUNT=.*|export AZURE_STORAGE_ACCOUNT=\"$STORAGE_ACCOUNT\"|" ~/.config/secrets/global.env
  sed -i '' "s|export AZURE_STORAGE_KEY=.*|export AZURE_STORAGE_KEY=\"$STORAGE_KEY\"|" ~/.config/secrets/global.env
  sed -i '' "s|export AZURE_COSMOS_URL=.*|export AZURE_COSMOS_URL=\"$COSMOS_URL\"|" ~/.config/secrets/global.env
  sed -i '' "s|export AZURE_COSMOS_KEY=.*|export AZURE_COSMOS_KEY=\"$COSMOS_KEY\"|" ~/.config/secrets/global.env
  
  echo "✅ Updated ~/.config/secrets/global.env"
  echo "✅ Backup saved to ~/.config/secrets/global.env.backup"
else
  echo "⚠️ ~/.config/secrets/global.env not found - create it manually"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ COFFEEVERSE AZURE RESOURCES CREATED!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎯 NEXT STEPS:"
echo "1. Start Docker Desktop"
echo "2. cd /Users/anixlynch/dev/northstar/06_coffeeverse"
echo "3. docker build -t anixlynch/coffeeverse:latest ."
echo "4. docker-compose up -d"
echo "5. Visit http://localhost:8501"
echo ""
echo "✨ Dashboard will show REAL data from Cosmos DB!"
echo ""

