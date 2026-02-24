#!/bin/bash
set -e

# Set Azure credentials from environment if provided
if [ -n "$AZURE_STORAGE_ACCOUNT" ] && [ -n "$AZURE_STORAGE_KEY" ]; then
    echo "Configuring Azure credentials..."
    export AZURE_STORAGE_ACCOUNT="${AZURE_STORAGE_ACCOUNT}"
    export AZURE_STORAGE_KEY="${AZURE_STORAGE_KEY}"
fi

if [ -n "$AZURE_COSMOS_URL" ] && [ -n "$AZURE_COSMOS_KEY" ]; then
    echo "Configuring Cosmos DB credentials..."
    export AZURE_COSMOS_URL="${AZURE_COSMOS_URL}"
    export AZURE_COSMOS_KEY="${AZURE_COSMOS_KEY}"
fi

# Create .streamlit directory if it doesn't exist
mkdir -p ~/.streamlit

# If Streamlit is being run, configure it
if [[ "$*" == *"streamlit"* ]]; then
    echo "Configuring Streamlit..."
    cat > ~/.streamlit/config.toml << EOF
[logger]
level = "info"

[client]
showErrorDetails = true

[browser]
gatherUsageStats = false
EOF
fi

# Execute the command passed to the container
exec "$@"

