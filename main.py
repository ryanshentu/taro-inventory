from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi.middleware.cors import CORSMiddleware

# 1. DATABASE SETUP
# This URL connects to your local Postgres server.
# Format: postgresql://user:password@localhost/dbname
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Lin19120@taro-db.cxemks0mavmy.us-east-2.rds.amazonaws.com/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. DEFINE THE SQL TABLE (The Schema)
class IngredientDB(Base):
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)
    unit = Column(String)
    threshold = Column(Integer)

# Create the tables automatically
Base.metadata.create_all(bind=engine)

# 3. INITIALIZE FASTAPI
app = FastAPI()

# Allow React to talk to this API
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # uses the list above
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. DATA MODELS (Pydantic - for validation)
class IngredientCreate(BaseModel):
    name: str
    quantity: int
    unit: str
    threshold: int

class Sale(BaseModel):
    name: str  # We will search by name
    amount_used: int

# 5. ENDPOINTS

@app.post("/ingredients")
def add_ingredient(item: IngredientCreate, db: Session = Depends(get_db)):
    # Create the new item
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
    # SQL Translation: SELECT * FROM ingredients;
    return db.query(IngredientDB).all()

@app.post("/sale")
def record_sale(sale: Sale, db: Session = Depends(get_db)):
    # 1. Find the item in the DB
    # SQL Translation: SELECT * FROM ingredients WHERE name = '...' LIMIT 1;
    item = db.query(IngredientDB).filter(IngredientDB.name == sale.name).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # 2. Update Quantity
    item.quantity -= sale.amount_used
    db.commit() # Save changes permanently
    
    # 3. Check Logic
    alert = None
    if item.quantity < item.threshold:
        alert = f"⚠️ LOW STOCK WARNING: {item.name} is below {item.threshold} {item.unit}!"

    return {
        "status": "success", 
        "remaining": item.quantity,
        "alert": alert
    }