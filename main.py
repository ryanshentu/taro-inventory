import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# fallback
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL is missing! Check your .env file or Render settings.")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class IngredientDB(Base):
    __tablename__ = "inventory"  
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)
    unit = Column(String)
    threshold = Column(Integer)

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class IngredientCreate(BaseModel):
    name: str
    quantity: int
    unit: str
    threshold: int

class Sale(BaseModel):
    name: str  
    amount_used: int

@app.post("/ingredients")
def add_ingredient(item: IngredientCreate, db: Session = Depends(get_db)):
    db_item = IngredientDB(
        name=item.name, 
        quantity=item.quantity, 
        unit=item.unit, 
        threshold=item.threshold
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/inventory")
def get_inventory(db: Session = Depends(get_db)):
    return db.query(IngredientDB).all()

@app.post("/sale")
def record_sale(sale: Sale, db: Session = Depends(get_db)):
    item = db.query(IngredientDB).filter(IngredientDB.name == sale.name).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.quantity -= sale.amount_used
    db.commit() 
    
    alert = None
    if item.quantity < item.threshold:
        alert = f"⚠️ LOW STOCK WARNING: {item.name} is below {item.threshold} {item.unit}!"

    return {
        "status": "success", 
        "remaining": item.quantity,
        "alert": alert
    }