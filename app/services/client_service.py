from sqlalchemy.orm import Session
from app.db.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate, ClientOut
from fastapi import HTTPException, Request


def create_client(db: Session, client_in: ClientCreate, user):
    existing_client = db.query(Client).filter(Client.user_id == user.id).first()
    if existing_client:
        raise HTTPException(status_code=400, detail="Usuário já possui um cliente.")

    email_exists = db.query(Client).filter(Client.email == client_in.email).first()
    if email_exists:
        raise HTTPException(
            status_code=400,
            detail="Já existe um cliente cadastrado com este E-mail.",
        )

    client = Client(
        **client_in.model_dump(),
        user_id=user.id
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def list_clients(db: Session, skip: int, limit: int, page: int, request: Request):
    query = db.query(Client).order_by(Client.id)
    total = query.count()
    clients = query.offset(skip).limit(limit).all()

    base_url = str(request.url).split("?")[0]
    query_params = request.query_params.multi_items()
    query_dict = dict(query_params)

    def build_url(new_page: int):
        query_dict["page"] = str(new_page)
        query_dict["limit"] = str(limit)
        params = "&".join(f"{k}={v}" for k, v in query_dict.items())
        return f"{base_url}?{params}"

    next_page = build_url(page + 1) if skip + limit < total else None
    prev_page = build_url(page - 1) if page > 1 else None

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "next_page": next_page,
        "prev_page": prev_page,
        "data": [ClientOut.model_validate(c) for c in clients],
    }

def get_client_by_id(db: Session, client_id: int, user):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    if not user.is_admin and client.user_id != user.id:
        raise HTTPException(status_code=403, detail="Acesso negado a este cliente")
    
    return client

def get_client_by_user(db: Session, user):
    client = db.query(Client).filter(Client.user_id == user.id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado para este usuário")
    return client

def update_client(db: Session, client_id: int, client_in: ClientUpdate, user):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    if not user.is_admin and client.user_id != user.id:
        raise HTTPException(status_code=403, detail="Acesso negado a este cliente")
    
    update_data = client_in.model_dump(exclude_unset=True)

    if "email" in update_data:
        email_exists = (
            db.query(Client)
            .filter(Client.email == client_in.email, Client.id != client_id)
            .first()
        )
        if email_exists:
            raise HTTPException(
                status_code=400,
                detail="Já existe um cliente cadastrado com este E-mail.",
            )

    for field, value in update_data.items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client_id: int, user):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    if not user.is_admin and client.user_id != user.id:
        raise HTTPException(status_code=403, detail="Acesso negado a este cliente")
    
    db.delete(client)
    db.commit()
    return {"detail": "Cliente deletado com sucesso"}
