from utilities.swen_344_db_utils import exec_get_one, exec_commit

# Validate user session by checking session_key
def validate_user_session(user_id, session_key):
    query = """
        SELECT session_key 
        FROM UserTable 
        WHERE id = %s AND session_key = %s AND role = 'Student'
    """
    result = exec_get_one(query, (user_id, session_key))
    return result is not None

# Add an event to the user's bucket
def add_event_to_bucket(user_id, event_id):
    # Check if the event is already in the bucket
    query_check = """
        SELECT id 
        FROM EventBucket 
        WHERE user_id = %s AND event_id = %s
    """
    existing = exec_get_one(query_check, (user_id, event_id))
    if existing:
        return False  # Event already exists in the bucket

    # Insert the event into the bucket
    query_insert = """
        INSERT INTO EventBucket (user_id, event_id)
        VALUES (%s, %s)
    """
    exec_commit(query_insert, (user_id, event_id))
    return True

def get_user_major(user_id):
    query = "SELECT major FROM UserTable WHERE id = %s"
    result = exec_get_one(query, (user_id,))
    return result[0] if result else None

def get_event_audience_type(event_id):
    query = "SELECT audience_type FROM EventData WHERE id = %s"
    result = exec_get_one(query, (event_id,))
    return result[0] if result else None

def add_event_to_bucket(user_id, event_id):
    query = """
        INSERT INTO EventBucket (user_id, event_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """
    exec_commit(query, (user_id, event_id))
    return True  # Return True if insertion succeeded

def log_user_activity(session_key, activity, status, user_id):
    query = """
        INSERT INTO SessionStorage (session_key, data, timestamp, user_id)
        VALUES (%s, %s, CURRENT_TIMESTAMP, %s)
    """
    data = f"{activity} | Status: {status}"
    exec_commit(query, (session_key, data, user_id))