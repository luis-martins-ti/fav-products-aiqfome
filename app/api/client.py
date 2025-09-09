from fastapi import APIRouter, Depends, Query, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.auth.deps import get_db, get_current_user
from app.schemas.client import ClientCreate, ClientUpdate, ClientOut
from app.services.client_service import (
    create_client,
    list_clients,
    get_client_by_id,
    get_client_by_user,
    update_client,
    delete_client,
)
from app.schemas.favorite_product import FavoriteCreate, FavoriteOut
from app.services.favorite_service import (
    add_favorite_for_client,
    list_favorites_for_client,
    remove_favorite_for_client,
)

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/", response_model=ClientOut)
def add_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return create_client(db, client_in, user)


@router.get("/", response_model=dict)
def get_clients(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    request: Request = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    if not user.is_admin:
        raise HTTPException(
            status_code=403, detail="Acesso negado. Listagem de clientes disponível apenas para administradores."
        )
    
    skip = (page - 1) * limit
    return list_clients(db=db, skip=skip, limit=limit, page=page, request=request)


@router.get("/{client_id}", response_model=ClientOut)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_client_by_id(db, client_id, user)


@router.put("/{client_id}", response_model=ClientOut)
def edit_client(
    client_id: int,
    client_in: ClientUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return update_client(db, client_id, client_in, user)


@router.patch("/{client_id}", response_model=ClientOut)
def patch_client(
    client_id: int,
    client_in: ClientUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return update_client(db, client_id, client_in, user)


@router.delete("/{client_id}", status_code=204)
def remove_client(
    client_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    delete_client(db, client_id, user)
    return None

@router.post("/me/favorites", response_model=FavoriteOut, status_code=201)
def add_my_favorite(
    payload: FavoriteCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    client = get_client_by_user(db, user)
    fav = add_favorite_for_client(db, client, payload.external_id)
    return fav

@router.get("/me/favorites", response_model=list[FavoriteOut])
def get_my_favorites(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    client = get_client_by_user(db, user)
    favs = list_favorites_for_client(db, client)
    return favs

# admin: listar favoritos de um cliente específico
@router.get("/{client_id}/favorites", response_model=list[FavoriteOut])
def get_client_favorites(
    client_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado a este recurso")
    client = get_client_by_id(db, client_id, user)
    favs = list_favorites_for_client(db, client)
    return favs


@router.delete("/me/favorites/{external_id}", status_code=204)
def delete_my_favorite(
    external_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    client = get_client_by_user(db, user)
    remove_favorite_for_client(db, client, external_id)
    return None