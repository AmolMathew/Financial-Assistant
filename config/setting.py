import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuration
CSV_FILE = os.path.join(BASE_DIR, "data", "Equity.csv")
TARGET_YEAR = "2023"
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads", TARGET_YEAR)
LOG_FILE = os.path.join(DOWNLOAD_FOLDER, f"download_log_{TARGET_YEAR}.txt")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
