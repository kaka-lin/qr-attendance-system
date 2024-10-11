import os

config = {
    "GOOGLE_SHEET_KEY": os.getenv("GOOGLE_SHEET_KEY"),
    "GOOGLE_GMAIL_KEY": os.getenv("GOOGLE_GMAIL_KEY"),
    "GOOGLE_SHEET_URL": os.getenv("GOOGLE_SHEET_URL"),
    "MONGO_URI": os.getenv("MONGODB_URI")
}
