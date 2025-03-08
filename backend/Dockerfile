# Sử dụng Python 3.9 làm base image
FROM python:3.9-slim

# Đặt thư mục làm việc bên trong container
WORKDIR /main

# Sao chép file requirements.txt trước để cài đặt dependencies trước
COPY requirements.txt .

# Cài đặt các dependencies từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sau đó sao chép toàn bộ mã nguồn backend vào container
COPY . .

# Mở cổng 5000
EXPOSE 5000

# Chạy ứng dụng Flask
CMD ["python", "main.py"]
