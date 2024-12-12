from pydantic import BaseModel, PositiveFloat, EmailStr, HttpUrl
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum
from db.conf import DEFAULT_COUNTRY_CODE

PhoneNumber.phone_format = 'E164'  # 'INTERNATIONAL', 'NATIONAL'
PhoneNumber.default_region_code = DEFAULT_COUNTRY_CODE


class Token(BaseModel):
    access_token: str
    token_type: str


class TableStatusEnum(str, Enum):
    FREE = "free"
    OCCUPIED = "occupied"
    RESERVED = "reserved"


class ReservationStatusEnum(str, Enum):
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PENDING = "pending"


class OrderStatusEnum(str, Enum):
    CREATED = 'created'
    ACCEPTED = 'accepted'
    COOKING = 'cooking'
    DONE = 'done'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'


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
    image_url: Optional[HttpUrl]


class Restaurant(BaseModel):
    address: str
    city: str
    country: Optional[str]
    work_hours: Dict[str, str]


class Table(BaseModel):
    """
    Represents table at restaurant.
    """
    number: int
    restaurant_id: Restaurant
    status: TableStatusEnum


class ReservationTable(BaseModel):
    """
    Represents table at restaurant.
    """
    number: int
    restaurant: Restaurant


class User(BaseModel):
    phone_number: PhoneNumber
    name: Optional[str]
    email: Optional[EmailStr]


class Reservation(BaseModel):
    table_id: str
    restaurant: str
    start_time: datetime
    end_time: datetime
    user_phone_number: str
    status: ReservationStatusEnum


class OrderedFood(BaseModel):
    """
    Represents food data that is stored in Order documents.
    """
    name: str
    price: PositiveFloat


class Order(BaseModel):
    table_id: str
    status: OrderStatusEnum
    food: List[OrderedFood]
    date: datetime
    grade: Optional[int]
    review: Optional[str]
    payment: Optional[str]
    user_phone_number: Optional[str]
    reservation: Optional[str]
    comments: Optional[list]


class RestaurantMenu(BaseModel):
    restaurant_id: str
    foods: List[Food]
