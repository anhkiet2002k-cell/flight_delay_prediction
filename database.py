import sqlite3
import pandas as pd
import os

DB_NAME = 'flights.db'
CSV_FILE = 'flight_delay_prediction_2024.csv'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Tự động kiểm tra và xóa DB cũ nếu thiếu cột
    if os.path.exists(DB_NAME):
        conn = get_db_connection()
        try:
            conn.execute("SELECT origin_city_name FROM flights LIMIT 1")
            conn.close()
        except sqlite3.OperationalError:
            conn.close()
            os.remove(DB_NAME)
            print("Đang cập nhật cấu trúc database mới...")

    if not os.path.exists(DB_NAME):
        print("Đang khởi tạo dữ liệu từ CSV (vui lòng đợi)...")
        df = pd.read_csv(CSV_FILE)
        df.columns = [c.lower().strip() for c in df.columns]
        df['fl_date'] = pd.to_datetime(df['fl_date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
        
        conn = get_db_connection()
        cols = ['fl_date', 'op_unique_carrier', 'origin', 'origin_city_name', 'dest', 'dest_city_name', 'arr_delay']
        df[cols].to_sql('flights', conn, index=False, if_exists='replace')
        conn.execute('CREATE INDEX idx_date ON flights (fl_date)')
        conn.close()
        print("Khởi tạo thành công!")

def get_all_airports():
    conn = get_db_connection()
    rows = conn.execute("SELECT DISTINCT origin, origin_city_name FROM flights ORDER BY origin").fetchall()
    conn.close()
    return rows

def get_best_carrier_for_date(date_str):
    conn = get_db_connection()
    query = """
        SELECT op_unique_carrier, COUNT(*) as total,
               SUM(CASE WHEN arr_delay > 15 THEN 1 ELSE 0 END) as delayed
        FROM flights WHERE fl_date = ?
        GROUP BY op_unique_carrier HAVING total > 5
        ORDER BY (CAST(delayed AS FLOAT)/total) ASC LIMIT 1
    """
    row = conn.execute(query, (date_str,)).fetchone()
    conn.close()
    return row

def get_top_stats(order='ASC'):
    conn = get_db_connection()
    query = f"""
        SELECT op_unique_carrier, COUNT(*) as total_flights,
               AVG(arr_delay) as avg_delay,
               (CAST(SUM(CASE WHEN arr_delay > 15 THEN 1 ELSE 0 END) AS FLOAT)/COUNT(*))*100 as rate
        FROM flights 
        GROUP BY op_unique_carrier HAVING total_flights > 20
        ORDER BY rate {order} LIMIT 5
    """
    rows = conn.execute(query).fetchall()
    conn.close()
    return rows

def search_flights(date_str, origin=None, dest=None):
    conn = get_db_connection()
    query = """
        SELECT op_unique_carrier, origin, dest, COUNT(*) as total,
               AVG(arr_delay) as avg_delay,
               (CAST(SUM(CASE WHEN arr_delay > 15 THEN 1 ELSE 0 END) AS FLOAT)/COUNT(*))*100 as rate
        FROM flights WHERE fl_date = ?
    """
    params = [date_str]
    if origin: query += " AND origin = ?"; params.append(origin)
    if dest: query += " AND dest = ?"; params.append(dest)
    query += " GROUP BY op_unique_carrier, origin, dest ORDER BY rate ASC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows