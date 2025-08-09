# Airflow Local Development Setup

Hướng dẫn chạy Apache Airflow local với Docker Compose để đọc DAGs từ folder `dac_coder`.
## Cách chạy dùng make:
### 1. Vào thư mục UAT-local
cd UAT-local

### 2. Khởi tạo lần đầu (tạo .env và init DB)
make init

### 3. Chạy Airflow
make up

# 4. Truy cập Web UI
# http://localhost:8080
# Username: admin / Password: admin123

## 🚀 Cách chạy

### 1. Tạo file .env (nếu chưa có)
```bash
# Tạo file .env trong thư mục UAT-local
echo "AIRFLOW_UID=50000" > .env
echo "_AIRFLOW_WWW_USER_USERNAME=admin" >> .env
echo "_AIRFLOW_WWW_USER_PASSWORD=admin123" >> .env
```

### 2. Khởi tạo Airflow
```bash
# Trong thư mục UAT-local
docker-compose up airflow-init
```

### 3. Chạy Airflow
```bash
# Chạy tất cả services
docker-compose up -d

# Hoặc chỉ chạy các service cần thiết
docker-compose up -d postgres airflow-webserver airflow-scheduler
```

### 4. Truy cập Airflow Web UI
- URL: http://localhost:8080
- Username: admin
- Password: admin123

## 📁 Cấu trúc thư mục

```
dac_coder/
├── UAT-local/
│   ├── docker-compose.yml
│   ├── .env
│   ├── logs/          # Airflow logs
│   ├── plugins/       # Airflow plugins
│   └── config/        # Airflow config
├── advertising/
│   └── dag.py         # DAG files
└── other_folders/
    └── *.py           # Other DAG files
```

## 🔧 Cấu hình

### DAGs Location
- DAGs được mount từ: `../` (toàn bộ folder dac_coder)
- Path trong Airflow: `/opt/airflow/dags/dac_coder/`
- DAG `quote_and_hello_dag` sẽ có trong: `dac_coder/advertising/dag.py`

### Database
- PostgreSQL chạy trên port 5432
- Database: airflow
- User/Password: airflow/airflow

### Services
- **airflow-webserver**: Port 8080 (Web UI)
- **airflow-scheduler**: Lập lịch và chạy tasks
- **airflow-triggerer**: Xử lý async tasks
- **postgres**: Database backend

## 🛠️ Các lệnh hữu ích

### Kiểm tra logs
```bash
# Xem logs của service
docker-compose logs airflow-webserver
docker-compose logs airflow-scheduler

# Follow logs real-time
docker-compose logs -f airflow-scheduler
```

### Chạy Airflow CLI
```bash
# Vào container để chạy airflow commands
docker-compose exec airflow-webserver bash

# Hoặc chạy trực tiếp
docker-compose exec airflow-webserver airflow dags list
docker-compose exec airflow-webserver airflow tasks list quote_and_hello_dag
```

### Dừng và cleanup
```bash
# Dừng services
docker-compose down

# Dừng và xóa volumes (mất data)
docker-compose down -v

# Rebuild images
docker-compose build --no-cache
```

## 🐛 Troubleshooting

### Permission Issues
Nếu gặp lỗi permission, chạy:
```bash
# Linux/Mac
export AIRFLOW_UID=$(id -u)
echo "AIRFLOW_UID=$(id -u)" > .env

# Windows
echo "AIRFLOW_UID=50000" > .env
```

### DAG không xuất hiện
1. Kiểm tra DAG syntax: `python dac_coder/advertising/dag.py`
2. Xem logs: `docker-compose logs airflow-scheduler`
3. Refresh DAGs trong UI: Admin > DAGs > Refresh

### Database Connection Issues
```bash
# Reset database
docker-compose down -v
docker-compose up airflow-init
docker-compose up -d
```

## 📦 Dependencies

Nếu DAG cần thêm Python packages:
1. Tạo file `requirements.txt` trong folder dac_coder
2. Cập nhật `_PIP_ADDITIONAL_REQUIREMENTS` trong docker-compose.yml
3. Rebuild containers

## 🔗 Links hữu ích

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Compose for Airflow](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [DAG Writing Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)


