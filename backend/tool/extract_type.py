import os
import json

def get_folder_structure(parent_folder_path):
    """
    Duyệt qua thư mục cha và tạo dictionary với cấu trúc:
    {folder B: [list of folder C names]}
    
    Args:
        parent_folder_path (str): Đường dẫn tới thư mục cha.
    
    Returns:
        dict: Dictionary chứa các thư mục con B và các thư mục con C của nó.
    """
    result = {}
    
    # Duyệt qua các thư mục con trong thư mục cha
    for folder_b in os.listdir(parent_folder_path):
        folder_b_path = os.path.join(parent_folder_path, folder_b)
        
        # Kiểm tra xem folder_b có phải là thư mục không
        if os.path.isdir(folder_b_path):
            folder_c_list = []
            
            # Duyệt qua các thư mục con trong folder B (tìm folder C)
            for folder_c in os.listdir(folder_b_path):
                folder_c_path = os.path.join(folder_b_path, folder_c)
                
                # Nếu folder_c là một thư mục thì thêm vào list
                if os.path.isdir(folder_c_path):
                    folder_c_list.append(folder_c)
            
            # Thêm vào dictionary
            result[folder_b] = folder_c_list
    
    return result

def save_structure_to_json(structure, filename):
    """
    Lưu cấu trúc vào một file JSON.
    
    Args:
        structure (dict): Cấu trúc cần lưu.
        filename (str): Tên file JSON muốn lưu.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=4)

# Ví dụ sử dụng
parent_folder_path = '../model3D'  # Thay 'path/to/parent_folder' bằng đường dẫn thực tế
folder_structure = get_folder_structure(parent_folder_path)

# Lưu cấu trúc vào file JSON
json_filename = 'type.json'  # Tên file JSON cần lưu
save_structure_to_json(folder_structure, json_filename)

print(f"Cấu trúc đã được lưu vào file {json_filename}")
