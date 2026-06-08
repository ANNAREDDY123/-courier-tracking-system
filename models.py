from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship

from database import Base

from datetime import datetime


# -----------------------------
# CUSTOMER TABLE
# -----------------------------

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String)
    address = Column(String)

    packages = relationship(
        "Package",
        back_populates="customer"
    )


# -----------------------------
# PACKAGE TABLE
# -----------------------------

class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)

    package_name = Column(String)
    weight = Column(Float)
    package_type = Column(String)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    customer = relationship(
        "Customer",
        back_populates="packages"
    )

    shipment = relationship(
        "Shipment",
        back_populates="package",
        uselist=False
    )


# -----------------------------
# SHIPMENT TABLE
# -----------------------------

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)

    package_id = Column(
        Integer,
        ForeignKey("packages.id")
    )

    shipment_status = Column(
        String,
        default="Pending"
    )

    created_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    delivered_time = Column(
        DateTime,
        nullable=True
    )

    package = relationship(
        "Package",
        back_populates="shipment"
    )

    tracking = relationship(
        "Tracking",
        back_populates="shipment",
        uselist=False
    )


# -----------------------------
# TRACKING TABLE
# -----------------------------

class Tracking(Base):
    __tablename__ = "tracking"

    id = Column(Integer, primary_key=True, index=True)

    tracking_id = Column(
        String,
        unique=True
    )

    shipment_id = Column(
        Integer,
        ForeignKey("shipments.id")
    )

    current_location = Column(String)

    updated_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    shipment = relationship(
        "Shipment",
        back_populates="tracking"
    )
