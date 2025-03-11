 

import json
import os
import random


def find_key(item_name , data_type):
    for key, items in data_type.items():
        if key == "_comment" : continue
        if item_name in items:
            return key
    return None


# Hàm đọc bảng xếp hạng thuộc tính từ file JSON
def load_attribute_ranking(attribute_name ,ATTR_DIR):
    file_path = os.path.join(ATTR_DIR, f"{attribute_name}.json")
    if not os.path.exists(file_path):
        attribute_name = "bình thường"
        file_path = os.path.join(ATTR_DIR, f"{attribute_name}.json")
        # raise ValueError(f"File xếp hạng thuộc tính '{attribute_name}' không tồn tại.")
    
    with open(file_path, 'r') as file:
        return json.load(file)

# Hàm chọn đồ vật có điểm thuộc tính cao nhất trong loại đồ vật
def get_best_item_by_attribute(item_type, attribute_name, data_type ,ATTR_DIR):
    # Kiểm tra xem loại đồ vật có tồn tại trong dữ liệu không
    if item_type not in data_type:
        return "Loại đồ vật không hợp lệ."
    
    # Lấy danh sách các mô hình trong loại đồ vật
    items = data_type[item_type]
    
    # Đọc bảng xếp hạng thuộc tính từ file JSON
    try:
        attribute_ranking = load_attribute_ranking(attribute_name , ATTR_DIR)
    except ValueError as e:
        return str(e)

    # Khởi tạo biến để theo dõi mô hình có điểm cao nhất
    best_item = None
    highest_score = -1  # Đảm bảo điểm bắt đầu thấp nhất
    
    # Duyệt qua các mô hình và tìm mô hình có điểm cao nhất
    for item in items:
        if item in attribute_ranking:
            score = attribute_ranking[item]
            if score > highest_score:
                highest_score = score
                best_item = item
    
    # Nếu không tìm thấy mô hình nào có điểm thuộc tính
    if best_item is None:
        return "Không có mô hình nào trong loại này có điểm thuộc tính."
    
    return best_item, highest_score


def find_matching_indexes(samples, selected_items):
    matching_indexes = []
    
    # Duyệt qua từng danh sách con trong samples
    for idx, sample_group in enumerate(samples):
        # Kiểm tra nếu có bất kỳ phần tử nào trong group khớp với model_name
        if any(item['model_name'] == selected_items.get(item['type'], "") for item in sample_group):
            matching_indexes.append(idx)
    
    return matching_indexes

def generateLayout(info, data_type, vi_to_en_map, ATTR_DIR, samples ):  
    layout = {}

    # Lấy thông tin về đồ vật
    for furniture in info.get("furnitures", []):
        for item_type_vi, attributes in furniture.items():
            amount = attributes.get("amount", "")
            
            # Kiểm tra điều kiện: số lượng khác rỗng và lớn hơn 0
            if amount and int(amount) > 0:
                item_type = vi_to_en_map.get(item_type_vi, item_type_vi)
                adjective = attributes.get("adjective", "")
                
                # Gọi hàm lấy đồ vật tốt nhất theo thuộc tính
                
                best_item_result = get_best_item_by_attribute(item_type, adjective, data_type, ATTR_DIR)

                if isinstance(best_item_result, str):
                    print(best_item_result)  # In ra thông báo lỗi nếu có
                else:
                    best_item, highest_score = best_item_result
                    layout[find_key(best_item, data_type)] = best_item

    matching_indexes = find_matching_indexes(samples, layout)
    random_item = random.choice(matching_indexes)
    
    return samples[random_item]


