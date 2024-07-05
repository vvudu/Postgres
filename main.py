import psycopg2

# Создаем функции:
# Создание базы данных
def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100),
            phones VARCHAR(20)[]
        );
        ''')
        conn.commit()

 # Добавление нового клиента
def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO clients (first_name, last_name, email, phones)
        VALUES (%s, %s, %s, %s);
        ''', (first_name, last_name, email, phones))
        conn.commit()

    # Добавление телефона к существующему клиенту
def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE clients SET phones = array_append(phones, %s) WHERE client_id=%s;
        ''', (phone, client_id))
        conn.commit()

    # Изменение данных о клиенте
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        if first_name:
            cur.execute('''
            UPDATE clients SET first_name=%s WHERE client_id=%s;
            ''', (first_name, client_id))
        
        if last_name:
            cur.execute('''
            UPDATE clients SET last_name=%s WHERE client_id=%s;
            ''', (last_name, client_id))
        
        if email:
            cur.execute('''
            UPDATE clients SET email=%s WHERE client_id=%s;
            ''', (email, client_id))
        
        if phones is not None:
            cur.execute('''
            UPDATE clients SET phones=%s WHERE client_id=%s;
            ''', (phones, client_id))
        
        conn.commit()
  
    # Удаление телефона у существующего клиента
def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE clients SET phones = array_remove(phones, %s) WHERE client_id=%s;
        ''', (phone, client_id))
        conn.commit()

    # Удаление существующего клиента
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM clients WHERE client_id=%s;
        ''', (client_id,))
        conn.commit()
 
    # Поиск клиента по имени
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    query = '''
    SELECT client_id, first_name, last_name, email, phones
    FROM clients
    WHERE TRUE
    '''
    params = []
    
    if first_name:
        query += ' AND first_name=%s'
        params.append(first_name)
    
    if last_name:
        query += ' AND last_name=%s'
        params.append(last_name)
    
    if email:
        query += ' AND email=%s'
        params.append(email)
    
    if phone:
        query += ' AND %s = ANY(phones)'
        params.append(phone)
    
    with conn.cursor() as cur:
        cur.execute(query, tuple(params))
        results = cur.fetchall()
        return results

# Пример использования:
with psycopg2.connect(database="netology_db", user="postgres", password="1912") as conn:
    create_db(conn)
    
   
    add_client(conn, 'Иван', 'Иванов', 'ivan.petrov@mail.ru', ['+79876543210', '+79123456789'])
    
    add_phone(conn, 1, '+79001234567')
    
    change_client(conn, 1, first_name='Иван', last_name='Петров', email='ivan.petrov@mail.ru')
  
    delete_phone(conn, 1, '+79123456789')
   
    clients = find_client(conn, first_name='Иван')
    print(clients)
    
    delete_client(conn, 1)

conn.close()
