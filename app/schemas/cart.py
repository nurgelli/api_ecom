from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProductInCart(BaseModel):
    id: int
    name: str
    price: float
    
    class Config:
        from_attributes = True
        
class CartItemBase(BaseModel):
    product_id: int = Field(..., gt=0, description="The ID of the product to add to cart")
    quantity: int = Field(1, gt=0, description="The quantity of the product")
    

class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(CartItemBase):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    

class CartItem(CartItemBase):
    id: int 
    cart_id: int
    product: ProductInCart
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config: 
        from_attributes = True
        
class CartBase(BaseModel):
    pass


class Cart(BaseModel):
    id: int
    user_id: int
    cart_items: List[CartItem] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
