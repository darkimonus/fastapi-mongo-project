from pydantic import BaseModel, PositiveFloat
from typing import List, Optional, Dict
from datetime import datetime


class NutritionalValue(BaseModel):
    """
    This model describes Nutritional Value of food that is served in related restaurants.
    """
    calories: PositiveFloat
    proteins: PositiveFloat
    fat: PositiveFloat
    carbohydrates: PositiveFloat


class Food(BaseModel):
    name: str
    kind: str
    price: PositiveFloat
    nutritional_value: NutritionalValue
    composition: Optional[Dict[str, PositiveFloat]]


class Restaurant(BaseModel):
    address: str
    city: str
    country: Optional[str]


class Table(BaseModel):
    """
    Represents table at restaurant.
    """
    number: int
    restaurant: Restaurant


class OrderedFood(BaseModel):
    """
    Represents food data that is stored in Order documents.
    """
    name: str
    price: PositiveFloat


class Order(BaseModel):
    table: Table
    food: List[OrderedFood]
    full_price: PositiveFloat
    date: datetime
    grade: Optional[int]
    review: Optional[str]
    payment: Optional[str]
    user_phone_number: Optional[str]


class RestaurantMenu(BaseModel):
    restaurant_id: str
    foods: List[Food]
