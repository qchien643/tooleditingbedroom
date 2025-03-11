
from snippet.extract_info_user.extractInfoUser import extractInfoUser
from snippet.generate_layout.generateLayout import generateLayout
from snippet.arrange_layout.arrangeLayout import arrangeLayout
import json 

def sort_by_type(data , priority_order):
   
    # Tạo một từ điển để ánh xạ các loại đồ vật (type) sang thứ tự ưu tiên của chúng
    priority_map = {type_: index for index, type_ in enumerate(priority_order)}
    
    # Hàm key cho sắp xếp: ánh xạ "type" sang thứ tự ưu tiên trong bảng
    def get_priority(item):
        return priority_map.get(item["type"], float('inf'))  # Trả về thứ tự ưu tiên của loại đồ vật
    
    # Sắp xếp từ điển data theo thứ tự ưu tiên của "type"
    sorted_data = sorted(data, key=get_priority)
    
    return sorted_data

with open("./data/vi_to_en_map.json" , "r" , encoding='utf-8') as file:
    vi_to_en_map = json.load(file)
with open("./data/type.json" , "r" , encoding="utf-8" ) as file : 
    data_type = json.load(file)
with open("./data/dimension.json" , "r" , encoding="utf-8" ) as file : 
    dimension = json.load(file)
with open("./data/distance.json" , "r" , encoding="utf-8" ) as file : 
    distance = json.load(file)
with open("./data/list_prio_type.json" , "r" , encoding="utf-8" ) as file : 
    prio = json.load(file)['priority']
oder_ways_sample_raw = []
for i in range(1, 11):
    with open(f"./data/oder_ways_sample/state_{i}.json" , "r" , encoding ="utf-8") as file:
        sample = json.load(file)
    oder_ways_sample_raw.append(sample)
oder_ways_sample = [sort_by_type(sample ,prio) for sample in oder_ways_sample_raw]

text = "tôi muốn xây phòng ngủ với một chiếc bàn hiện đại , một chiếc giường mới và một chiếc tủ to"

def generateDesign(prompt ) : 
    extracted_info = extractInfoUser(prompt)
    
    layout_raw = generateLayout(extracted_info ,data_type , vi_to_en_map , ATTR_DIR = r"./data/attr_sorted" ,samples = oder_ways_sample)
    
    # arrange_layout = arrangeLayout(layout_raw, dimension , distance , prio)
    
    return layout_raw


print(generateDesign(text))