from database_service import connect_to_db


def add_convention_to_tracking_table():
    connection = connect_to_db()
    with connection.cursor() as cursor:
        retrieve_between_dates = """
        SELECT name,
            start_date,
            end_date,
            location AS venue,
            url
            FROM Conventions WHERE start_date >= %s AND end_date <= %s;
    """
        cursor.execute(retrieve_between_dates,(start_date, end_date))
    if 'connection' in locals() and connection.open:
        connection.close()


    
