import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER','root')}:{os.getenv('DB_PASSWORD','')}"
        f"@{os.getenv('DB_HOST','127.0.0.1')}:{os.getenv('DB_PORT','3306')}"
        f"/{os.getenv('DB_NAME','productos_db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INTERNAL_KEY = os.getenv('INTERNAL_KEY', '')