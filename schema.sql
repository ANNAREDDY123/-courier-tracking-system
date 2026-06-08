CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    address TEXT
);

CREATE TABLE packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_name VARCHAR(100),
    weight FLOAT NOT NULL,
    package_type VARCHAR(50),
    customer_id INTEGER,
    FOREIGN KEY (customer_id)
        REFERENCES customers(id)
);

CREATE TABLE shipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER,
    shipment_status VARCHAR(50)
        DEFAULT 'Pending',
    created_time DATETIME,
    delivered_time DATETIME,
    FOREIGN KEY (package_id)
        REFERENCES packages(id)
);

CREATE TABLE tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tracking_id VARCHAR(100) UNIQUE,
    shipment_id INTEGER,
    current_location VARCHAR(255),
    updated_time DATETIME,
    FOREIGN KEY (shipment_id)
        REFERENCES shipments(id)
);
