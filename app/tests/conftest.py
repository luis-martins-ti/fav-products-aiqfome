import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.db.database import SessionLocal, Base, engine
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user(db_session):
    username = "testuser"
    password = "123456"
    existing = db_session.query(User).filter(User.username == username).first()
    if existing:
        return existing
    user = User(username=username, hashed_password=hash_password(password))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(client, test_user):
    response = client.post(
        "/auth/token", data={"username": "testuser", "password": "123456"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
