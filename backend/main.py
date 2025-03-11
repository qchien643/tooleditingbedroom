from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS class
import json 

from testChecktypeofchatuser import * 


# default prompt = tôi muốn xây phòng ngủ với một chiếc bàn hiện đại , một chiếc giường mới và một chiếc tủ to

# NOTE : format of data from frontend""""
#      {
#         flag : flag ,
#         data : data
#     }
# ""

"""
 flag sending data from chatbot : "message"
 flag sending data from user : "flowchart"
 
 +format base on flag:
 
 -flag : "message" 
 --> {
        flag : <flag>,
        data : {
            prompt : <prompt>
        }
    }

-flag : "flowchart"
-->{
        flag : <flag>,
        data : {
            "room": {
                "floor": "tile",
                "wall": "brick",
                "dimension": [
                "5",
                "5",
                "5"
                ]
            },
            "furnitures": [
                {
                "type": "chair",
                "model": "gaming_chair",
                "placement": "BehindFurnitureRule table [] center | SameDirection table []"
                },
                {
                "type": "bed",
                "model": "bed_1",
                "placement": "NextToWallRule None ['E', 'S'] left | SameDirectionWall None ['E', 'S']"
                }
            ]
        }
    }
"""

        

def dispatcher(datas):
    flag , data = datas["flag"] , datas["data"]
    if flag == 'message':
        promptUser = data[-1]["message"]
        type_of_mess = classify_type_of_mess(promptUser)
        res = {
            "flag" : flag ,
            "data" : type_of_mess
        }
        return res

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True, methods=["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"])

@app.route('/api/chat', methods=['GET', 'POST'])
def chat():
    try:
        data = request.get_json()
        
        res = dispatcher(data)  
        return jsonify(res)

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route("/api/refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    if data and data.get('flag') == "refresh":
        # Thực hiện logic reset / khởi tạo / đánh dấu "đã refresh" ...
        print("Client vừa gửi yêu cầu refresh!")
        resert_chat_history()
        
    return jsonify({"status": "OK", "message": "Refresh request received"})


if __name__ == '__main__':
    app.run(debug=True)

