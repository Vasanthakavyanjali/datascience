# Final Presentation — Outline

**Project:** E-Commerce Sales Performance & Customer Analytics
**Role:** Business Analyst
**Slides:** ~15
**Duration:** 15 minutes

---

## Slide 1 — Title

**E-Commerce Sales Analytics**

Transforming transaction data into business decisions

*Analyst name*
*Date*

---

## Slide 2 — Business Problem

- Thousands of orders per month
- Management cannot answer key questions quickly
- No single source of truth for KPIs
- Data-quality issues go unnoticed
- Outliers may distort averages

---

## Slide 3 — Objective

Build a single dashboard that:

- Answers the top 10 business questions
- Calculates KPIs dynamically
- Validates and cleans the data
- Detects anomalies
- Provides downloadable results

---

## Slide 4 — Data Source

Schema overview:
order_id, order_date, customer_id, product_id, product_name,
category, region, quantity, unit_price, discount, sales


Data quality rules applied:

- Quantity ≥ 1
- Price > 0
- Discount 0–100
- Valid dates
- Unique order IDs

---

## Slide 5 — Approach
Raw Data
↓
Validation
↓
Cleaning
↓
Transformation
↓
Statistics
↓
KPIs
↓
Dashboard
↓
Insights
↓
Recommendations

---

## Slide 6 — KPIs Delivered

| KPI | Meaning |
|-----|---------|
| Total Sales | Total revenue |
| Orders | Unique order count |
| Customers | Unique buyers |
| Units Sold | Total items |
| Average Order Value | Spend per order |
| Median Order Value | Middle order value |

---

## Slide 7 — Sales Insights

- Sales trend over time
- Top categories
- Top regions
- Weak regions

*(Insert screenshot of Dashboard page)*

---

## Slide 8 — Customer Insights

- Average spending per customer
- Top 10 spenders
- Low / Medium / High segments
- Repeat vs one-time buyers

*(Insert screenshot of Customer page)*

---

## Slide 9 — Product Insights

- Top 10 products by revenue
- Low-performing products
- Category performance

*(Insert screenshot of Products page)*

---

## Slide 10 — Statistical Analysis

- Mean, median, mode
- Variance, standard deviation
- Q1, Q2, Q3, IQR
- Outlier bounds: Q1 − 1.5×IQR and Q3 + 1.5×IQR
- Correlation between discount and sales

*(Insert screenshot of Statistics page)*

---

## Slide 11 — Data Quality

- Missing value report
- Duplicate order check
- Invalid values detected
- Rows excluded from analysis

*(Insert screenshot of Data Quality page)*

---

## Slide 12 — Key Business Insights

- Top category accounts for X% of revenue
- Region A leads, Region B lags
- Average >> median → outliers present
- Discount shows moderate/strong correlation with sales

*(These sentences should come from the actual data.)*

---

## Slide 13 — Recommendations

- Review inventory for top categories
- Investigate low-performing regions
- Verify outlier transactions
- Encourage repeat purchases via loyalty program

---

## Slide 14 — What We Did NOT Do (and Why)

To keep v1 focused:

- No machine learning
- No forecasting
- No cloud deployment
- No authentication

These belong in future phases.

---

## Slide 15 — Resume / Project Pitch

> "I built an end-to-end analytics solution: defined KPIs, validated and cleaned transactional data, performed statistical analysis (mean, median, variance, IQR, correlation), and delivered an interactive Streamlit dashboard with filters, outlier detection, and downloadable reports."

---

## Backup Slides

- Detailed column definitions
- Full KPI dictionary
- Data pipeline diagram
- Screenshots of all pages