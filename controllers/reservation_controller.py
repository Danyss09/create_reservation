from flask import Blueprint, request, jsonify
import requests
from models.reservation_model import create_reservation

reservation_bp = Blueprint('reservation', __name__)

CUSTOMER_SERVICE_URL = "http://localhost:5000/get_customer"

@reservation_bp.route('/create_reservation', methods=['POST'])
def create_reservation_route():
    data = request.json
    
    # Validar si CustomerID existe en el microservicio de Customer
    response = requests.get(f"{CUSTOMER_SERVICE_URL}/{data['CustomerID']}")
    if response.status_code != 200:
        return jsonify({"error": "Customer not found"}), 400

    # Crear la reserva
    response = create_reservation(
        data['CustomerID'],
        data['TableID'],
        data['RestaurantID'],
        data['ReservationTime']
    )

    return jsonify(response)
