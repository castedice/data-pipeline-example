import sys
import logging
import logging.handlers
from typing import Optional
import datetime
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel
from dotenv import dotenv_values
from rich.logging import RichHandler
from aiofiles import open as aio_open
import ujson as json
from motor import motor_asyncio as mongo

LOG_PATH = "./log.log"
RICH_FORMAT = "[%(filename)s:%(lineno)s] >> %(message)s"
FILE_HANDLER_FORMAT = "[%(asctime)s]\\t%(levelname)s\\t[%(filename)s:%(funcName)s:%(lineno)s]\\t>> %(message)s"


def set_logger() -> logging.Logger:
    logging.basicConfig(
        level="NOTSET", format=RICH_FORMAT, handlers=[RichHandler(rich_tracebacks=True)]
    )
    logger = logging.getLogger("rich")

    file_handler = logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(FILE_HANDLER_FORMAT))
    logger.addHandler(file_handler)

    return logger


def handle_exception(exc_type, exc_value, exc_traceback):
    logger = logging.getLogger("rich")

    logger.error("Unexpected exception", exc_info=(exc_type, exc_value, exc_traceback))


logger = set_logger()
sys.excepthook = handle_exception

config = dotenv_values(".env")

app = FastAPI()


class Data(BaseModel):
    category: str
    acq_time: datetime.datetime
    payload: dict
    description: Optional[str] = None


@app.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_data(data: Data):
    data_id = str(uuid4())
    # TODO: NFS에 데이터 저장하는 방법 고민
    data_path = Path(f"{config['TMPDIR']}/{data_id}.json")
    logger.info(f"Data Path: {data_path}")

    async with aio_open(str(data_path), "w") as f:
        await f.write(json.dumps(data.payload))
    logger.info(f"Data is saved to file server.")

    mongo_uri = f"mongodb://{config['MONGO_INITDB_ROOT_USERNAME']}:{config['MONGO_INITDB_ROOT_PASSWORD']}@{config['MONGO_HOST']}:{config['MONGO_PORT']}/"
    db_name = data.category.split("/")[0]
    collection_name = data.category.split("/")[1]
    document = {}
    if len(data.category.split("/")) == 3:
        document["category"] = data.category.split("/")[2]
    document["acq_time"] = data.acq_time.isoformat()
    document["keys"] = list(data.payload.keys())
    document["path"] = str(data_path)
    if data.description:
        document["description"] = data.description
    logger.info("Document is ready.")

    client = mongo.AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    _id = await collection.insert_one(document)
    client.close()
    logger.info(f"Document inserted to MongoDB. ID:{_id.inserted_id}")

    return {"file_id": data_id, "mongodb_id": str(_id.inserted_id)}
