from utilities.swen_344_db_utils import exec_get_all, exec_get_one, exec_commit

def validate_user_session(user_id, session_key):
    query = """
        SELECT session_key 
        FROM UserTable 
        WHERE id = %s AND session_key = %s AND role = 'Student'
    """
    result = exec_get_one(query, (user_id, session_key))
    return result is not None

def get_all_events():
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

def log_user_activity(session_key, activity, status, user_id):
    query = """
        INSERT INTO SessionStorage (session_key, data, timestamp, user_id)
        VALUES (%s, %s, CURRENT_TIMESTAMP, %s)
    """
    activity_data = f"{activity} | Status: {status}"
    exec_commit(query, (session_key, activity_data, user_id))