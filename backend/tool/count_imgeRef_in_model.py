import os

def count_files_in_subfolders(parent_folder):
    result = []
    
    # Duyệt qua tất cả các thư mục con trong thư mục cha
    for subfolder in os.listdir(parent_folder):
        subfolder_path = os.path.join(parent_folder, subfolder)
        
        # Kiểm tra xem đó có phải là thư mục không
        if os.path.isdir(subfolder_path):
            # Đếm số tệp trong thư mục con
            file_count = len([f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))])
            # Thêm vào mảng kết quả
            result.append({subfolder: file_count})
    
    return result

# Thay đổi đường dẫn tới thư mục cha của bạn
parent_folder_path = '../../geMark/public/ref_image'
result = count_files_in_subfolders(parent_folder_path)

# In kết quả
print(result)