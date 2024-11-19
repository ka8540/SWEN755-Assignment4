from utilities.swen_344_db_utils import exec_get_one, exec_commit, exec_get_all
from datetime import datetime

# Validate admin session by checking if session_key is valid
def validate_admin_session(user_id, session_key):
    query = """
        SELECT session_key 
        FROM UserTable 
        WHERE id = %s AND session_key = %s AND role = 'Admin'
    """
    result = exec_get_one(query, (user_id, session_key))
    return result is not None

# Add event details to EventData table
def add_event_to_db(event_data):
    query = """
        INSERT INTO EventData (date, description, title, location, time, organizer, audience_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    exec_commit(query, (
        event_data['date'],
        event_data['description'],
        event_data['title'],
        event_data['location'],
        event_data['time'],
        event_data['organizer'],
        event_data['audience_type']
    ))

# Log admin activity in SessionStorage table
def log_admin_activity(session_key, activity, status,user_id):
    query = """
        INSERT INTO SessionStorage (session_key, data, timestamp, user_id)
        VALUES (%s, %s, %s, %s)
    """
    activity_data = f"{activity} | Status: {status}"
    exec_commit(query, (session_key, activity_data, datetime.utcnow(),user_id))

def get_event_titles():
    query = """
        SELECT id, title 
        FROM EventData
    """
    return exec_get_all(query)

def get_event_details_by_id(event_id):
    query = """
        SELECT id, title, description, date, time, location, organizer, audience_type
        FROM EventData
        WHERE id = %s
    """
    result = exec_get_one(query, (event_id,))
    if result:
        return {
            "id": result[0],
            "title": result[1],
            "description": result[2],
            "date": str(result[3]),
            "time": str(result[4]),
            "location": result[5],
            "organizer": result[6],
            "audience_type": result[7]
        }
    return None

def update_event_by_id(event_id, updated_event):
    query = """
        UPDATE EventData
        SET title = %s, description = %s, date = %s, time = %s, location = %s, organizer = %s, audience_type = %s
        WHERE id = %s
    """
    try:
        exec_commit(query, (
            updated_event['title'],
            updated_event['description'],
            updated_event['date'],
            updated_event['time'],
            updated_event['location'],
            updated_event['organizer'],
            updated_event['audience_type'],
            event_id
        ))
        return True
    except Exception as e:
        print(f"Error updating event: {e}")
        return False