{{ config(materialized='view') }}

-- Staging model for raw cocktail data from Cosmos DB
-- This model cleans and standardizes the raw cocktail data

SELECT
    -- Primary key
    id,

    -- Basic cocktail information
    name,
    category,
    glass_type as glass,

    -- Ingredients (stored as JSON array)
    ingredients,

    -- Instructions
    instructions,

    -- Metadata
    processed_at as extracted_at,
    processed_at as enriched_at,

    -- Enrichment fields
    CAST(JSON_VALUE(ingredients, '$.length') AS INT) as ingredient_count,
    CAST(complexity_score AS FLOAT) as complexity_score,
    CASE
        WHEN instructions IS NOT NULL THEN LEN(instructions) - LEN(REPLACE(instructions, ' ', '')) + 1
        ELSE 0
    END as instruction_word_count,
    CASE
        WHEN CAST(complexity_score AS FLOAT) < 3 THEN 5
        WHEN CAST(complexity_score AS FLOAT) BETWEEN 3 AND 6 THEN 15
        ELSE 30
    END as estimated_prep_time,
    CAST(is_alcoholic AS BIT) as is_alcoholic,
    spirit_type,
    CAST(estimated_calories AS INT) as estimated_calories,
    tags,

    -- Audit fields
    CAST(processed_at AS DATETIME2) as loaded_at

FROM {{ source('cosmosdb', 'cocktails') }}

-- Only include valid records
WHERE id IS NOT NULL
  AND name IS NOT NULL
  AND ingredients IS NOT NULL
