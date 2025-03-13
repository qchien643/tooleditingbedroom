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
-status : "start" or "restart"
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