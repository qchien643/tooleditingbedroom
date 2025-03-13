from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS class
import json 

from testChecktypeofchatuser import * 

def extractInfoUser(prompt) :
    pass
        
def dispatcher(datas):
    flag , data , status = datas["flag"] , datas["data"] , datas["status"]
    
    if flag == 'message':
        promptUser = data[-1]["message"]
        type_of_mess = classify_type_of_mess(promptUser)
        res = {
            "flag" : flag ,
            "data" : type_of_mess
        }
        return res
    
    elif flag == 'flowchart':
        
        if status == "start" :
            print(datas)
            res = {"flag" : flag , "status" : status , "data" :"hi"}
            
        elif status == "restart": pass

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

