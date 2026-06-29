from flask import Flask, render_template, request
from datetime import datetime, timedelta
import database

app = Flask(__name__)
database.init_db()

@app.route('/')
def index():
    # Lấy ngày hiện tại nhưng gán vào năm 2024 để khớp dữ liệu
    now = datetime.now()
    today_sim = datetime(2024, now.month, now.day)
    
    dates_info = []
    for label, offset in [('Hôm qua', -1), ('Hôm nay', 0), ('Ngày mai', 1)]:
        d = today_sim + timedelta(days=offset)
        d_str = d.strftime('%Y-%m-%d')
        best = database.get_best_carrier_for_date(d_str)
        dates_info.append({
            'label': label, 'date': d.strftime('%d/%m'),
            'carrier': best['op_unique_carrier'] if best else 'N/A',
            'rate': round((best['delayed']/best['total'])*100, 2) if best else 0
        })

    airports = database.get_all_airports()
    top_best = database.get_top_stats('ASC')
    top_worst = database.get_top_stats('DESC')

    return render_template('index.html', dates_info=dates_info, airports=airports, 
                           top_best=top_best, top_worst=top_worst)

@app.route('/search', methods=['POST'])
def search():
    d, m = request.form.get('day'), request.form.get('month')
    date_str = f"2024-{m.zfill(2)}-{d.zfill(2)}"
    
    origin = request.form.get('origin').split(' - ')[0].strip().upper() or None
    dest = request.form.get('dest').split(' - ')[0].strip().upper() or None
    
    results = database.search_flights(date_str, origin, dest)
    return render_template('search.html', results=results, date=f"{d}/{m}/2024", origin=origin or "Tất cả", dest=dest or "Tất cả")

if __name__ == '__main__':
    app.run(debug=True)