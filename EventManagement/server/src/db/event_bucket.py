from utilities.swen_344_db_utils import exec_get_one, exec_commit
from datetime import datetime

def is_event_eligible(event_id, user_major):
    query = """
        SELECT audience_type
        FROM EventData
        WHERE id = %s
    """
    result = exec_get_one(query, (event_id,))
    if not result:
        return {"eligible": False, "message": "Event not found"}
    
    audience_type = result[0]
    if audience_type == "UG&G" or audience_type == user_major:
        return {"eligible": True}
    else:
        return {"eligible": False, "message": f"This event is for {audience_type} students"}

def add_event_to_bucket(user_id, event_id):
    query = """
        INSERT INTO EventAttendance (user_id, event_id)
        VALUES (%s, %s)
    """
    try:
        exec_commit(query, (user_id, event_id))
        return True
    except Exception as e:
        print(f"Error adding to bucket: {e}")
        return False

def log_event_activity(user_id, activity, status):
    query = """
        INSERT INTO SessionStorage (user_id, data, timestamp)
        VALUES (%s, %s, %s)
    """
    activity_data = f"{activity} | Status: {status}"
    exec_commit(query, (user_id, activity_data, datetime.utcnow()))
