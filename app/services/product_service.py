import requests
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.db.models.product import Product
from datetime import datetime

FAKESTORE_BASE = "https://fakestoreapi.com/products"


def fetch_product_from_external(external_id: int, timeout: int = 5):
    url = f"{FAKESTORE_BASE}/{external_id}"
    try:
        resp = requests.get(url, timeout=timeout)
    except requests.RequestException as exc:
        raise HTTPException(status_code=503, detail="Erro ao consultar API externa de produtos") from exc

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Produto não encontrado na API externa")
    if resp.status_code != 200:
        raise HTTPException(status_code=503, detail="API externa retornou erro")
    
    if not resp.text.strip():
        raise HTTPException(status_code=404, detail="Produto não encontrado na API externa")

    try:
        return resp.json()
    except ValueError:
        raise HTTPException(status_code=502, detail="Resposta inválida da API externa")


def create_product_from_external(db: Session, external_id: int):
    payload = fetch_product_from_external(external_id)
    product = Product(
        external_id=payload.get("id"),
        title=payload.get("title"),
        image=payload.get("image"),
        price=payload.get("price"),
        description=payload.get("description"),
        category=payload.get("category"),
        rating_rate=(payload.get("rating") or {}).get("rate") if payload.get("rating") else None,
        rating_count=(payload.get("rating") or {}).get("count") if payload.get("rating") else None,
    )
    db.add(product)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        product = db.query(Product).filter(Product.external_id == external_id).first()
        if product is None:
            raise
    else:
        db.refresh(product)

    return product


def get_or_create_product(db: Session, external_id: int):
    product = db.query(Product).filter(Product.external_id == external_id).first()
    if product:
        return product
    return create_product_from_external(db, external_id)
