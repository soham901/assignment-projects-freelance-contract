import pymysql


timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="mysql-29c7d902-sandip-169.a.aivencloud.com",
  password="AVNS_mUrVl8TMxZSSXnNPAuq",
  read_timeout=timeout,
  port=13251,
  user="avnadmin",
  write_timeout=timeout,
)


def log_error(error):
    print(f"DB Error: {error}")



def get_leads():
  try:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM leads")
    return cursor.fetchall()
  
  except Exception as e:
    log_error(e)
    return []


def get_lead(id):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM leads WHERE id = '{id}'")
        return cursor.fetchone()
    
    except Exception as e:
        log_error(e)
        return None


def create_lead(data):
    try:
        cursor = connection.cursor()
        
        # if id exists, update
        if get_lead(data['id']):
            cursor.execute(f"UPDATE leads SET first_name = '{data['first_name']}', last_name = '{data['last_name']}', phone_work = '{data['phone_work']}' WHERE id = '{data['id']}'")
            connection.commit()
            return get_lead(data['id'])
        
        # if id does not exist, insert
        cursor.execute(f"INSERT INTO leads (id, first_name, last_name, phone_work) VALUES ('{data['id']}', '{data['first_name']}', '{data['last_name']}', '{data['phone_work']}')")
        connection.commit()
        return get_lead(data['id'])

    except Exception as e:
        log_error(e)
        return None




if __name__ == "__main__":
   data = get_leads()
   print(f"Total leads: {len(data)}")
