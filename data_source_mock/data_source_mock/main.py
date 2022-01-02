import sys
import time
import numpy as np

from locust import HttpUser, task, between
from dotenv import dotenv_values

from .richlogger import set_logger, handle_exception

config = dotenv_values(".env")

logger = set_logger()
sys.excepthook = handle_exception


class ArrayDataSource(HttpUser):
    wait_time = between(1, 10)

    @task
    def insert_array_data(self):
        self.client.post("/insert")
