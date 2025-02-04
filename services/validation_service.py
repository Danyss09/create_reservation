import requests
import os

CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://customer-service:8001")
TABLE_SERVICE_URL = os.getenv("TABLE_SERVICE_URL", "http://table-service:8002")

def validate_customer(customer_id: int) -> bool:
    response = requests.get(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}")
    return response.status_code == 200

def validate_table(table_id: int) -> bool:
    response = requests.get(f"{TABLE_SERVICE_URL}/tables/{table_id}")
    return response.status_code == 200
