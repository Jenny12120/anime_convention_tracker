from database_service import connect_to_db

def add_to_tracking(convention_id, convention_name):
    connection = connect_to_db()
    with connection.cursor() as cursor:
        add_convention = """
           INSERT INTO Tracking (convention_id, name)
           VALUES (%s, %s);
        """
        cursor.execute(add_convention,(convention_id, convention_name))
    connection.commit()
    if 'connection' in locals() and connection.open:
        connection.close()

def retrieve_all_tracked_conventions():
    connection = connect_to_db()
    with connection.cursor() as cursor:
        select_all = """
            SELECT Tracking.id,
            Conventions.name,
            Conventions.start_date,
            Conventions.end_date,
            Conventions.location AS venue,
            Conventions.url
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
           WHERE id=%s;
        """
        cursor.execute(delete_convention,id)
        connection.commit()
    if 'connection' in locals() and connection.open:
        connection.close()
    return cursor.fetchall()

    
