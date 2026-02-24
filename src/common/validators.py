"""
Data validation utilities for Coffeeverse pipeline.
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


def validate_cocktail_data(data: Dict[str, Any]) -> bool:
    """
    Validate raw cocktail data from API.
    
    Args:
        data: Raw cocktail dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = [
        "idDrink",
        "strDrink", 
        "strCategory",
        "strAlcoholic",
        "strInstructions"
    ]
    
    for field in required_fields:
        if not data.get(field):
            logger.warning(f"Missing or empty required field: {field}")
            return False
    
    return True


def calculate_complexity_score(ingredient_count: int, instruction_length: int) -> float:
    """
    Calculate cocktail complexity score (1-10).
    
    Args:
        ingredient_count: Number of ingredients
        instruction_length: Length of instructions in characters
        
    Returns:
        Complexity score between 1.0 and 10.0
    """
    # Base score from ingredient count
    if ingredient_count <= 3:
        base_score = ingredient_count
    elif ingredient_count <= 6:
        base_score = 3 + (ingredient_count - 3) * 1.0
    else:
        base_score = 6 + min(ingredient_count - 6, 4) * 1.0
    
    # Adjust for instruction complexity
    if instruction_length > 500:
        base_score += 1.0
    elif instruction_length > 300:
        base_score += 0.5
    
    return min(max(base_score, 1.0), 10.0)


def estimate_calories(ingredients: List[Dict[str, str]]) -> int:
    """
    Estimate cocktail calories based on ingredients.
    
    Args:
        ingredients: List of ingredient dictionaries with name and measure
        
    Returns:
        Estimated calories as integer
    """
    calorie_map = {
        'vodka': 100,
        'rum': 100,
        'gin': 100,
        'whiskey': 100,
        'bourbon': 100,
        'tequila': 100,
        'liqueur': 150,
        'triple sec': 150,
        'juice': 50,
        'lime': 10,
        'lemon': 10,
        'sugar': 50,
        'syrup': 100,
        'cream': 100,
    }
    
    total_calories = 0
    
    for ingredient in ingredients:
        name = ingredient.get('name', '').lower()
        
        for key, cal in calorie_map.items():
            if key in name:
                # Rough estimate: assume 1 oz per ingredient
                total_calories += cal
                break
        else:
            # Unknown ingredient, add minimal calories
            total_calories += 20
    
    return max(total_calories, 50)  # Minimum 50 calories


def parse_ingredients(data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Parse ingredients and measures from raw cocktail data.
    
    Args:
        data: Raw cocktail dictionary
        
    Returns:
        List of ingredient dictionaries
    """
    ingredients = []
    
    for i in range(1, 16):  # API has up to 15 ingredients
        ingredient_key = f"strIngredient{i}"
        measure_key = f"strMeasure{i}"
        
        ingredient = data.get(ingredient_key)
        measure = data.get(measure_key, "")
        
        if ingredient and ingredient.strip():
            ingredients.append({
                "name": ingredient.strip(),
                "measure": measure.strip() if measure else ""
            })
    
    return ingredients
