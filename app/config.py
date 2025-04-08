import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///local.db") 
    
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "20ce36a79a8887f6023e73dd4a6ec49c1031e65ea31ea6dd6570e35dd87752e1")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SWAGGER_URL = os.getenv("SWAGGER_URL", "/api-docs")  
    API_URL = os.getenv("API_URL", "/static/swagger.yaml")  

    if FLASK_ENV == "production":
        if not SQLALCHEMY_DATABASE_URI: 
            raise ValueError("SQLALCHEMY_DATABASE_URI must be defined in production")
        if JWT_SECRET_KEY == "20ce36a79a8887f6023e73dd4a6ec49c1031e65ea31ea6dd6570e35dd87752e1":
            raise ValueError("JWT_SECRET_KEY must be defined in production")