import abbreviations
from database_service import connect_to_db

def fetch_from_db_date_range(start_date, end_date):
    connection = connect_to_db()
    with connection.cursor() as cursor:
        retrieve_between_dates = """
        SELECT id AS convention_id,
            name,
            start_date,
            end_date,
            location AS venue,
            url
            FROM Conventions WHERE start_date >= %s AND end_date <= %s;
    """
        cursor.execute(retrieve_between_dates,(start_date, end_date))
    if 'connection' in locals() and connection.open:
        connection.close()
    
    return cursor.fetchall()

def fetch_from_db_location(location):
    connection = connect_to_db()
    province_state_abbrev = abbreviations.get_abbreviation(location)
    
    search_pattern_province_state = f"% {province_state_abbrev}%" 
    search_pattern_city = f"%, {location} __%"

   
    with connection.cursor() as cursor:
        retrieve_location = """
        SELECT id AS convention_id,
            name,
            start_date,
            end_date,
            location AS venue,
            url
            FROM Conventions WHERE location LIKE %s OR location LIKE %s OR country = %s;
    """
        cursor.execute(retrieve_location,(search_pattern_province_state, search_pattern_city, location))
    if 'connection' in locals() and connection.open:
        connection.close()
    
    return cursor.fetchall()