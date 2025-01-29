from services.db_config import get_connection

def create_reservation(customer_id, table_id, restaurant_id, reservation_time):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO Reservation (CustomerID, TableID, RestaurantID, ReservationTime, Status)
            VALUES (%s, %s, %s, %s, 'Pending')
            """
            cursor.execute(query, (customer_id, table_id, restaurant_id, reservation_time))
            connection.commit()

            reservation_id = cursor.lastrowid  # Obtener ID generado
            return {"message": "Reservation created successfully!", "ReservationID": reservation_id}
    except Exception as e:
        return {"error": str(e)}
    finally:
        connection.close()
