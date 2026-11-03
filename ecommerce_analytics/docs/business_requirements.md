# Business Requirements Document (BRD)

**Project:** E-Commerce Sales Performance & Customer Analytics

**Role:** Business Analyst

**Version:** 1.0

**Date:** 2026

**Status:** Approved for Development

---

## 1. Executive Summary

An e-commerce business generates thousands of orders every month. Management lacks a single view to understand sales performance, customer behavior, product performance, regional performance, and unusual transactions.

This project builds a **Streamlit analytics dashboard** that turns raw transaction data into KPIs, charts, statistical analysis, and management insights.

---

## 2. Business Problem

Management currently cannot easily answer:

- What is our total sales?
- How are sales changing over time?
- Which categories and products generate the most revenue?
- Which regions perform best and worst?
- What is the typical order value?
- Who are our high-value customers?
- Are there unusual transactions?
- Are discounts related to sales?

---

## 3. Objectives

### Primary Objective

Deliver a dashboard that answers all business questions from live data.

### Secondary Objectives

- Validate and clean transactional data automatically
- Calculate standard business KPIs dynamically
- Perform descriptive statistical analysis
- Identify potential outliers using the IQR method
- Segment customers by spending
- Provide downloadable results
- Generate plain-English insights and recommendations

---

## 4. Stakeholders

| Role | Primary Use |
|------|-------------|
| Business Managers | Overall performance |
| Sales Managers | Sales trend, top products |
| Marketing Managers | Customer segments, discount analysis |
| Operations Managers | Regional and category performance |
| Data Analysts | Validation and statistics pages |
| Leadership | Executive summary view |

---

## 5. Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-01 | The system must load CSV / Excel files |
| FR-02 | The system must validate required columns before analysis |
| FR-03 | The system must report data-quality issues |
| FR-04 | The system must compute KPIs dynamically from the data |
| FR-05 | The system must display sales trends over time |
| FR-06 | The system must group sales by category and region |
| FR-07 | The system must segment customers by spending |
| FR-08 | The system must calculate mean, median, variance, quartiles, IQR |
| FR-09 | The system must identify potential outliers |
| FR-10 | The system must compute correlation and covariance |
| FR-11 | The user must be able to filter data |
| FR-12 | The user must be able to download results |

---

## 6. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-01 | Runs on localhost using Streamlit |
| NFR-02 | Loads within 5 seconds on typical data volumes |
| NFR-03 | Handles invalid data gracefully without crashing |
| NFR-04 | Uses accessible colors and clear labels |
| NFR-05 | Every number in the dashboard must be recalculated from the data |
| NFR-06 | No hard-coded business results anywhere in the code |

---

## 7. Assumptions

- The dataset contains the required transaction columns.
- `sales` represents net sales after discount.
- `discount` is expressed as a percentage (0–100).
- `order_date` is in a standard date format.
- Users have basic familiarity with dashboards.

---

## 8. Constraints

- No database layer (CSV only) in v1.
- No authentication in v1.
- Runs locally, not deployed to the cloud.
- English language only.

---

## 9. Out of Scope (for v1)

- Machine learning models
- Forecasting
- Churn prediction
- Recommendation engines
- Real-time streaming data
- Multi-user authentication
- Cloud deployment

---

## 10. Acceptance Criteria

The project is complete when:

- [x] The app loads valid CSV / Excel data
- [x] Required columns are validated
- [x] Data-quality issues are reported
- [x] KPIs are calculated dynamically
- [x] Filters update all results
- [x] Charts render on all pages
- [x] Statistics (mean, median, IQR, etc.) are correct
- [x] Outliers are identified via the IQR method
- [x] Correlation and covariance are computed
- [x] Results can be downloaded
- [x] Insights are derived from the displayed data
- [x] The app handles errors gracefully

---

## 11. Approval

| Name | Role | Signature | Date |
|------|------|-----------|------|
| (Analyst) | Business Analyst | | |
| (Manager) | Business Manager | | |