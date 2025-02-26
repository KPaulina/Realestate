import os
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv
import dash

# Load environment variables from .env file
load_dotenv()

# Read database credentials from environment variables
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("PASSWORD")
DB_HOST = os.getenv("HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DATABASE")

# Construct the database URL
DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

app = FastAPI()


@app.get("/{table_name}")
def get_user(table_name: str):
    # Create a new session
    try:
        with engine.connect() as conn:
            print("działa?")
            query = text(f"SELECT id, kwartal, bialystok, bydgoszcz, gdansk, gdynia, katowice, kielce, krakow, lublin, lodz, olsztyn, opole, poznan, rzeszow, szczecin, warszawa, wroclaw, zielona_gora, siedem_miast, dziesiec_miast, szesc_miast_bez_warszawy, dziewiec_miast FROM public.{table_name} ORDER BY id")
            df = pd.read_sql(query, conn)
            df = df.fillna('')
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




