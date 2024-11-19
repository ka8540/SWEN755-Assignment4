# from EventManagement.server.src.db.utilities import connect
from utilities.swen_344_db_utils import connect, exec_commit, exec_get_one

def get_all_events():
    try:
        conn = connect()
        cur = conn.cursor()
        query = """
            SELECT id, date, description, title, location, time, organizer, audience_type
            FROM EventData
        """
        cur.execute(query)
        events = cur.fetchall()
        cur.close()
        conn.close()

        # Convert query result to a list of dictionaries
        return [
            {
                "id": row[0],
                "date": str(row[1]),
                "description": row[2],
                "title": row[3],
                "location": row[4],
                "time": str(row[5]),
                "organizer": row[6],
                "audience_type": row[7]
            }
            for row in events
        ]
    except Exception as e:
        print(f"Error fetching events: {e}")
        return []

# to log the user activity
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

def get_event_titles():
    query = """
        SELECT id, title 
        FROM EventData
    """
    return exec_get_all(query)


