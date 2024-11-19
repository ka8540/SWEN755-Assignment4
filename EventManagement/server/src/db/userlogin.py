from utilities.swen_344_db_utils import exec_get_one, exec_commit

def get_user_credentials(username):
    query = """
        SELECT id, password, role 
        FROM UserTable 
        WHERE username = %s AND role = 'Student'
    """
    user_credentials = exec_get_one(query, (username,))
    return user_credentials

def update_user_session_key(user_id, session_key):
    query = """
        UPDATE UserTable 
        SET session_key = %s 
        WHERE id = %s
    """
    exec_commit(query, (session_key, user_id))

def log_user_activity(activity_data, user_id):
    query = """
        INSERT INTO SessionStorage (session_key, user_id, data, timestamp)
        VALUES (%s, %s, %s, %s)
    """
    exec_commit(query, (
        activity_data['session_key'], 
        user_id, 
        activity_data['data'], 
        activity_data['timestamp']
    ))

def log_user_activity(activity_data, user_id):
    query = """
        INSERT INTO SessionStorage (session_key, data, timestamp, user_id)
        VALUES (%s, %s, %s, %s)
    """
    try:
        exec_commit(query, (
            activity_data["session_key"],
            activity_data["data"],
            activity_data["timestamp"],
            user_id
        ))
    except Exception as e:
        print(f"Error logging user activity: {e}")
        
def invalidate_user_session_key(user_id):
    query = """
        UPDATE UserTable
        SET session_key = NULL
        WHERE id = %s
    """
    try:
        exec_commit(query, (user_id,))
        return True
    except Exception as e:
        print(f"Error invalidating session key: {e}")
        return False
