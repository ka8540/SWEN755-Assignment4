# from EventManagement.server.src.db.utilities import connect
from utilities.swen_344_db_utils import connect

from utilities.swen_344_db_utils import exec_commit


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
