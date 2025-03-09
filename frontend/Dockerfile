# Sử dụng Node.js image
FROM node:18-alpine

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép file package.json và package-lock.json trước để cài đặt dependencies
COPY package.json package-lock.json ./

# Cài đặt dependencies
RUN npm install --legacy-peer-deps

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Mở cổng 5173 (Vite mặc định), hoặc có thể thay đổi tùy vào config
EXPOSE 5173

# Chạy Vite ở chế độ development
CMD ["npm", "run", "dev", "--", "--host"]
