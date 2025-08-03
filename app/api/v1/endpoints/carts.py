from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.schemas.cart import Cart, CartItem, CartItemCreate, CartItemUpdate
from app.models.cart import Cart as DBCart, CartItem as DBCartItem
from app.models.product import Product as DBProduct
from app.models.user import User as DBUser
from app.api.deps import get_db, get_current_active_user



router = APIRouter()


def get_user_cart(db: Session, user_id: int) -> DBCart:
    cart = db.query(DBCart).filter(DBCart.user_id == user_id).first()
    if not cart:
        cart = DBCart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart
    
@router.get("/", response_model=Cart)
def read_cart(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)   
) -> Any:
    
    cart = db.query(DBCart)\
            .options(joinedload(DBCart.cart_items).joinedload(DBCartItem.product))\
            .filter(DBCart.user_id == current_user.id)\
            .first()
    
    if not cart:
        cart = get_user_cart(db, current_user.id)
        db.refresh(cart)
        return cart
    
    return cart
@router.post("/items/", response_model=Cart)
def add_item_to_cart(
    *,
    db: Session = Depends(get_db),
    cart_item_in: CartItemCreate,
    current_user: DBUser = Depends(get_current_active_user)
) -> Any:
    
    cart = get_user_cart(db, current_user.id)
    
    product = db.query(DBProduct).filter(DBProduct.id == cart_item_in.product_id).first()
    if not product or not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or is not active"
        )
        
    existing_item = db.query(DBCartItem).filter(
        DBCartItem.cart_id == cart.id,
        DBCartItem.product_id == cart_item_in.product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += cart_item_in.quantity
        db.add(existing_item)
        db.commit()
        db.refresh(existing_item)
    else:
        new_item = DBCartItem(
            cart_id=cart.id,
            product_id=cart_item_in.product_id,
            quantity=cart_item_in.quantity
        )
        
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        
        
    updated_cart = db.query(DBCart)\
                    .options(joinedload(DBCart.cart_items).joinedload(DBCartItem.product))\
                    .filter(DBCart.id == cart.id)\
                    .first()
    return updated_cart

@router.put("items/{item_id}", response_model=Cart)
def update_cart_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    cart_item_update: CartItemUpdate,
    current_user: DBUser = Depends(get_current_active_user)
) -> Any:
    
    cart = get_user_cart(db, current_user.id)
    
    cart_item = db.query(DBCartItem).filter(
        DBCartItem.id == item_id,
        DBCartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Cart item not found in your cart'
        )

    if cart_item_update.quantity is not None:
        if cart_item_update.quantity <= 0:
            db.delete(cart_item)
            db.commit()
        else:
            cart_item.quantity = cart_item_update.quantity
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be provided for update"
        )
        
    updated_cart = db.query(DBCart)\
                    .options(joinedload(DBCart.cart_items).joinedload(DBCartItem.product))\
                    .filter(DBCart.id == cart.id)\
                    .first()
    return updated_cart

@router.delete("/items/{item_id}")
def remove_item_from_cart(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: DBUser = Depends(get_current_active_user)
) -> Any:
    cart = get_user_cart(db, current_user.id)
    
    cart_item = db.query(DBCartItem).filter(
        DBCartItem.id == item_id,
        DBCartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found in your cart."
        )
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed successfully"}