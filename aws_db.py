# Import required packages
import pandas as pd
import numpy as np
import os
import psycopg2
from datetime import datetime
from sqlalchemy import create_engine
import json

# Load secrets from secrets.json
with open('.vscode/secrets.json') as f:
    secrets = json.load(f)

# PostgreSQL DB Connection Parameters
DB_HOST = os.getenv("DB_HOST", "database-1.c3eic0i08xdc.ap-south-1.rds.amazonaws.com")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = secrets['db_password']
DB_PORT = os.getenv("DB_PORT", "5432")

engine_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(engine_string)


df = pd.read_csv("news_data_final.csv")

df.to_sql("news_data_final", con=engine, if_exists='replace')
