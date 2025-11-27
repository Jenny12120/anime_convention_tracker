from database_service import connect_to_db

def add_convention_to_tracking(convention_id, convention_name):
    connection = connect_to_db()
    with connection.cursor() as cursor:
        add_convention = """
           INSERT INTO Tracking
           VALUES (%s, %s);
        """
        cursor.execute(add_convention,(convention_id, convention_name))
        cursor.commit()
    if 'connection' in locals() and connection.open:
        connection.close()

def retrieve_all_tracked_conventions():
    connection = connect_to_db()
    with connection.cursor() as cursor:
        select_all = """
            SELECT Tracking.id
            Convention.name,
            Convention.start_date,
            Convention.end_date,
            Convention.location AS venue
            FROM Tracking LEFT JOIN Conventions
            ON Tracking.convention_id = Conventions.id
        """
        cursor.execute(select_all)
    if 'connection' in locals() and connection.open:
        connection.close()
    return cursor.fetchall()

def untrack_convention(id):
    connection = connect_to_db()
    with connection.cursor() as cursor:
        delete_convention = """
           DELETE FROM Tracking 
           WHERE convention_id=%s;
        """
        cursor.execute(delete_convention,id)
    if 'connection' in locals() and connection.open:
        connection.close()
    return cursor.fetchall()

    
