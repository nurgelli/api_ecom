from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint
from app.db.base import Base

class Cart(Base):
    __tablename__ = 'carts'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    user = relationship("User", back_populates='cart')
    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    
class CartItem(Base):
    __tablename__ = 'cart_items'
    
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    cart = relationship("Cart", back_populates='cart_items')
    product = relationship("Product")
    __table_args__ = (
        UniqueConstraint('cart_id', 'product_id', name='_cart_product_uc'),
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    
    
    