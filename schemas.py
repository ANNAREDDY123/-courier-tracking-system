from pydantic import BaseModel
from datetime import datetime


# --------------------------------
# CUSTOMER SCHEMAS
# --------------------------------

class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str
    address: str


class CustomerResponse(CustomerCreate):
    id: int

    class Config:
        from_attributes = True


# --------------------------------
# PACKAGE SCHEMAS
# --------------------------------

class PackageCreate(BaseModel):
    package_name: str
    weight: float
    package_type: str
    customer_id: int


class PackageResponse(PackageCreate):
    id: int

    class Config:
        from_attributes = True


# --------------------------------
# SHIPMENT SCHEMAS
# --------------------------------

class ShipmentCreate(BaseModel):
    package_id: int


class ShipmentUpdate(BaseModel):
    shipment_status: str


class ShipmentResponse(BaseModel):
    id: int
    package_id: int
    shipment_status: str

    class Config:
        from_attributes = True


# --------------------------------
# TRACKING SCHEMAS
# --------------------------------

class TrackingCreate(BaseModel):
    tracking_id: str
    shipment_id: int
    current_location: str


class TrackingUpdate(BaseModel):
    current_location: str


class TrackingResponse(BaseModel):
    id: int
    tracking_id: str
    shipment_id: int
    current_location: str
    updated_time: datetime

    class Config:
        from_attributes = True
