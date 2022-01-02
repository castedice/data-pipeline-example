import sys
from pathlib import Path

from locust import FastHttpUser, task, between
import numpy as np
import ujson as json

from data_source_mock.richlogger import set_logger, handle_exception

logger = set_logger()
sys.excepthook = handle_exception

# TODO: locust master와 worker를 구현하여 테스트를 해봐야 함


class ArrayDataSource(FastHttpUser):
    wait_time = between(1, 10)

    @task
    def insert_array_data(self):
        response = self.client.post(
            "/insert",
            json={
                "demo": False,
                "category": "database/collection/category",
                "acq_time": "2022-01-02T10:42:10.834703",
                "payload": {"prps": make_synthetic_array_data()},
                "description": "string",
            },
        )
        logger.info(f"response: {response.status_code}")
        logger.info(f"response: {response.text}")


def make_synthetic_array_data():
    return np.random.randint(0, 255, size=(3600, 128)).tolist()
