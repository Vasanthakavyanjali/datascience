# KPI Definitions

**Project:** E-Commerce Sales Performance & Customer Analytics
**Version:** 1.0

This document defines every KPI used in the dashboard. Use these formulas to ensure consistency across reports, meetings, and documentation.

---

## 1. Financial KPIs

### 1.1 Total Sales

**Definition:** Sum of all net sales values.

**Formula:** gross_sales = quantity × unit_price


**Unit:** Currency (₹)
**Source columns:** `quantity`, `unit_price`

---

### 1.3 Discount Amount

**Definition:** Money value of discount given.

**Formula:**  discount_amount = gross_sales × discount / 100


**Unit:** Currency (₹)
**Source columns:** `gross_sales`, `discount`

---

### 1.4 Net Sales

**Definition:** Sales after discount.

**Formula:**  net_sales = gross_sales − discount_amount


**Unit:** Currency (₹)

---

## 2. Volume KPIs

### 2.1 Total Orders

**Definition:** Count of unique orders.

**Formula:**  total_orders = COUNT(DISTINCT order_id)


**Unit:** Count

---

### 2.2 Total Customers

**Definition:** Count of unique customers.

**Formula:**  total_customers = COUNT(DISTINCT customer_id)


**Unit:** Count

---

### 2.3 Total Units Sold

**Definition:** Sum of quantities across all orders.

**Formula:**  total_units = SUM(quantity)


**Unit:** Count

---

## 3. Averages

### 3.1 Average Order Value (AOV)

**Definition:** Average net revenue per unique order.

**Formula:**  AOV = total_sales / total_orders


**Unit:** Currency (₹)

---

### 3.2 Median Order Value

**Definition:** Middle order value when sorted.

**Formula:**  median_order_value = MEDIAN(SUM(sales) GROUP BY order_id)


**Unit:** Currency (₹)

---

### 3.3 Average Customer Spend

**Definition:** Average total spend per customer.

**Formula:**  avg_customer_spend = SUM(sales) / COUNT(DISTINCT customer_id)


**Unit:** Currency (₹)

---

## 4. Statistical KPIs

| KPI | Meaning |
|-----|---------|
| Mean | Arithmetic average |
| Median | Middle value |
| Mode | Most frequent value |
| Variance | Average squared deviation from mean |
| Standard Deviation | Square root of variance |
| Q1 | 25th percentile |
| Q2 | Median (50th percentile) |
| Q3 | 75th percentile |
| IQR | Q3 − Q1 |

**Outlier bounds (Tukey's rule):**
 lower_bound = Q1 − 1.5 × IQR
 upper_bound = Q3 + 1.5 × IQR


Any value outside these bounds is flagged as a **potential outlier**.

---

## 5. Relationship KPIs

### 5.1 Correlation

**Definition:** Pearson correlation coefficient between two numeric columns.
**Range:** −1 to +1

| Absolute value | Strength |
|----------------|----------|
| ≥ 0.80 | Very strong |
| ≥ 0.60 | Strong |
| ≥ 0.40 | Moderate |
| ≥ 0.20 | Weak |
| < 0.20 | Little / none |

**Important:** Correlation does not imply causation.

### 5.2 Covariance

**Definition:** A measure of how two variables vary together. Its magnitude depends on the units of the variables, so correlation is easier to interpret.

---

## 6. Customer Segmentation

Customers are segmented into three groups based on their **total spend**:

| Segment | Definition |
|---------|------------|
| Low Value | Bottom 25% (≤ Q1) |
| Medium Value | Middle 50% (Q1–Q3) |
| High Value | Top 25% (> Q3) |

---

## 7. KPI Summary Table

| KPI | Formula | Unit |
|-----|---------|------|
| Total Sales | SUM(sales) | ₹ |
| Gross Sales | quantity × unit_price | ₹ |
| Discount Amount | gross × discount / 100 | ₹ |
| Net Sales | gross − discount | ₹ |
| Total Orders | COUNT(DISTINCT order_id) | Count |
| Total Customers | COUNT(DISTINCT customer_id) | Count |
| Total Units | SUM(quantity) | Count |
| AOV | total_sales / total_orders | ₹ |
| Median Order Value | median of order totals | ₹ |
| Avg Customer Spend | total_sales / customers | ₹ |
| IQR | Q3 − Q1 | ₹ |
| Outlier Bounds | Q1 − 1.5×IQR; Q3 + 1.5×IQR | ₹ |
| Correlation | Pearson r | −1 to 1 |




 


