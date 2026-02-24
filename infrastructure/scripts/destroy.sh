#!/bin/bash

# Coffeeverse Azure Resource Cleanup Script
# Destroys all Azure resources created by the deployment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="coffeeverse"
ENVIRONMENT="dev"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

confirm_destruction() {
    echo -e "${RED}⚠️  WARNING: This will delete ALL Azure resources for $PROJECT_NAME-$ENVIRONMENT${NC}"
    echo
    echo "This includes:"
    echo "  - Storage Account and all blob containers"
    echo "  - Cosmos DB account and all databases/containers"
    echo "  - Azure Functions app"
    echo "  - Data Factory"
    echo "  - Resource Group"
    echo
    read -p "Are you sure you want to continue? (type 'yes' to confirm): " confirm

    if [ "$confirm" != "yes" ]; then
        log_info "Destruction cancelled"
        exit 0
    fi
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check if Azure CLI is installed
    if ! command -v az &> /dev/null; then
        log_error "Azure CLI is not installed."
        exit 1
    fi

    # Check if logged in to Azure
    if ! az account show &> /dev/null; then
        log_error "Not logged in to Azure. Please run: az login"
        exit 1
    fi

    log_success "Prerequisites check passed"
}

find_resource_group() {
    local rg_pattern="${PROJECT_NAME}-rg-${ENVIRONMENT}"

    log_info "Looking for resource group: $rg_pattern"

    local rg_name
    rg_name=$(az group list --query "[?name=='$rg_pattern'].name" --output tsv)

    if [ -z "$rg_name" ]; then
        log_error "Resource group $rg_pattern not found"
        exit 1
    fi

    echo "$rg_name"
}

destroy_resources() {
    local rg_name="$1"

    log_info "Destroying all resources in resource group: $rg_name"

    # List all resources before deletion
    log_info "Resources to be deleted:"
    az resource list --resource-group "$rg_name" --query "[].{name:name, type:type}" --output table

    echo
    read -p "Press Enter to continue with deletion..."

    # Delete resource group (this deletes all resources within it)
    log_warning "Deleting resource group and all resources..."
    az group delete \
        --name "$rg_name" \
        --yes \
        --no-wait \
        --output none

    log_success "Resource group deletion initiated"
    log_info "Note: Deletion may take several minutes to complete"
}

cleanup_local_files() {
    log_info "Cleaning up local files..."

    # Remove environment files
    if [ -f ".env.azure" ]; then
        rm .env.azure
        log_info "Removed .env.azure"
    fi

    if [ -f "deployment_outputs.json" ]; then
        rm deployment_outputs.json
        log_info "Removed deployment_outputs.json"
    fi

    log_success "Local cleanup completed"
}

monitor_deletion() {
    local rg_name="$1"

    log_info "Monitoring deletion progress..."

    # Wait for deletion to complete
    local status
    status=$(az group show --name "$rg_name" --query "properties.provisioningState" --output tsv 2>/dev/null || echo "Deleted")

    local attempts=0
    local max_attempts=30  # 5 minutes with 10s intervals

    while [ "$status" != "Deleted" ] && [ $attempts -lt $max_attempts ]; do
        echo -n "."
        sleep 10
        status=$(az group show --name "$rg_name" --query "properties.provisioningState" --output tsv 2>/dev/null || echo "Deleted")
        ((attempts++))
    done

    echo

    if [ "$status" = "Deleted" ]; then
        log_success "Resource group successfully deleted"
    else
        log_warning "Resource group deletion may still be in progress"
        log_info "Check status manually: az group show --name $rg_name"
    fi
}

main() {
    echo "💥 Coffeeverse Azure Resource Destruction"
    echo "========================================"
    echo

    check_prerequisites
    confirm_destruction

    local rg_name
    rg_name=$(find_resource_group)

    destroy_resources "$rg_name"

    monitor_deletion "$rg_name"

    cleanup_local_files

    echo
    log_success "🗑️  All resources destroyed successfully!"
    echo
    echo "What was cleaned up:"
    echo "  ✅ Azure Storage Account"
    echo "  ✅ Cosmos DB Account & Databases"
    echo "  ✅ Azure Functions App"
    echo "  ✅ Data Factory"
    echo "  ✅ Resource Group"
    echo "  ✅ Local configuration files"
    echo
    echo "To redeploy, run: ./deploy.sh"
}

# Run main function
main "$@"
