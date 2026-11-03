# ============================================================
# config.py
# All settings for our project in one place.
# ============================================================

from pathlib import Path

# ------------------------------------------------------------
# 1. FOLDERS
# ------------------------------------------------------------
# BASE_DIR = the main project folder (ecommerce_analytics)
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR   = BASE_DIR / "data"
SRC_DIR    = BASE_DIR / "src"
DOCS_DIR   = BASE_DIR / "docs"
ASSETS_DIR = BASE_DIR / "assets"

# The default CSV file we will load
DEFAULT_DATA_FILE = DATA_DIR / "ecommerce_data.csv"


# ------------------------------------------------------------
# 2. APP INFO
# ------------------------------------------------------------
APP_TITLE   = "E-Commerce Sales Analytics"
APP_ICON    = "🛒"
APP_VERSION = "1.0.0"


# ------------------------------------------------------------
# 3. COLUMNS WE NEED IN THE DATA
# ------------------------------------------------------------
# If any of these are missing, we stop and show an error.
REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "product_id",
    "category",
    "region",
    "quantity",
    "unit_price",
    "discount",
    "sales",
]

# Columns with numbers (used for math)
NUMERIC_COLUMNS = [
    "quantity",
    "unit_price",
    "discount",
    "sales",
]

# Columns with text (used for filters)
CATEGORICAL_COLUMNS = [
    "category",
    "region",
    "product_name",
    "customer_id",
]


# Columns that must have valid values for a row to be useful
CRITICAL_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "product_id",
    "sales",
]

# Text columns used during cleaning
TEXT_COLUMNS = [
    "category",
    "region",
    "product_name",
    "customer_id",
]

# Date columns
DATE_COLUMNS = [
    "order_date",
]



# ------------------------------------------------------------
# 4. DATA RULES
# ------------------------------------------------------------
MIN_QUANTITY   = 1       # quantity must be 1 or more
MIN_UNIT_PRICE = 0.01    # price must be more than 0
MIN_DISCOUNT   = 0       # discount cannot be negative
MAX_DISCOUNT   = 100     # discount cannot be more than 100


# ------------------------------------------------------------
# 5. STATISTICS
# ------------------------------------------------------------
OUTLIER_IQR_MULTIPLIER = 1.5   # standard rule for finding outliers


# ------------------------------------------------------------
# 6. CURRENCY
# ------------------------------------------------------------
CURRENCY_SYMBOL = "₹"
LAKH = 100000   # 1 Lakh = 100,000


# ------------------------------------------------------------
# 7. COLORS (for charts)
# ------------------------------------------------------------
COLOR_PRIMARY = "#1f77b4"   # blue
COLOR_ACCENT  = "#ff7f0e"   # orange
COLOR_SUCCESS = "#2ca02c"   # green
COLOR_DANGER  = "#d62728"   # red

CHART_HEIGHT = 400