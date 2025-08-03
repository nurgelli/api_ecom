from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.order import OrderStatus



class ProductInOrder(BaseModel):
    id: int
    name: str
    price: float
    
    class Config:
        from_attributes = True
        
class OrderItemBase(BaseModel):
    product_id: int = Field(..., gt=0, description="The ID of the product in the order.")
    quantity: int = Field(..., gt=0, description="The quantity of the product in the order.")
    price: float = Field(..., ge=0, description="The price of the product at the time of order.")
    
    
class OrderItem(OrderItemBase):
    id: int
    order_id: int
    product: ProductInOrder
    created_at: datetime
    updated_at: Optional[datetime] = None

class OrderCreate(BaseModel):
    pass


class Order(OrderBase):
    id: int
    user_id: int
    total_amount: float
    status: OrderStatus
    order_items: List[OrderItem] = []
    craeted_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True