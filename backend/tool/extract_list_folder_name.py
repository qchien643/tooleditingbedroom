import os

# Đường dẫn đến thư mục chứa các file zip
folder_path = '../data/model_unextract'

# Lấy tất cả các file trong thư mục
files_in_folder = os.listdir(folder_path)

# Lọc và in ra tên của các file zip
zip_files = [file[:-4] for file in files_in_folder if file.endswith('.zip')]
print(zip_files)
