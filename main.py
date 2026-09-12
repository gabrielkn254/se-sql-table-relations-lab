# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""
    SELECT firstName, lastName
    FROM employees
    WHERE officeCode IN (
        SELECT officeCode
        FROM offices
        WHERE city = "Boston"
    )
""", conn)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""
    SELECT offices.*
    FROM offices
    LEFT JOIN employees USING(officeCode)
    WHERE employees.officeCode IS NULL

""", conn)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o USING(officeCode)
    ORDER BY e.firstName ASC
""", conn)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""
    SELECT 
        c.contactFirstName,
        c.contactLastName,
        c.phone,
        c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o USING(customerNumber)
    WHERE o.customerNumber IS NULL
    ORDER BY c.contactLastName ASC
""", conn)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""
    SELECT 
        c.contactFirstName,
        c.contactLastName,
        p.paymentDate,
        p.amount
    FROM customers c
    JOIN payments p USING(customerNumber)
    ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql("""
    SELECT 
        e.employeeNumber,
        e.firstName,
        e.lastName,
        COUNT(c.customerNumber) AS numberOfCustomers
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY numberOfCustomers DESC
    LIMIT 4
""", conn)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""
    SELECT 
        p.productName,
        COUNT(od.orderNumber) AS numorders,
        SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od USING(productCode)
    GROUP BY p.productCode, p.productName
    ORDER BY totalunits DESC
""", conn)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""
    SELECT 
        p.productCode,
        p.productName,
        COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode, p.productName
    ORDER BY numpurchasers DESC
""", conn)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""
    SELECT 
        o.officeCode,
        o.city,
        COUNT(DISTINCT c.customerNumber) AS n_customers
    FROM offices o
    JOIN employees e ON o.officeCode = e.officeCode
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
    ORDER BY o.officeCode
""", conn)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql("""
WITH UnderperformingProducts AS (
        SELECT od.productCode
        FROM orderdetails od
        JOIN orders o ON od.orderNumber = o.orderNumber
        GROUP BY od.productCode
        HAVING COUNT(DISTINCT o.customerNumber) < 20
    )
    SELECT DISTINCT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        o.city,
        o.officeCode
    FROM UnderperformingProducts up
    JOIN orderdetails od ON up.productCode = od.productCode
    JOIN orders ord ON od.orderNumber = ord.orderNumber
    JOIN customers c ON ord.customerNumber = c.customerNumber
    JOIN employees e ON c.salesRepEmployeeNumber = e.employeeNumber
    JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.lastName, e.firstName;
""", conn)

conn.close()