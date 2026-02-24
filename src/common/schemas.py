"""
Data schemas and validation for Coffeeverse pipeline.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator


class Ingredient(BaseModel):
    """Single cocktail ingredient with measure."""
    name: str
    measure: Optional[str] = ""


class CocktailRaw(BaseModel):
    """Raw cocktail data from TheCocktailDB API (Bronze layer)."""
    idDrink: str
    strDrink: str
    strCategory: str
    strAlcoholic: str
    strGlass: Optional[str] = None
    strInstructions: str
    strDrinkThumb: Optional[str] = None
    
    @validator('idDrink', 'strDrink', 'strCategory', 'strAlcoholic', 'strInstructions')
    def must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v


class CocktailCleaned(BaseModel):
    """Cleaned and enriched cocktail data (Silver layer)."""
    id: str
    name: str
    category: str
    alcoholic: bool
    glass: Optional[str] = None
    instructions: str
    thumbnail_url: Optional[str] = None
    ingredients: List[Ingredient]
    ingredient_count: int = Field(ge=0)
    complexity_score: float = Field(ge=1.0, le=10.0)
    estimated_calories: int = Field(ge=0)
    processed_at: datetime
    source: str = "thecocktaildb"
    version: str = "1.0"
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CocktailAnalytics(BaseModel):
    """Aggregated analytics data (Gold layer)."""
    id: str
    spirit_type: str
    category: str
    avg_complexity: float
    total_cocktails: int
    avg_calories: float
    alcoholic_pct: float
    popular_glass: str
    generated_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
