#!/usr/bin/env python3
"""
Coffeeverse Azure Function - ETL Transform

🎯 PURPOSE: Processes raw JSON data from Blob Storage, validates/transforms it, stores in Cosmos DB.
📊 FEATURES: Schema validation, data enrichment, timestamp tracking, error handling,
           integrates with Cosmos DB for processed data and Blob Storage for raw/processed containers.
🏗️ ARCHITECTURE: Triggered by Blob Storage event. Reads from raw container, transforms,
               writes to Cosmos DB and processed container.
⚡ PERFORMANCE: Sub-second processing, designed for high concurrency and auto-scaling.
"""
import azure.functions as func
import json
import logging
from datetime import datetime
from azure.cosmos import CosmosClient, exceptions
from azure.storage.blob import BlobServiceClient
import os

app = func.FunctionApp()

# Configuration from environment variables
COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
COSMOS_KEY = os.environ.get("COSMOS_KEY")
COSMOS_DATABASE = os.environ.get("COSMOS_DATABASE", "coffeeverse")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER", "cocktails")
STORAGE_CONNECTION_STRING = os.environ.get("STORAGE_CONNECTION_STRING")
PROCESSED_CONTAINER = os.environ.get("PROCESSED_CONTAINER", "processed")

# Initialize clients
cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = cosmos_client.get_database_client(COSMOS_DATABASE)
container = database.get_container_client(COSMOS_CONTAINER)
blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)


def validate_cocktail_data(data: dict) -> bool:
    """
    Basic validation for cocktail data.
    Ensures essential fields are present.
    """
    required_fields = ["idDrink", "strDrink", "strCategory", "strAlcoholic", "strInstructions"]
    if not all(data.get(field) for field in required_fields):
        logging.warning(f"Missing required fields in data: {data.get('idDrink', 'N/A')}")
        return False
    return True


def enrich_cocktail_data(data: dict) -> dict:
    """
    Adds enrichment fields to the cocktail data.
    - processing_timestamp
    - source_api (hardcoded for now, could be dynamic)
    - Azure-specific metadata
    """
    data['processing_timestamp'] = datetime.utcnow().isoformat() + 'Z'
    data['source_api'] = 'TheCocktailDB'
    data['cloud_provider'] = 'Azure'
    data['processing_service'] = 'Azure Functions'
    
    # Flatten ingredients and measures into a list of dicts for easier querying
    ingredients_list = []
    for i in range(1, 16):  # Max 15 ingredients
        ingredient_key = f"strIngredient{i}"
        measure_key = f"strMeasure{i}"
        
        ingredient = data.get(ingredient_key)
        measure = data.get(measure_key)
        
        if ingredient:
            ingredients_list.append({
                "ingredient": ingredient,
                "measure": measure if measure else ""
            })
        
        # Remove original strIngredientX and strMeasureX keys to clean up
        data.pop(ingredient_key, None)
        data.pop(measure_key, None)
        
    data['ingredients'] = ingredients_list
    
    # Add id field for Cosmos DB (required)
    data['id'] = data['idDrink']
    
    return data


@app.blob_trigger(arg_name="myblob", path="raw/{name}",
                  connection="STORAGE_CONNECTION_STRING")
def blob_trigger(myblob: func.InputStream):
    """
    Triggered when a new blob is uploaded to the 'raw' container.
    Processes the blob and stores results in Cosmos DB and processed container.
    """
    logging.info(f"Python blob trigger function processed blob"
                 f"Name: {myblob.name}"
                 f"Blob Size: {myblob.length} bytes")
    
    try:
        # Read blob content
        blob_content = myblob.read().decode('utf-8')
        
        # Parse NDJSON (one JSON object per line)
        cocktails_raw = [json.loads(line) for line in blob_content.splitlines() if line.strip()]
        
        processed_cocktails = []
        for cocktail_data in cocktails_raw:
            if validate_cocktail_data(cocktail_data):
                enriched_data = enrich_cocktail_data(cocktail_data)
                processed_cocktails.append(enriched_data)
                
                # Store in Cosmos DB
                try:
                    container.upsert_item(enriched_data)
                    logging.info(f"Successfully loaded {enriched_data.get('id')} to Cosmos DB.")
                except exceptions.CosmosHttpResponseError as e:
                    logging.error(f"Error writing to Cosmos DB: {e}")
            else:
                logging.warning(f"Skipping invalid cocktail data: {cocktail_data.get('idDrink', 'N/A')}")
        
        # Write processed data to 'processed' container
        processed_blob_name = f"processed/{datetime.now().strftime('%Y/%m/%d')}/{os.path.basename(myblob.name)}"
        processed_container_client = blob_service_client.get_blob_client(
            container=PROCESSED_CONTAINER,
            blob=processed_blob_name
        )
        
        processed_content = json.dumps(processed_cocktails, indent=2)
        processed_container_client.upload_blob(processed_content, overwrite=True)
        logging.info(f"Successfully wrote processed data to {processed_blob_name}")
        
    except Exception as e:
        logging.error(f"Error processing blob {myblob.name}: {e}")
        raise e


@app.route(route="health", methods=["GET"])
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint for monitoring."""
    return func.HttpResponse(
        json.dumps({"status": "healthy", "service": "coffeeverse-function"}),
        mimetype="application/json",
        status_code=200
    )


@app.route(route="process", methods=["POST"])
def manual_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """
    Manual trigger endpoint for testing.
    Accepts JSON payload and processes it directly.
    """
    try:
        req_body = req.get_json()
        logging.info(f"Received manual trigger with {len(req_body)} items")
        
        processed_count = 0
        for item in req_body:
            if validate_cocktail_data(item):
                enriched = enrich_cocktail_data(item)
                container.upsert_item(enriched)
                processed_count += 1
        
        return func.HttpResponse(
            json.dumps({
                "status": "success",
                "processed": processed_count,
                "total": len(req_body)
            }),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error in manual trigger: {e}")
        return func.HttpResponse(
            json.dumps({"status": "error", "message": str(e)}),
            mimetype="application/json",
            status_code=500
        )

