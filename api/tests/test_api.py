from unittest import TestCase

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app

load_dotenv()


class TestApi(TestCase):
    def setUp(self):
        with TestClient(app) as client:
            self.client = client
