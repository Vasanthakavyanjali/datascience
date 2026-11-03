# Data Quality Report

**Project:** E-Commerce Sales Performance & Customer Analytics

**Version:** 1.0

**Report Type:** Data Quality Assessment

**Prepared by:** Business Analyst

**Date:** 2026

---

## 1. Purpose

This report documents the quality of the raw e-commerce transaction
dataset before analysis. It identifies missing values, duplicates,
invalid entries, and describes how each issue is handled.

The goal is transparency: **every number in the dashboard should be
traceable back to a documented data-quality decision.**

---

## 2. Dataset Overview

| Item | Value |
|------|-------|
| Source file | `data/ecommerce_data.csv` |
| Format | CSV (UTF-8) |
| Primary key | `order_id` |
| Total rows (raw) | To be filled after loading |
| Total columns | 11 |
| Time period | As present in the dataset |

---

## 3. Required Columns

The following columns must be present for the analysis to run:
order_id, order_date, customer_id, product_id, product_name,
category, region, quantity, unit_price, discount, sales



If any column is missing, the application stops and lists the missing
columns. No partial analysis is performed.

---

## 4. Data Quality Checks Performed

| # | Check | Rule | Action if Fails |
|---|-------|------|-----------------|
| 1 | Required columns | All must exist | Stop analysis, list missing |
| 2 | Missing values | Reported per column | Report only |
| 3 | Duplicate orders | `order_id` must be unique | Remove duplicates (keep first) |
| 4 | Quantity valid | `quantity ≥ 1` | Remove row |
| 5 | Unit price valid | `unit_price > 0` | Remove row |
| 6 | Discount valid | `0 ≤ discount ≤ 100` | Remove row |
| 7 | Date valid | `order_date` parses as a date | Remove row |
| 8 | Sales present | `sales` must not be null | Remove row |
| 9 | Critical IDs | `order_id`, `customer_id`, `order_date` present | Remove row |

---

## 5. Summary of Findings

*(Fill in actual numbers after running the app.)*

| Check | Count |
|-------|-------|
| Total rows (raw) | — |
| Duplicate order IDs | — |
| Missing category | — |
| Missing region | — |
| Missing sales | — |
| Invalid quantity | — |
| Invalid unit price | — |
| Invalid discount | — |
| Invalid order date | — |
| Rows after cleaning | — |

---

## 6. Treatment of Issues

### 6.1 Missing Values

- **Category / Region / Product Name** → Filled with `"Unknown"`.
- **Sales / Quantity / Unit Price** → Row removed (cannot calculate KPIs).
- **Customer ID / Order ID** → Row removed (identity required).

### 6.2 Duplicate Orders

- Duplicate `order_id` rows are removed. Only the first occurrence
  is kept. This prevents double-counting in revenue.

### 6.3 Invalid Numeric Values

- Quantity `< 1` → removed.
- Unit price `< 0.01` → removed.
- Discount `< 0` or `> 100` → removed.

### 6.4 Invalid Dates

- Rows where `order_date` cannot be parsed are removed because they
  break time-series analysis.

### 6.5 Outliers

- Outliers in `sales` are **flagged, not removed**.
- A high-value order may be a legitimate bulk or corporate purchase.
- Outliers are visible on the **Statistics** page.

---

## 7. Impact on Analysis

| Decision | Reason |
|----------|--------|
| Keep outliers | May represent genuine bulk orders |
| Drop rows with no sales | Cannot contribute to revenue KPIs |
| Fill missing text with "Unknown" | Preserves row for other KPIs |
| Remove duplicates | Prevents inflated totals |
| Require valid dates | Enables trend analysis |

---

## 8. Post-Cleaning Guarantees

After cleaning, the dataset satisfies:

- No duplicate `order_id`
- No missing `order_id`, `customer_id`, `order_date`, or `sales`
- `quantity ≥ 1`
- `unit_price > 0`
- `0 ≤ discount ≤ 100`
- `order_date` is a valid date
- New derived columns exist:
  - `gross_sales`
  - `discount_amount`
  - `net_sales`
  - `order_year`
  - `order_month`
  - `order_month_name`

---

## 9. Recommended Follow-Ups

- Confirm that removed rows were truly invalid (not source errors).
- Review flagged outliers to determine whether they are genuine.
- Monitor the incoming data pipeline to prevent recurring issues.
- Periodically re-run this report as new data arrives.

---

## 10. Conclusion

The dataset is **suitable for analysis** after the documented cleaning
steps. All KPIs in the dashboard are computed from the cleaned data,
and every transformation is traceable to a rule in this report.