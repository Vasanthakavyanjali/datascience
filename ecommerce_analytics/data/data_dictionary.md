# Data Dictionary

**Dataset:** E-Commerce Transactions
**File:** `data/ecommerce_data.csv`
**Format:** CSV (UTF-8)
**Primary key:** `order_id`

---

## 1. Source Columns

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| order_id | String | Unique order identifier | ORD1001 |
| order_date | Date | Date of order (YYYY-MM-DD) | 2026-01-05 |
| customer_id | String | Unique customer identifier | C1001 |
| product_id | String | Product identifier | P2001 |
| product_name | String | Product name | Wireless Mouse |
| category | String | Product category | Electronics |
| region | String | Customer region | North |
| quantity | Integer | Units ordered (≥ 1) | 2 |
| unit_price | Decimal | Price per unit (₹) | 799.00 |
| discount | Decimal | Discount % (0–100) | 10 |
| sales | Decimal | Net sales amount (₹) | 1438.20 |

---

## 2. Derived Columns (added by cleaning)

| Column | Data Type | Description | Formula |
|--------|-----------|-------------|---------|
| gross_sales | Decimal | Sales before discount | quantity × unit_price |
| discount_amount | Decimal | Money value of discount | gross_sales × discount / 100 |
| net_sales | Decimal | Sales after discount | gross_sales − discount_amount |
| order_year | Integer | Year of order | year(order_date) |
| order_month | Integer | Month number (1–12) | month(order_date) |
| order_month_name | String | Month name (Jan, Feb, ...) | month_abbrev(order_date) |

---

## 3. Data Quality Rules

| Rule | Condition |
|------|-----------|
| Order ID required | `order_id` must not be null |
| Customer ID required | `customer_id` must not be null |
| Order date required | `order_date` must parse as a valid date |
| Quantity valid | `quantity ≥ 1` |
| Unit price valid | `unit_price > 0` |
| Discount valid | `0 ≤ discount ≤ 100` |
| Sales required | `sales` must not be null |
| No duplicates | `order_id` must be unique |

Rows that fail any rule are flagged in the **Data Quality** page and excluded from the cleaned dataset.

---

## 4. Example Row

```csv
ORD1001,2026-01-05,C1001,P2001,Wireless Mouse,Electronics,North,2,799,10,1438.20