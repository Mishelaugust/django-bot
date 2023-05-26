import pymysql


ENDPOINT = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
DBNAME = 'usersdb'
PASSWORD = '1234' 
CURSORCLASS = pymysql.cursors.DictCursor

TOKEN = '5848210560:AAHMXEoE6NP6ii5TiAmHk9hM8MapLxvjp0M'

def initial_connection():
    try:
        connection = pymysql.connect(host=ENDPOINT,
            port=PORT,
            user=USERNAME,
            passwd=PASSWORD,
            db=DBNAME,
            cursorclass=CURSORCLASS)
        print('[+] Local Connection Successful')
    except Exception as e:
            print(f'[+] Local Connection Failed: {e}')
            connection = None

    return connection