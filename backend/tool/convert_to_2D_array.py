import os
import shutil

# Đường dẫn đến folder A
folder_A = "./model3D"
# Đường dẫn đến folder mới để chứa các folder C
folder_moi = "./model3D_extract"

# Tạo folder mới nếu chưa tồn tại
os.makedirs(folder_moi, exist_ok=True)

# Duyệt qua từng folder B trong folder A
for folder_B in os.listdir(folder_A):
    path_B = os.path.join(folder_A, folder_B)
    
    # Kiểm tra nếu đó là folder
    if os.path.isdir(path_B):
        # Duyệt qua từng folder C trong folder B
        for folder_C in os.listdir(path_B):
            path_C = os.path.join(path_B, folder_C)
            
            # Kiểm tra nếu đó là folder C
            if os.path.isdir(path_C):
                # Copy folder C vào folder mới
                dest_path = os.path.join(folder_moi, folder_C)
                
                # Đảm bảo tên folder C không bị trùng, nếu có trùng sẽ thêm hậu tố để tránh ghi đè
                if os.path.exists(dest_path):
                    count = 1
                    while os.path.exists(f"{dest_path}_{count}"):
                        count += 1
                    dest_path = f"{dest_path}_{count}"
                
                shutil.copytree(path_C, dest_path)
                print(f"Đã copy {path_C} đến {dest_path}")
