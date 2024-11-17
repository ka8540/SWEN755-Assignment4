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
        INSERT INTO EventData (date, description, title, location, time, organizer)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    exec_commit(query, (
        event_data['date'],
        event_data['description'],
        event_data['title'],
        event_data['location'],
        event_data['time'],
        event_data['organizer']
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
