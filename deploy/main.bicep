@description('The name of the environment (dev, staging, prod)')
param environment string = 'dev'

@description('Location for all resources')
param location string = resourceGroup().location

@description('Project name')
param projectName string = 'coffeeverse'

@description('Unique suffix for resources')
param uniqueSuffix string = uniqueString(resourceGroup().id)

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: '${projectName}storage${uniqueSuffix}'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    encryption: {
      services: {
        blob: {
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
  }
  tags: {
    Environment: environment
    Project: projectName
  }
}

// Blob containers
resource rawDataContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/coffeeverse-raw-data'
  dependsOn: [
    storageAccount
  ]
}

resource processedDataContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/coffeeverse-processed-data'
  dependsOn: [
    storageAccount
  ]
}

resource dbtDataContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: '${storageAccount.name}/default/coffeeverse-dbt-data'
  dependsOn: [
    storageAccount
  ]
}

// Cosmos DB Account
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' = {
  name: '${projectName}-cosmos-${uniqueSuffix}'
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    databaseAccountOfferType: 'Standard'
    enableAutomaticFailover: false
    enableMultipleWriteLocations: false
    enableAnalyticalStorage: true
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
  }
  tags: {
    Environment: environment
    Project: projectName
  }
}

// Cosmos DB Database
resource cosmosDatabase 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2023-04-15' = {
  name: '${cosmosAccount.name}/coffeeverse-db'
  properties: {
    resource: {
      id: 'coffeeverse-db'
    }
  }
  dependsOn: [
    cosmosAccount
  ]
}

// Cosmos DB Containers
resource cocktailsContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2023-04-15' = {
  name: '${cosmosDatabase.name}/cocktails'
  properties: {
    resource: {
      id: 'cocktails'
      partitionKey: {
        paths: [
          '/category'
        ]
        kind: 'Hash'
      }
      indexingPolicy: {
        indexingMode: 'consistent'
        automatic: true
        includedPaths: [
          {
            path: '/*'
          }
        ]
        excludedPaths: [
          {
            path: '/"_etag"/?'
          }
        ]
      }
      uniqueKeyPolicy: {
        uniqueKeys: [
          {
            paths: [
              '/id'
            ]
          }
        ]
      }
      conflictResolutionPolicy: {
        mode: 'LastWriterWins'
        conflictResolutionPath: '/_ts'
      }
    }
    options: {
      throughput: 1000
    }
  }
  dependsOn: [
    cosmosDatabase
  ]
}

resource pipelineMetadataContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2023-04-15' = {
  name: '${cosmosDatabase.name}/pipeline-metadata'
  properties: {
    resource: {
      id: 'pipeline-metadata'
      partitionKey: {
        paths: [
          '/pipeline_name'
        ]
        kind: 'Hash'
      }
      indexingPolicy: {
        indexingMode: 'consistent'
        automatic: true
        includedPaths: [
          {
            path: '/last_run/?'
          }
          {
            path: '/status/?'
          }
        ]
        excludedPaths: [
          {
            path: '/"_etag"/?'
          }
        ]
      }
    }
    options: {
      throughput: 400
    }
  }
  dependsOn: [
    cosmosDatabase
  ]
}

// Azure Functions App Service Plan (Consumption Plan - Free Tier)
resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: '${projectName}-plan-${uniqueSuffix}'
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
  properties: {
    reserved: false
  }
  tags: {
    Environment: environment
    Project: projectName
  }
}

// Azure Functions App
resource functionApp 'Microsoft.Web/sites@2022-09-01' = {
  name: '${projectName}-func-${uniqueSuffix}'
  location: location
  kind: 'functionapp'
  properties: {
    serverFarmId: appServicePlan.id
    functionAppConfig: {
      runtime: {
        name: 'python'
        version: '3.11'
      }
    }
    siteConfig: {
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${listKeys(storageAccount.name, storageAccount.apiVersion).keys[0].value};EndpointSuffix=core.windows.net'
        }
        {
          name: 'WEBSITE_RUN_FROM_PACKAGE'
          value: '1'
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'AzureCosmosDBConnectionString'
          value: 'AccountEndpoint=${cosmosAccount.properties.documentEndpoint};AccountKey=${listKeys(cosmosAccount.name, cosmosAccount.apiVersion).keys[0].value};'
        }
        {
          name: 'PROJECT_NAME'
          value: projectName
        }
        {
          name: 'ENVIRONMENT'
          value: environment
        }
      ]
    }
  }
  dependsOn: [
    appServicePlan
    storageAccount
    cosmosAccount
  ]
  tags: {
    Environment: environment
    Project: projectName
  }
}

// Data Factory
resource dataFactory 'Microsoft.DataFactory/factories@2018-06-01' = {
  name: '${projectName}-adf-${uniqueSuffix}'
  location: location
  properties: {
    publicNetworkAccess: 'Enabled'
  }
  dependsOn: [
    storageAccount
    cosmosAccount
  ]
  tags: {
    Environment: environment
    Project: projectName
  }
}

// Linked Services for Data Factory
resource blobLinkedService 'Microsoft.DataFactory/factories/linkedservices@2018-06-01' = {
  name: '${dataFactory.name}/AzureBlobStorage'
  properties: {
    type: 'AzureBlobStorage'
    typeProperties: {
      connectionString: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${listKeys(storageAccount.name, storageAccount.apiVersion).keys[0].value};EndpointSuffix=core.windows.net'
    }
  }
  dependsOn: [
    dataFactory
  ]
}

resource cosmosLinkedService 'Microsoft.DataFactory/factories/linkedservices@2018-06-01' = {
  name: '${dataFactory.name}/AzureCosmosDb'
  properties: {
    type: 'CosmosDb'
    typeProperties: {
      connectionString: 'AccountEndpoint=${cosmosAccount.properties.documentEndpoint};AccountKey=${listKeys(cosmosAccount.name, cosmosAccount.apiVersion).keys[0].value};'
    }
  }
  dependsOn: [
    dataFactory
  ]
}

// Outputs
output storageAccountName string = storageAccount.name
output storageAccountKey string = listKeys(storageAccount.name, storageAccount.apiVersion).keys[0].value
output cosmosAccountName string = cosmosAccount.name
output cosmosAccountEndpoint string = cosmosAccount.properties.documentEndpoint
output cosmosAccountKey string = listKeys(cosmosAccount.name, cosmosAccount.apiVersion).keys[0].value
output functionAppName string = functionApp.name
output functionAppUrl string = functionApp.properties.defaultHostname
output dataFactoryName string = dataFactory.name
output resourceGroupName string = resourceGroup().name
