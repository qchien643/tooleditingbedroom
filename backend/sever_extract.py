from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS class
import json 

from snippet import relation, custom_type, extractInfoUser, generateLayout


# from snippet.arrange_layout import relation
# from snippet.arrange_layout import custom_type
# from snippet.arrange_layout import *
# from snippet.extract_info_user.extractInfoUser import extractInfoUser
# from snippet.generate_layout.generateLayout import generateLayout

def sort_by_type(data , priority_order ):
   
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



#preapre data
list_type_name= [c.__name__ for c in relation.Furniture.__subclasses__()]
def extract_ways_to_oder():
    oders_dict = {}
    for type in relation.Furniture.__subclasses__():
        obj = type("test" , (0,0,0) , distance)
        oders_dict[obj.type] = obj.oder_ways
    return oders_dict

# Convert and write JSON object to file
with open("sample.json", "w") as outfile: 
    json.dump(extract_ways_to_oder(), outfile )

user_message_current = {'flag': 'apply', 'data': [{'type': 'bed', 'model_name': 'bed_1', 'oders': [0]}, {'type': 'chair', 'model_name': 'fly_dinner_chair', 'oders': [0]}, {'type': 'door', 'model_name': 'door_with_cardreader', 'oders': [2]}, {'type': 'table', 'model_name': 'desk', 'oders': [0]}, {'type': 'wardrobe', 'model_name': 'celestine_four_door_wardrobeobj', 'oders': [0]}]}
print(extract_data_frontend(sort_by_type(user_message_current["data"]) , dimension , distance))


# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True, methods=["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"])

# # default prompt = tôi muốn xây phòng ngủ với một chiếc bàn hiện đại , một chiếc giường mới và một chiếc tủ to

# @app.route('/api/chat', methods=['GET', 'POST'])
# def chat():
#     try:
#         data = request.get_json()
#         user_messages = data
#         user_message_current = user_messages
        
#         data_front = {}
#         # set user_message_current following { type: 'user', text: inputValue }
#          # dataSendBack = {"flag" : "apply" , "dataReturn" : dataReturn};
#         if user_message_current["flag"] == 'upload':
#             botRespone = extract_ways_to_oder()
#             data_front =  {'oders': botRespone , 'model_names' : data_type}
#         elif user_message_current["flag"] == 'apply':
#             # print(sort_by_type(user_message_current["data"]))
#             # [{'type': 'bed', 'model_name': 'bed_1', 'oders': [1, 3]}]
#             data_front = extract_data_frontend(sort_by_type(user_message_current["data"] ,prio) , dimension ,distance)
#             print(data_front)
#         elif user_message_current["flag"] == 'answer':
#             data = user_message_current["text"]
#             print("debug" + str(data))
#             extracted_info = extractInfoUser(data)
#             layout = generateLayout(extracted_info ,data_type , vi_to_en_map , ATTR_DIR = r"./data/attr_sorted" ,samples = oder_ways_sample)
#             data_front = extract_data_frontend(sort_by_type(layout , prio) , dimension ,distance)
#             print("debug "+ str(data_front))    
#         return jsonify(data_front)

#     except Exception as e:
#         print(f"Error processing request: {str(e)}")
#         return jsonify({'error': 'Internal Server Error'}), 500


# if __name__ == '__main__':
#     app.run(debug=True)

