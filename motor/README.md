
# Motor Insurance Claims and Policy Analytics

## Project Overview

Motor Insurance Claims and Policy Analytics is a data analytics project designed to analyze customers, vehicles, insurance policies, claims, and payments.

The project uses Python for data processing and analysis, Pandas and NumPy for data manipulation, Plotly and Matplotlib for visualization, and Streamlit for the interactive dashboard.

## Objectives

- Analyze insurance policy portfolio performance.
- Monitor premium and coverage amounts.
- Understand claim volumes, statuses, and claim costs.
- Analyze claim processing and settlement timelines.
- Examine customer and vehicle characteristics.
- Identify potential business risks and provide data-driven recommendations.

## Project Structure

```text
motor/
├── data/
│   ├── raw/
│   └── cleaned/
├── notebooks/
│   └── insurance_analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── validation.py
│   ├── data_cleaner.py
│   ├── insurance_analysis.py
│   ├── visualization.py
│   ├── insights.py
│   └── logger.py
├── app/
│   └── streamlit_app.py
├── reports/
│   └── business_report.md
├── tests/
│   ├── test_pipeline.py
│   ├── test_analysis.py
│   └── test_validation.py
├── logs/
├── run_pipeline.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Datasets

Place the following CSV files inside `data/raw/`:

- `customers.csv`
- `vehicles.csv`
- `policies.csv`
- `claims.csv`
- `payments.csv`

The CSV files should contain the columns specified in the project requirements.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- SciPy
- Scikit-learn
- Pytest
- Docker

## Installation

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Data Pipeline

From the project root directory, run:

```bash
python run_pipeline.py
```

The pipeline loads the raw data, validates it, cleans the datasets, saves cleaned CSV files, and calculates key performance indicators.

## Run the Streamlit Dashboard

Run the following command from the project root:

```bash
python -m streamlit run app/streamlit_app.py
```

The dashboard will normally be available at:

`http://localhost:8501`

## Run Tests

Run the project tests with:

```bash
python -m pytest tests/ -v
```

## Docker

Build the Docker image:

```bash
docker build -t motor-insurance-analytics .
```

Start the container:

```bash
docker run -p 8501:8501 motor-insurance-analytics
```

Open `http://localhost:8501` in your browser.

Ensure the required CSV files are available to the application before running the pipeline or dashboard.

## Dashboard Sections

- Executive Overview
- Policy Analysis
- Claims Analysis
- Customer Analysis
- Vehicle Analysis
- Premium and Risk
- Insights and Recommendations

## Reports

The `reports/business_report.md` file documents the business objectives, KPIs, data quality considerations, and recommendations.

Final numerical findings should be based on analysis of the actual assignment datasets.

## Author

Motor Insurance Analytics Project