# Data Contracts

## Overview

This document defines the schemas, expectations, and contracts for data flowing through the Coffeeverse pipeline.

## Data Layers

### Bronze Layer (Raw)
**Location**: Azure Blob Storage (`raw/` container)  
**Format**: NDJSON (newline-delimited JSON)  
**Source**: TheCocktailDB API

### Silver Layer (Cleaned)
**Location**: Azure Cosmos DB  
**Format**: JSON documents  
**Transformations**: Validated, cleaned, enriched

### Gold Layer (Analytics)
**Location**: Cosmos DB (separate container)  
**Format**: dbt-modeled tables  
**Purpose**: Business metrics and aggregations

---

## Schema Definitions

### Bronze: Raw Cocktail Data

**Source**: `https://www.thecocktaildb.com/api/json/v1/1/search.php?s=`

```json
{
  "idDrink": "string",           // Required, unique ID
  "strDrink": "string",          // Required, cocktail name
  "strCategory": "string",       // Required, e.g. "Cocktail"
  "strAlcoholic": "string",      // Required, "Alcoholic" or "Non alcoholic"
  "strGlass": "string",          // Optional, glass type
  "strInstructions": "string",   // Required, preparation steps
  "strDrinkThumb": "string",     // Optional, image URL
  "strIngredient1": "string",    // Optional, first ingredient
  "strIngredient2": "string",    // Optional, second ingredient
  // ... up to strIngredient15
  "strMeasure1": "string",       // Optional, first measure
  "strMeasure2": "string",       // Optional, second measure
  // ... up to strMeasure15
}
```

**Validation Rules**:
- `idDrink` must be present and non-empty
- `strDrink` must be present and non-empty
- `strCategory` must be present
- `strAlcoholic` must be present
- `strInstructions` must be present

---

### Silver: Cleaned Cocktail Data

**Location**: Cosmos DB `cocktails` container

```json
{
  "id": "string",                    // Mapped from idDrink
  "name": "string",                  // Mapped from strDrink
  "category": "string",              // Mapped from strCategory
  "alcoholic": "boolean",            // Parsed from strAlcoholic
  "glass": "string",                 // Mapped from strGlass
  "instructions": "string",          // Mapped from strInstructions
  "thumbnail_url": "string",         // Mapped from strDrinkThumb
  "ingredients": [                   // Parsed from strIngredient1-15
    {
      "name": "string",
      "measure": "string"
    }
  ],
  "ingredient_count": "integer",     // Calculated
  "complexity_score": "float",       // Calculated (1-10)
  "estimated_calories": "integer",   // Calculated
  "processed_at": "datetime",        // ISO 8601 timestamp
  "source": "string",                // "thecocktaildb"
  "version": "string"                // Schema version "1.0"
}
```

**Enrichment Logic**:
- `complexity_score`: Based on ingredient count and instruction length
  - 1-3 ingredients: score 1-3
  - 4-6 ingredients: score 4-6
  - 7+ ingredients: score 7-10
- `estimated_calories`: Rough estimate based on ingredient types
  - Spirits: ~100 cal/oz
  - Liqueurs: ~150 cal/oz
  - Juices: ~50 cal/oz
  - Syrups: ~100 cal/oz

**Validation Rules**:
- All required fields from Bronze must be present
- `id` must be unique (partition key)
- `alcoholic` must be boolean
- `complexity_score` must be 1-10
- `processed_at` must be valid ISO 8601

---

### Gold: Analytics Mart

**Location**: Cosmos DB `analytics` container  
**Model**: `mart_cocktail_analytics`

```json
{
  "id": "string",                    // Unique analytics record ID
  "spirit_type": "string",           // Primary spirit (Vodka, Rum, etc.)
  "category": "string",              // Cocktail category
  "avg_complexity": "float",         // Average complexity for this group
  "total_cocktails": "integer",      // Count of cocktails
  "avg_calories": "float",           // Average calories
  "alcoholic_pct": "float",          // % alcoholic in this group
  "popular_glass": "string",         // Most common glass type
  "generated_at": "datetime"         // Timestamp of calculation
}
```

**Aggregation Logic**:
- Group by `spirit_type` and `category`
- Calculate averages and counts
- Identify most common glass type per group
- Update daily via dbt scheduled run

---

## Data Quality Rules

### Completeness
- **Bronze**: 100% of required fields must be present
- **Silver**: All enrichment fields must be calculated
- **Gold**: No null values in aggregated metrics

### Accuracy
- **Complexity Score**: Must be between 1-10
- **Calorie Estimate**: Must be positive integer
- **Timestamps**: Must be valid ISO 8601

### Consistency
- **ID Format**: Must match source format (numeric string)
- **Boolean Fields**: Must be true/false (not "yes"/"no")
- **Timestamps**: Must use UTC timezone

### Timeliness
- **Bronze → Silver**: Process within 5 seconds of blob upload
- **Silver → Gold**: Update daily at 00:00 UTC
- **Dashboard**: Refresh every 5 minutes

---

## Breaking Changes

### Version 1.0 → 1.1 (Planned)
- Add `difficulty_level` field (Easy/Medium/Hard)
- Add `preparation_time` estimate
- Add `flavor_profile` tags

**Migration Plan**:
1. Add new fields with default values
2. Backfill historical data
3. Update validation rules
4. Update dbt models
5. Update Streamlit dashboard

---

## Testing

### Unit Tests
- Validate schema compliance
- Test enrichment calculations
- Verify data type conversions

### Integration Tests
- End-to-end pipeline test with sample data
- Verify Cosmos DB writes
- Check dbt model outputs

### Data Quality Tests (dbt)
```sql
-- tests/assert_valid_complexity.sql
SELECT * FROM {{ ref('stg_cocktails') }}
WHERE complexity_score < 1 OR complexity_score > 10

-- tests/assert_no_nulls.sql
SELECT * FROM {{ ref('mart_cocktail_analytics') }}
WHERE spirit_type IS NULL OR category IS NULL
```

---

## Sample Data

### Bronze Sample
```json
{"idDrink":"11007","strDrink":"Margarita","strCategory":"Ordinary Drink","strAlcoholic":"Alcoholic","strGlass":"Cocktail glass","strInstructions":"Rub the rim of the glass with the lime slice...","strIngredient1":"Tequila","strMeasure1":"1 1/2 oz"}
```

### Silver Sample
```json
{
  "id": "11007",
  "name": "Margarita",
  "category": "Ordinary Drink",
  "alcoholic": true,
  "glass": "Cocktail glass",
  "instructions": "Rub the rim of the glass with the lime slice...",
  "ingredients": [{"name": "Tequila", "measure": "1 1/2 oz"}],
  "ingredient_count": 3,
  "complexity_score": 3.5,
  "estimated_calories": 200,
  "processed_at": "2024-02-23T12:00:00Z",
  "source": "thecocktaildb",
  "version": "1.0"
}
```

---

## Contact

For schema changes or questions:
- **Owner**: Data Engineering Team
- **Slack**: #coffeeverse-data
- **Email**: data@coffeeverse.dev
