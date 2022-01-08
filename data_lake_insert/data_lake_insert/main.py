# TODO: Authorization 설정
# TODO: 필요하다면 nginx로 리버스프록시 추가
# TODO: 필요하다면 kafka로 message queue 추가
# TODO: kafka 분산처리용 zookeeper 추가

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import insert


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(insert.router)
