# TODO: uuid를 생성하지 말고 mongo에서 생성하는 것을 사용하도록 수정
import sys
from pathlib import Path
from typing import Optional
import datetime
from uuid import uuid4

from dotenv import dotenv_values
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from aiofiles import open as aio_open
import ujson as json
from motor import motor_asyncio as mongo

from ..richlogger import set_logger, handle_exception


config = dotenv_values(".env")

logger = set_logger()
sys.excepthook = handle_exception

router = APIRouter(
    prefix="/insert",
    tags=["insert"],
    responses={404: {"description": "Not found"}},
)


class Data(BaseModel):
    """FastAPI에서 요구하는 데이터 형식
    demo: (bool) API 문서에서 테스트할 때 데이터 저장을 막기 위해 사용
    category: (str) "database/collection/category"의 구조
        database와 collection은 mongodb 구조를 의미하며
        category는 추가적인 분류를 위한 정보를 의미함
    acq_time: (ISOdatetime) 수집 시간
    payload: (dict) json 형식으로 파일 형식으로 저장할 데이터 전송
    description: (Optional, str) 필요한 경우 데이터에 대한 설명 추가
    """

    demo: bool = True
    category: str = "database/collection/category"
    acq_time: datetime.datetime = datetime.datetime.now()
    payload: dict = {"key": "value"}
    description: Optional[str] = None


@router.post("/", status_code=status.HTTP_201_CREATED)
async def insert_data(data: Data):
    """데이터를 수신하여 파일로 저장하고 메타 정보를 DB에 저장
    1. uuid4를 통해 json 파일 이름 생성
    2. category에 해당하는 디렉토리 없으면 생성하고 파일 경로 설정
    3. payload가 비어있는 경우 400 에러 반환
    4. json 형식으로 payload 저장
    5. DB에 저장할 document 생성
        - category, acq_time, keys, path, description
    6. DB에 저장
    """
    data.category = data.category.lower()
    data_id = str(uuid4())

    # TODO: NFS에 데이터 저장하는 방법 고민
    dir_path = Path(f"{config['TMPDIR']}/{data.category}")
    dir_path.mkdir(parents=True, exist_ok=True)
    data_path = dir_path / f"{data_id}.json"
    logger.info(f"Data Path: {data_path}")

    if len(data.payload.keys()) == 0:
        logger.error("Payload is empty")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Payload is empty"
        )

    if not data.demo:
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

    if not data.demo:
        client = mongo.AsyncIOMotorClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        _id = await collection.insert_one(document)
        client.close()
        logger.info(f"Document inserted to MongoDB. ID:{_id.inserted_id}")

        return {"file_id": data_id, "mongodb_id": str(_id.inserted_id)}
    else:
        return {
            "file_id": "a406cec7-5a9b-44f4-a140-161d613f634d",
            "mongodb_id": "61c92168d7ab1811c0bec4ad",
        }
