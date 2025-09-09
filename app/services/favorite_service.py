from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.db.models.product import Product
from app.db.models.favorite_product import FavoriteProduct
from app.db.models.client import Client
from app.services.product_service import get_or_create_product


def add_favorite_for_client(db: Session, client: Client, external_id: int):
    product = get_or_create_product(db, external_id)

    existing = db.query(FavoriteProduct).filter(
        FavoriteProduct.client_id == client.id,
        FavoriteProduct.product_id == product.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Produto já está nos favoritos deste cliente")

    fav = FavoriteProduct(client_id=client.id, product_id=product.id)
    db.add(fav)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Produto já está nos favoritos deste cliente")
    db.refresh(fav)
    fav.product = product
    return fav


def list_favorites_for_client(db: Session, client: Client):
    favs = (
        db.query(FavoriteProduct)
        .options(joinedload(FavoriteProduct.product))
        .filter(FavoriteProduct.client_id == client.id)
        .all()
    )
    return favs


def remove_favorite_for_client(db: Session, client: Client, external_id: int):
    
    product = db.query(Product).filter(Product.external_id == external_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    fav = db.query(FavoriteProduct).filter(
        FavoriteProduct.client_id == client.id,
        FavoriteProduct.product_id == product.id
    ).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Produto não está nos favoritos")
    db.delete(fav)
    db.commit()
    return {"detail": "Removido"}
