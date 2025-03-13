from relation import *
import json
from snippet.constant import DIMENSION, type_to_class_map ,DISTANCE

"""
    This class is used to generate the relation between objects in the scene.
    input sample : 
    {
    'flag': 'flowchart',
    'status': 'start',
    'data': {
        'room': {
            'floor': 'wood',
            'wall': 'brick',
            'dimension': ['5', '5', '5']
        },
        'furnitures': [
            {
                'type': 'chair',
                'model': 'fly_dinner_chair',
                'placement': [0]
            },
            {
                'type': 'chair',
                'model': 'fly_dinner_chair',
                'placement': [0]
            },
            {
                'type': 'chair',
                'model': 'gaming_chair',
                'placement': [0]
            }
        ]
    }
}
data is list funitures
"""

# def __init__(self, name , dimension ,distance  ):
def extract_data_frontend(data ):
    dataSendFront = {"posible_to_place" : [] , "impossible_to_place" : [] }
    
    room = Room((5, 5, 5))
    for item in data:
        
        
        w = float(DIMENSION[item["model"]]["width"])
        h = float(DIMENSION[item["model"]]["height"])
        d = float(DIMENSION[item["model"]]["depth"])
        
        obj = type_to_class_map[item["type"]](
            name = item["model"], 
            dimension = (w ,h,d),
            distance = DISTANCE
        )
        # try :
        #     possible_to_place = obj.apply_placement_rule([obj.placement_rules[i] for i in item["oders"]] , room)
        #     if possible_to_place:
        #         room.add_object(obj)
        #     else: 
        
        #         dataSendFront["impossible_to_place"].append(item["model"])# Không thể đặt
        # except :
        #     print("debug "+ item["model"])
        #     dataSendFront["impossible_to_place"].append(item["model"])
        
        possible_to_place = obj.apply_placement_rule([obj.placement_rules[i] for i in item["placement"]] , room)
        if possible_to_place:
            room.add_object(obj)
        else: 
            dataSendFront["impossible_to_place"].append(item["model"])# Không thể đặt
        
        dataSendFront["posible_to_place"] = room.export_room()
    return dataSendFront

data = [
            {
                'type': 'bed',
                'model': 'bed_1',
                'placement': [2]
            },

        ]
    

print(extract_data_frontend(data))
