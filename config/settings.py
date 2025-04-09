import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Environment settings
ENVIRONMENT = os.environ.get("FLASK_ENV", "production")
DEBUG = ENVIRONMENT == "development"

# Server settings
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 5000))

# CORS settings
if ENVIRONMENT == "development":
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
else:
    CORS_ORIGINS = ["https://erth.network"]

# Secret Network settings
SECRET_NETWORK_LCD = os.environ.get("SECRET_NETWORK_LCD", "https://lcd.erth.network")
SECRET_NETWORK_CHAIN_ID = os.environ.get("SECRET_NETWORK_CHAIN_ID", "secret-4")
REGISTRATION_CONTRACT = os.environ.get(
    "REGISTRATION_CONTRACT", 
    "secret12q72eas34u8fyg68k6wnerk2nd6l5gaqppld6p"
)
REGISTRATION_HASH = os.environ.get(
    "REGISTRATION_HASH", 
    "04bd5177bad4c7846e97a9e3d345cf9e3e7fca5969f90ac20f3a5afc5b471cd5"
)

# Wallet settings
WALLET_KEY_FILE = os.environ.get("WALLET_KEY_FILE", "WALLET_KEY.txt")

# SecretAI settings
SECRET_AI_API_URL = os.environ.get("SECRET_AI_API_URL", "https://secretai1.scrtlabs.com/v1/chat")
SECRET_AI_API_KEY = os.environ.get(
    "SECRET_AI_API_KEY", 
    "N/A"
)
SECRET_AI_MODEL = os.environ.get("SECRET_AI_MODEL", "llama3.2-vision")

# Upload settings
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

# Analytics settings
ANALYTICS_DIR = BASE_DIR / "data"
ANALYTICS_FILE = ANALYTICS_DIR / "analytics.json"
SNAPSHOT_INTERVAL = int(os.environ.get("SNAPSHOT_INTERVAL", 3600))  # 1 hour

# Contract configuration
REGISTRATION_CONTRACT = "secret12q72eas34u8fyg68k6wnerk2nd6l5gaqppld6p"
REGISTRATION_HASH = "04bd5177bad4c7846e97a9e3d345cf9e3e7fca5969f90ac20f3a5afc5b471cd5"