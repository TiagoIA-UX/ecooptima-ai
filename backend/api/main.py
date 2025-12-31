from .external_services import convert_currency, validate_carbon_credit
@app.get("/currency/convert")
def currency_convert(amount: float, from_currency: str, to_currency: str, current_user: User = Depends(get_current_user)):
    api_key = os.getenv("EXCHANGE_API_KEY", "SUA_API_KEY_AQUI")
    result = convert_currency(amount, from_currency, to_currency, api_key)
    if result is None:
        raise HTTPException(status_code=400, detail="Falha na conversão de moeda")
    return {"amount": result, "currency": to_currency}

@app.post("/carbon/validate")
def carbon_validate(credit_id: int, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    credit = db.query(CarbonCredit).filter(CarbonCredit.id == credit_id).first()
    if not credit:
        raise HTTPException(status_code=404, detail="Crédito não encontrado")
    status = validate_carbon_credit(credit_id)
    credit.verified = status
    db.commit()
    return {"credit_id": credit_id, "verified": status}
from backend.data.carbon_models import CarbonCredit, CarbonTransaction
# Endpoint para listar créditos disponíveis
@app.get("/carbon/credits")
def list_credits(db=Depends(get_db)):
    credits = db.query(CarbonCredit).filter(CarbonCredit.status == "disponível").all()
    return [
        {"id": c.id, "owner_id": c.owner_id, "amount": c.amount, "price": c.price, "status": c.status, "created_at": c.created_at} for c in credits
    ]

# Endpoint para criar crédito de carbono (venda)
@app.post("/carbon/credits")
def create_credit(data: dict = Body(...), current_user: User = Depends(get_current_user), db=Depends(get_db)):
    amount = data.get("amount")
    price = data.get("price")
    if not amount or not price:
        raise HTTPException(status_code=400, detail="amount e price obrigatórios")
    credit = CarbonCredit(owner_id=current_user.id, amount=amount, price=price)
    db.add(credit)
    db.commit()
    db.refresh(credit)
    return {"id": credit.id, "amount": credit.amount, "price": credit.price, "status": credit.status}

# Endpoint para comprar crédito de carbono
@app.post("/carbon/buy")
def buy_credit(data: dict = Body(...), current_user: User = Depends(get_current_user), db=Depends(get_db)):
    credit_id = data.get("credit_id")
    credit = db.query(CarbonCredit).filter(CarbonCredit.id == credit_id, CarbonCredit.status == "disponível").first()
    if not credit:
        raise HTTPException(status_code=404, detail="Crédito não disponível")
    # Marcar como vendido
    credit.status = "vendido"
    db.commit()
    # Registrar transação
    transaction = CarbonTransaction(
        buyer_id=current_user.id,
        seller_id=credit.owner_id,
        credit_id=credit.id,
        amount=credit.amount,
        price=credit.price
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return {"transaction_id": transaction.id, "credit_id": credit.id, "amount": credit.amount, "price": credit.price}

# Endpoint para consultar transações do usuário
@app.get("/carbon/transactions")
def list_transactions(current_user: User = Depends(get_current_user), db=Depends(get_db)):
    txs = db.query(CarbonTransaction).filter(
        (CarbonTransaction.buyer_id == current_user.id) | (CarbonTransaction.seller_id == current_user.id)
    ).all()
    return [
        {"id": t.id, "buyer_id": t.buyer_id, "seller_id": t.seller_id, "credit_id": t.credit_id, "amount": t.amount, "price": t.price, "timestamp": t.timestamp} for t in txs
    ]
from .integrations import get_weather, get_carbon_offset
import os
@app.get("/weather")
def weather(city: str, country: str, current_user: User = Depends(get_current_user)):
    api_key = os.getenv("OPENWEATHER_API_KEY", "SUA_API_KEY_AQUI")
    data = get_weather(city, country, api_key)
    if not data:
        raise HTTPException(status_code=400, detail="Não foi possível obter dados do clima")
    return data

@app.get("/carbon")
def carbon(country: str, value: float, current_user: User = Depends(get_current_user)):
    return get_carbon_offset(country, value)
from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from backend.models.model_stub import EnergyPredictor
from backend.data.db import SessionLocal
from backend.data.models import User, EnergyRecord
import numpy as np
from passlib.context import CryptContext
from jose import JWTError, jwt
import datetime

app = FastAPI()

SECRET_KEY = "ecooptima_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

model = EnergyPredictor()
# Simulação de treinamento inicial
X_train = np.array([[1],[2],[3],[4],[5]])
y_train = np.array([10, 20, 30, 40, 50])
model.train(X_train, y_train)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
def read_root():
    return {"message": "EcoOptima AI Backend rodando!"}

@app.post("/register")
def register_user(data: dict = Body(...), db=Depends(get_db)):
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="Usuário e senha obrigatórios")
    hashed_password = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return {"id": user.id, "username": user.username}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}

@app.post("/energy")
def add_energy_record(data: dict = Body(...), current_user: User = Depends(get_current_user), db=Depends(get_db)):
    value = data.get("value")
    if value is None:
        raise HTTPException(status_code=400, detail="value obrigatório")
    record = EnergyRecord(user_id=current_user.id, value=value)
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"id": record.id, "user_id": record.user_id, "value": record.value, "timestamp": record.timestamp}

@app.get("/energy")
def list_energy_records(current_user: User = Depends(get_current_user), db=Depends(get_db)):
    records = db.query(EnergyRecord).filter(EnergyRecord.user_id == current_user.id).all()
    return [
        {"id": r.id, "user_id": r.user_id, "value": r.value, "timestamp": r.timestamp} for r in records
    ]

@app.post("/predict")
def predict_energy(data: dict = Body(...), current_user: User = Depends(get_current_user)):
    # Espera: { "values": [6, 7, 8] }
    values = np.array(data["values"]).reshape(-1, 1)
    prediction = model.predict(values)
    return {"prediction": prediction.tolist()}
