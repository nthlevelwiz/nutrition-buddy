

from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
from pydantic import BaseModel, validator
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import date, time
application = FastAPI()

# DATABASE_URL = "postgresql://neondb_playground_db_owner:VG4qeU3ADkaJ@ep-yellow-lake-a6yiod54.us-west-2.aws.neon.tech/neondb_playground_db?sslmode=require"
DATABASE_URL = "postgresql://neondb_playground_db_owner:VG4qeU3ADkaJ@ep-yellow-lake-a6yiod54.us-west-2.aws.neon.tech/neondb_playground_db?sslmode=require&options=endpoint%3Dep-yellow-lake-a6yiod54"

class FoodItem(BaseModel):
    calories: int
    protein: int
    barcode: str
    meal: str
    portion: str
    date: str
    time: str
    servingSize: int
    servingSizeUnits: str
    photoId: str
    food_item_name: str

    @validator('date', pre=True)
    def parse_date(cls, value):
        if isinstance(value, date):
            return value.isoformat()
        return value
    @validator('time', pre=True)
    def parse_time(cls, value):
        if isinstance(value, time):
            return value.isoformat()
        return value

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

@application.get("/food_items", response_model=List[FoodItem])
def read_food_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT "calories", "protein", "barcode", "meal", "portion", "date", "time", "servingSize", "servingSizeUnits", "photoId", "food_item_name" FROM "food_item"')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items

@application.post("/food_items", response_model=FoodItem)
def create_food_item(item: FoodItem):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO "food_item" ("calories", "protein", "barcode", "meal", "portion", "date", "time", "servingSize", "servingSizeUnits", "photoId", "food_item_name") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *',
        (item.calories, item.protein, item.barcode, item.meal, item.portion, item.date, item.time, item.servingSize, item.servingSizeUnits, item.photoId, item.food_item_name)
    )
    new_item = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return new_item

@application.put("/food_items/{barcode}", response_model=FoodItem)
def update_food_item(barcode: str, item: FoodItem):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE "food_item" SET "calories" = %s, "protein" = %s, "meal" = %s, "portion" = %s, "date" = %s, "time" = %s, "servingSize" = %s, "servingSizeUnits" = %s, "photoId" = %s, "food_item_name" = %s WHERE "barcode" = %s RETURNING *',
        (item.calories, item.protein, item.meal, item.portion, item.date, item.time, item.servingSize, item.servingSizeUnits, item.photoId, item.food_item_name, barcode)
    )
    updated_item = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Food item not found")
    return updated_item

@application.delete("/food_items/{barcode}", response_model=FoodItem)
def delete_food_item(barcode: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM "food_item" WHERE "barcode" = %s RETURNING *', (barcode,))
    deleted_item = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Food item not found")
    return deleted_item
