from utilities.swen_344_db_utils import exec_commit, exec_get_one

def register_user_in_db(user_data):
    query = """
        INSERT INTO UserTable (student_email, username, password, major, role, session_key)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    exec_commit(query, (
        user_data['student_email'],
        user_data['username'],
        user_data['password'],
        user_data['major'],
        user_data['role'],
        user_data['session_key']
    ))
    query_check = '''
        SELECT id 
        FROM UserTable 
        WHERE username = %s; 
    '''
    result = exec_get_one(query_check,(user_data['username'],))
    return result

     

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

def is_email_registered(student_email):
    query = """
        SELECT COUNT(*)
        FROM UserTable
        WHERE student_email = %s
    """
    result = exec_get_one(query, (student_email,))
    return result[0] > 0
