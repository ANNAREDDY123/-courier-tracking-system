from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal, engine, Base
from models import Customer, Package, Shipment, Tracking
from schemas import *

app = FastAPI(title="Courier Tracking System")

Base.metadata.create_all(bind=engine)


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# HOME API
# -----------------------------
@app.get("/")
def home():
    return {"message": "Courier Tracking System Running"}


# -----------------------------
# CUSTOMER APIs
# -----------------------------
@app.post("/customers", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()


@app.put("/customers/{customer_id}")
def update_customer(customer_id: int,
                    customer: CustomerCreate,
                    db: Session = Depends(get_db)):

    db_customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not db_customer:
        raise HTTPException(404, "Customer not found")

    db_customer.name = customer.name
    db_customer.email = customer.email
    db_customer.phone = customer.phone
    db_customer.address = customer.address

    db.commit()

    return {"message": "Customer updated"}


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int,
                    db: Session = Depends(get_db)):

    db_customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not db_customer:
        raise HTTPException(404, "Customer not found")

    db.delete(db_customer)
    db.commit()

    return {"message": "Customer deleted"}


# -----------------------------
# PACKAGE APIs
# -----------------------------
@app.post("/packages", response_model=PackageResponse)
def create_package(package: PackageCreate,
                   db: Session = Depends(get_db)):

    customer = db.query(Customer).filter(
        Customer.id == package.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=400,
            detail="Customer does not exist"
        )

    if package.weight <= 0:
        raise HTTPException(
            status_code=400,
            detail="Weight must be greater than 0"
        )

    db_package = Package(**package.model_dump())

    db.add(db_package)
    db.commit()
    db.refresh(db_package)

    return db_package


@app.get("/packages")
def get_packages(db: Session = Depends(get_db)):
    return db.query(Package).all()


@app.put("/packages/{package_id}")
def update_package(package_id: int,
                   package: PackageCreate,
                   db: Session = Depends(get_db)):

    db_package = db.query(Package).filter(
        Package.id == package_id
    ).first()

    if not db_package:
        raise HTTPException(404, "Package not found")

    db_package.package_name = package.package_name
    db_package.weight = package.weight
    db_package.package_type = package.package_type

    db.commit()

    return {"message": "Package updated"}


@app.delete("/packages/{package_id}")
def delete_package(package_id: int,
                   db: Session = Depends(get_db)):

    package = db.query(Package).filter(
        Package.id == package_id
    ).first()

    if not package:
        raise HTTPException(404, "Package not found")

    db.delete(package)
    db.commit()

    return {"message": "Package deleted"}


# -----------------------------
# SHIPMENT APIs
# -----------------------------
@app.post("/shipments")
def create_shipment(shipment: ShipmentCreate,
                    db: Session = Depends(get_db)):

    package = db.query(Package).filter(
        Package.id == shipment.package_id
    ).first()

    if not package:
        raise HTTPException(404, "Package not found")

    new_shipment = Shipment(
        package_id=shipment.package_id
    )

    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)

    return new_shipment


@app.get("/shipments")
def get_shipments(db: Session = Depends(get_db)):
    return db.query(Shipment).all()


@app.put("/shipments/{shipment_id}")
def update_shipment(shipment_id: int,
                    shipment: ShipmentUpdate,
                    db: Session = Depends(get_db)):

    db_shipment = db.query(Shipment).filter(
        Shipment.id == shipment_id
    ).first()

    if not db_shipment:
        raise HTTPException(404, "Shipment not found")

    if db_shipment.shipment_status == "Delivered":
        raise HTTPException(
            400,
            "Delivered shipment cannot be modified"
        )

    db_shipment.shipment_status = shipment.shipment_status

    if shipment.shipment_status == "Delivered":
        db_shipment.delivered_time = datetime.utcnow()

    db.commit()

    return {"message": "Shipment updated"}


# -----------------------------
# TRACKING APIs
# -----------------------------
@app.post("/tracking")
def create_tracking(tracking: TrackingCreate,
                    db: Session = Depends(get_db)):

    existing = db.query(Tracking).filter(
        Tracking.tracking_id == tracking.tracking_id
    ).first()

    if existing:
        raise HTTPException(
            400,
            "Tracking ID already exists"
        )

    shipment = db.query(Shipment).filter(
        Shipment.id == tracking.shipment_id
    ).first()

    if not shipment:
        raise HTTPException(
            404,
            "Shipment not found"
        )

    new_tracking = Tracking(
        tracking_id=tracking.tracking_id,
        shipment_id=tracking.shipment_id,
        current_location=tracking.current_location
    )

    db.add(new_tracking)
    db.commit()
    db.refresh(new_tracking)

    return new_tracking


@app.get("/tracking/{tracking_id}")
def track_package(tracking_id: str,
                  db: Session = Depends(get_db)):

    tracking = db.query(Tracking).filter(
        Tracking.tracking_id == tracking_id
    ).first()

    if not tracking:
        raise HTTPException(404, "Tracking ID not found")

    return tracking


@app.put("/tracking/{tracking_id}")
def update_tracking(tracking_id: str,
                    tracking_data: TrackingUpdate,
                    db: Session = Depends(get_db)):

    tracking = db.query(Tracking).filter(
        Tracking.tracking_id == tracking_id
    ).first()

    if not tracking:
        raise HTTPException(404, "Tracking ID not found")

    tracking.current_location = tracking_data.current_location
    tracking.updated_time = datetime.utcnow()

    db.commit()

    return {"message": "Tracking updated"}
