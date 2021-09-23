from typing import Optional,List

from fastapi import FastAPI, HTTPException
from fastapi.logger import logger
from fastapi.param_functions import Query

import  pymysql
import logging 

import random
from pydantic import BaseModel


class Account(BaseModel):
    name: str
    address: str

DB_ENDPOINT = 'mysqldb'
DB_ADMIN_USER = 'root'
DB_ADMIN_PASSWORD = '123'
DB_NAME = "bitcoin"


app = FastAPI(title='Matching Service',version='0.1')
gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)

if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)


def get_db_conn():
    try:
        conn = pymysql.connect(host=DB_ENDPOINT, user=DB_ADMIN_USER, passwd=DB_ADMIN_PASSWORD, db=DB_NAME, connect_timeout=100)
        return conn
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        raise


@app.get("/")
def read_root():
    return {"Service": "wallet pool"}


@app.get("/wallet")
def get_wallet():
    conn = get_db_conn()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        query = "SELECT name,address FROM accounts"
        cursor.execute(query)

    if (results := cursor.fetchall()):
        conn.close()

        return random.choice(results)
    else:
        conn.close()

        raise HTTPException(status_code=404, detail= f'No accounts :/') 


@app.post("/wallet")
def post_wallet(account:Account):
    conn = get_db_conn()
    account_dict = account.dict()

    cursor = conn.cursor()
    query = "INSERT INTO accounts(name,address) values(%s,%s)"
    cursor.execute(query,(account.name,account.address))
    insert_id = conn.insert_id()
    conn.commit()
    conn.close()

    return {insert_id}


     


