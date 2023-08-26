from unittest import TestCase

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app
import subprocess
import os

load_dotenv()


def execute_database(action, db_name):
    subprocess.call(["python", "execute_database_test.py", action, db_name])


class TestApi(TestCase):
    @classmethod
    def setUpClass(cls):
        execute_database("create", "test_database")
        os.environ["DB_NAME"] = "test_database"

    @classmethod
    def tearDownClass(cls):
        execute_database("delete", "test_database")

    def setUp(self):
        self.json_generic_customer = {
            "first_name": "John",
            "last_name": "Doe",
            "address": "Calle 123",
            "start_date": "2021-01-01",
            "end_date": "2021-01-01",
        }
        self.json_geric_order = {
            "customer_id": "11111",
            "title": "Doe",
            "planned_date_begin": "2021-01-01 01:00:00",
            "planned_date_end": "2021-01-01 02:00:00",
            "status": "NEW",
        }
        with TestClient(app) as client:
            self.client = client

    def test_create_customer(self):
        response = self.client.post(
            "/customers",
            json=self.json_generic_customer,
        )
        self.assertEqual(response.status_code, 201)
        assert response.json()["id"] is not None

    def test_create_order_failed_customer(self):
        self.json_geric_order["customer_id"] = "11111"
        response = self.client.post(
            "/orders",
            json=self.json_geric_order,
        )
        self.assertEqual(response.json()["detail"], "Customer not found")

    def test_create_order_failed_date_end(self):
        self.json_geric_order["planned_date_end"] = "2021-01-01 23:00:00"
        response = self.client.post(
            "/orders",
            json=self.json_geric_order,
        )
        self.assertEqual(response.json()["detail"][0]["msg"], "El tiempo máximo de ejecución es de 2 horas.")

    def test_create_order_failed_planned_date_begin(self):
        self.json_geric_order["planned_date_begin"] = "a"
        response = self.client.post(
            "/orders",
            json=self.json_geric_order,
        )
        self.assertEqual(response.json()["detail"][0]["msg"], "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'.")

    def test_create_order_failed_planned_date_end(self):
        self.json_geric_order["planned_date_end"] = "a"
        response = self.client.post(
            "/orders",
            json=self.json_geric_order,
        )
        self.assertEqual(response.json()["detail"][0]["msg"], "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'.")

    def test_create_order_good(self):
        response = self.client.post(
            "/customers",
            json=self.json_generic_customer,
        )
        self.assertEqual(response.status_code, 201)
        self.json_geric_order["customer_id"] = response.json()["id"]
        response = self.client.post(
            "/orders",
            json=self.json_geric_order,
        )
        self.assertEqual(response.status_code, 201)
        assert response.json()["id"] is not None

    def test_get_order_by_id(self):
        response_customer = self.client.post(
            "/customers",
            json=self.json_generic_customer,
        )
        self.assertEqual(response_customer.status_code, 201)
        self.json_geric_order["customer_id"] = response_customer.json()["id"]
        response = self.client.post(
            "/orders",
            json=self.json_geric_order,
        )
        self.assertEqual(response.status_code, 201)
        assert response.json()["id"] is not None
        response_get_by_order = self.client.get(
            "/orders/" + response.json()["id"],
        )
        self.assertEqual(response_get_by_order.status_code, 200)
        assert response_get_by_order.json()["work_order"]["id"] == response.json()["id"]
        assert response_get_by_order.json()["customer"]["id"] == response_customer.json()["id"]
