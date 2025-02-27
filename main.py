from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from sqlalchemy.orm import Session
from models import Product, Service, SessionLocal

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dariusmumbere.github.io"],  # Allows all origins (replace "*" with your frontend URL for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/")
def create_product(name: str, type: str, buying_price: float, selling_price: float, db: Session = Depends(get_db)):
    db_product = Product(name=name, type=type, buying_price=buying_price, selling_price=selling_price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/")
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.post("/services/")
def create_service(name: str, description: str, price: float, db: Session = Depends(get_db)):
    db_service = Service(name=name, description=description, price=price)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@app.get("/services/")
def read_services(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    services = db.query(Service).offset(skip).limit(limit).all()
    return services
