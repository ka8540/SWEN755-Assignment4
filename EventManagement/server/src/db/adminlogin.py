from utilities.swen_344_db_utils import exec_get_one, exec_get_all, exec_commit

# Function to fetch admin credentials by email
def get_admin_credentials(username):
    query = """
        SELECT id, password, role 
        FROM UserTable 
        WHERE username = %s AND role = 'Admin'
    """
    admin_credentials = exec_get_one(query, (username,))
    return admin_credentials

# Function to update session key for admin
def update_admin_session_key(user_id, session_key):
    query = """
        UPDATE UserTable 
        SET session_key = %s 
        WHERE id = %s
    """
    exec_commit(query, (session_key, user_id))

# Function to check if an email is already registered
def is_email_registered(email):
    query = """
        SELECT COUNT(*) 
        FROM UserTable 
        WHERE student_email = %s
    """
    result = exec_get_one(query, (email,))
    return result[0] > 0


def invalidate_admin_session_key(user_id):
    query = """
        UPDATE UserTable
        SET session_key = NULL
        WHERE id = %s;
    """
    exec_commit(query, (user_id,))
    check_query = '''SELECT session_key 
                     FROM UserTable 
                     WHERE id = %s;'''
    result = exec_get_one(check_query,(user_id,))
    return result

def log_admin_activity(activity_data):
    query = """
        INSERT INTO SessionStorage (session_key, data, timestamp)
        VALUES (%s, %s, %s)
    """
    exec_commit(query, (activity_data['session_key'], activity_data['data'], activity_data['timestamp']))