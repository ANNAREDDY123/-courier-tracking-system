
-- 1. Customers with Highest Shipments


SELECT
    c.id,
    c.name,
    COUNT(s.id) AS shipment_count
FROM customers c
JOIN packages p
    ON c.id = p.customer_id
JOIN shipments s
    ON p.id = s.package_id
GROUP BY c.id, c.name
ORDER BY shipment_count DESC;



-- 2. Total Delivered Packages


SELECT COUNT(*) AS total_delivered_packages
FROM shipments
WHERE shipment_status = 'Delivered';



-- 3. List Pending Shipments


SELECT *
FROM shipments
WHERE shipment_status = 'Pending';



-- 4. Monthly Shipment Report
-- =====================================

SELECT
    strftime('%Y-%m', created_time) AS month,
    COUNT(*) AS total_shipments
FROM shipments
GROUP BY month
ORDER BY month;



-- 5. Average Delivery Time


SELECT
    AVG(
        julianday(delivered_time)
        -
        julianday(created_time)
    ) AS average_delivery_days
FROM shipments
WHERE shipment_status = 'Delivered';


-- =====================================
-- 6. Rank Customers by Shipment Count
-- =====================================

SELECT
    customer_name,
    shipment_count,
    RANK() OVER (
        ORDER BY shipment_count DESC
    ) AS customer_rank
FROM
(
    SELECT
        c.name AS customer_name,
        COUNT(s.id) AS shipment_count
    FROM customers c
    JOIN packages p
        ON c.id = p.customer_id
    JOIN shipments s
        ON p.id = s.package_id
    GROUP BY c.id, c.name
) ranked_customers;
