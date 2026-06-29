Flight Delay Prediction Web Application

Ứng dụng web dự báo và tra cứu tình trạng trễ chuyến bay sử dụng dữ liệu chuyến bay năm 2024 kết hợp với cơ sở dữ liệu SQLite và Flask.

## Giới thiệu

Đây là đồ án xây dựng hệ thống dự báo và thống kê chuyến bay trễ.

Hệ thống sử dụng:

- Flask để xây dựng Website
- SQLite để lưu trữ dữ liệu
- Pandas để xử lý dữ liệu CSV
- Dataset dự báo chuyến bay năm 2024 được tạo từ mô hình Machine Learning (Gradient Boosted)

Website cho phép:

- Xem hãng hàng không có tỷ lệ đúng giờ cao nhất theo từng ngày
- Tra cứu chuyến bay theo:
  - Ngày
  - Sân bay đi
  - Sân bay đến
- Thống kê các hãng hàng không có tỷ lệ trễ thấp nhất
- Thống kê các hãng hàng không có tỷ lệ trễ cao nhất

---

# Công nghệ sử dụng

- Python 3.x
- Flask
- SQLite3
- Pandas
- HTML5
- CSS3
- Bootstrap (nếu có)

---


# Dataset

Dữ liệu sử dụng:

```
flight_delay_prediction_2024.csv
```

Bao gồm các trường:

| Cột | Ý nghĩa |
|------|----------|
| year | Năm |
| month | Tháng |
| day_of_month | Ngày |
| fl_date | Ngày chuyến bay |
| op_unique_carrier | Hãng hàng không |
| origin | Sân bay khởi hành |
| origin_city_name | Thành phố khởi hành |
| dest | Sân bay đến |
| dest_city_name | Thành phố đến |
| dep_delay | Trễ khởi hành |
| arr_delay | Trễ đến |
| distance | Khoảng cách |
| pred_delay_prob | Xác suất trễ dự đoán |
| pred_delay_15 | Dự báo có trễ trên 15 phút |

...

---

# Cách hoạt động

## 1. Khởi tạo Database

Khi chạy lần đầu:

- Đọc dữ liệu CSV
- Chuẩn hóa dữ liệu
- Chuyển ngày về định dạng

```
YYYY-MM-DD
```

Sau đó lưu vào SQLite.

Nếu phát hiện database cũ không đúng cấu trúc thì hệ thống sẽ:

- Xóa database cũ
- Khởi tạo lại tự động

---

## 2. Trang chủ

Hiển thị:

- Hôm qua
- Hôm nay
- Ngày mai

Dựa trên ngày hiện tại nhưng ánh xạ sang năm 2024 để phù hợp với dữ liệu.

Ví dụ:

Ngày thực tế:

```
29/06/2026
```

Sẽ được chuyển thành:

```
29/06/2024
```

Sau đó thống kê:

- Hãng ít trễ nhất
- Tỷ lệ chuyến bay trễ

---

## 3. Tra cứu chuyến bay

Người dùng nhập:

- Ngày
- Tháng
- Sân bay đi
- Sân bay đến

Sau đó hệ thống truy vấn SQLite và hiển thị:

- Hãng bay
- Số chuyến
- Thời gian trễ trung bình
- Tỷ lệ chuyến bay trễ

---

## 4. Thống kê

Trang chủ hiển thị:

### Top 5 hãng đúng giờ nhất

Sắp xếp theo:

```
ORDER BY rate ASC
```

### Top 5 hãng trễ nhiều nhất

Sắp xếp theo:

```
ORDER BY rate DESC
```

---

# Thuật toán

Dataset được xây dựng từ mô hình Machine Learning:

**Gradient Boosted**

Quy trình:

```
Dữ liệu năm 2019
            │
            ▼
Huấn luyện mô hình Gradient Boosted
            │
            ▼
Dữ liệu năm 2020
            │
            ▼
Đánh giá mô hình
            │
            ▼
Áp dụng dự báo cho dữ liệu năm 2024
            │
            ▼
Sinh xác suất trễ (pred_delay_prob)
            │
            ▼
Sinh nhãn dự báo (pred_delay_15)
```

Các cột:

```
pred_delay_prob
```

là xác suất chuyến bay bị trễ.

```
pred_delay_15
```

là kết quả phân loại:

- 0 : Không trễ
- 1 : Trễ trên 15 phút

---

# Database

SQLite gồm một bảng:

```
flights
```

Các trường lưu:

```
fl_date

op_unique_carrier

origin

origin_city_name

dest

dest_city_name

arr_delay
```

---

# Cài đặt

## Clone project

```bash
git clone https://github.com/username/PredictionFlight.git
```

---

## Cài thư viện

```bash
pip install -r requirements.txt
```

Hoặc:

```bash
pip install flask pandas
```

---

## Chạy chương trình

```bash
python app.py
```

Sau đó truy cập:

```
http://127.0.0.1:5000
```

---

# Yêu cầu hệ thống

- Python >= 3.10
- Flask
- Pandas
- SQLite3

---

# Một số chức năng nổi bật

✔ Tra cứu chuyến bay

✔ Thống kê hãng bay

✔ Hiển thị tỷ lệ trễ

✔ Khởi tạo Database tự động

✔ Tự động cập nhật Database khi thay đổi cấu trúc

✔ Giao diện Web trực quan

---

# Hướng phát triển

Trong tương lai có thể mở rộng:

- Kết nối API chuyến bay thời gian thực
- Dự báo theo thời tiết
- Hiển thị biểu đồ thống kê
- Đăng nhập người dùng
- Dashboard quản trị
- Triển khai trên Render hoặc Railway
- Kết nối MySQL/PostgreSQL thay SQLite

---

# Tác giả

**Kiệt Nguyễn**

Đồ án môn học:

**Dự báo tình trạng trễ chuyến bay bằng Machine Learning (Gradient Boosted) và xây dựng Website tra cứu bằng Flask**

---

# Giấy phép

Dự án phục vụ mục đích học tập và nghiên cứu.

```
MIT License
```
