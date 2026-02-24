{{ config(materialized='table') }}

-- Analytics mart for cocktail data
-- Provides aggregated insights and KPIs for the cocktail dataset

WITH cocktail_metrics AS (
    SELECT
        -- Cocktail dimensions
        spirit_type,
        category,
        glass,
        CAST(is_alcoholic AS BIT) as is_alcoholic,

        -- Metrics
        COUNT(*) as cocktail_count,
        AVG(CAST(complexity_score AS FLOAT)) as avg_complexity,
        AVG(CAST(ingredient_count AS FLOAT)) as avg_ingredients,
        AVG(CAST(estimated_prep_time AS FLOAT)) as avg_prep_time,
        AVG(CAST(estimated_calories AS FLOAT)) as avg_calories,
        SUM(CAST(estimated_calories AS INT)) as total_calories,

        -- Complexity distribution
        COUNT(CASE WHEN CAST(complexity_score AS FLOAT) < 3 THEN 1 END) as simple_count,
        COUNT(CASE WHEN CAST(complexity_score AS FLOAT) BETWEEN 3 AND 6 THEN 1 END) as intermediate_count,
        COUNT(CASE WHEN CAST(complexity_score AS FLOAT) > 6 THEN 1 END) as complex_count

    FROM {{ ref('stg_cocktails') }}
    GROUP BY spirit_type, category, glass, CAST(is_alcoholic AS BIT)
),

cocktail_rankings AS (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY cocktail_count DESC) as popularity_rank,
        ROW_NUMBER() OVER (ORDER BY avg_complexity DESC) as complexity_rank,
        ROW_NUMBER() OVER (ORDER BY avg_calories DESC) as calorie_rank
    FROM cocktail_metrics
)

SELECT
    -- Dimensions
    spirit_type,
    category,
    glass,
    is_alcoholic,

    -- Metrics
    cocktail_count,
    ROUND(avg_complexity, 2) as avg_complexity,
    ROUND(avg_ingredients, 1) as avg_ingredients,
    ROUND(avg_prep_time, 1) as avg_prep_time,
    ROUND(avg_calories, 0) as avg_calories,
    total_calories,

    -- Complexity breakdown
    simple_count,
    intermediate_count,
    complex_count,

    -- Rankings
    popularity_rank,
    complexity_rank,
    calorie_rank,

    -- Calculated fields
    ROUND((CAST(simple_count AS FLOAT) * 100.0 / cocktail_count), 1) as simple_percentage,
    ROUND((CAST(intermediate_count AS FLOAT) * 100.0 / cocktail_count), 1) as intermediate_percentage,
    ROUND((CAST(complex_count AS FLOAT) * 100.0 / cocktail_count), 1) as complex_percentage,

    -- Audit
    CAST(GETUTCDATE() AS DATETIME2) as created_at

FROM cocktail_rankings

ORDER BY cocktail_count DESC
