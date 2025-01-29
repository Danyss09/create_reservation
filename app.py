from flask import Flask
from controllers.reservation_controller import reservation_bp

app = Flask(__name__)

# Registrar Blueprint
app.register_blueprint(reservation_bp, url_prefix="/reservations")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
