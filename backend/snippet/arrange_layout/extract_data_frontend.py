from .relation import *
import json
# distance = {
#     "bed": {
#         "bed": {"infrontup": 0, "behind": 0, "right": 0, "left": 0},
#         "table": {"infrontup": 0, "behind": 0, "right": 0, "left": 0},
#         "chair": {"infrontup": 0, "behind": 0, "right": 0, "left": 0},
#         "wardrobe": {"infrontup": 0, "behind": 0, "right": 0, "left": 0}
#     },
#     "table": {
#         "bed": {"infrontup": 0, "behind": 0, "right": 0, "left": 0},
#         "table": {"infrontup": 0, "behind": 0, "right": 0, "left": 0},
#         "chair": {"infrontup": 0, "behind": 0, "right": 0, "left": 0},
#         "wardrobe": {"infrontup": 0, "behind": 0, "right": 0, "left": 0}
#     },
#     "chair": {
#         "bed": {"infrontup": 0, "behind": 0, "right": 0, "left": 0},
#         "table": {"infrontup": 0, "behind": 0, "right": 0, "left": 0},
#         "chair": {"infrontup": 0, "behind": 0, "right": 0, "left": 0},
#         "wardrobe": {"infrontup": 0, "behind": 0, "right": 0, "left": 0}
#     },
#     "wardrobe": {
#         "bed": {"infrontup": 0, "behind": 0, "right": 0, "left": 0},
#         "table": {"infrontup": 0, "behind": 0, "right": 0, "left": 0},
#         "chair": {"infrontup": 0, "behind": 0, "right": 0, "left": 0},
#         "wardrobe": {"infrontup": 0, "behind": 0, "right": 0, "left": 0}
#     }
# }
# with open("../../data/dimension.json" , "r" , encoding="utf-8" ) as file : 
#     dimension = json.load(file)
# # [{'type': 'bed', 'model_name': 'bed_1', 'oders': [1, 3]}]
# data = [{'type': 'bed', 'model_name': 'bed_1', 'oders': [1]}]

type_to_class_map = {
    "bed" : Bed,
    "chair" : Chair,
    "decorateFurniture" : DecorateFurniture,
    "door" : Door,
    "rug" : Rug ,
    "table" : Table,
    "wardrobe" : Wardrobe,
    "window" : Window
    
}
# def __init__(self, name , dimension ,distance  ):
def extract_data_frontend(data ,dimension , distance):
    dataSendFront = {"posible_to_place" : [] , "impossible_to_place" : [] }
    
    room = Room((5, 5, 5))
    for item in data:
        
        
        w = float(dimension[item["model_name"]]["width"])
        h = float(dimension[item["model_name"]]["height"])
        d = float(dimension[item["model_name"]]["depth"])
        
        obj = type_to_class_map[item["type"]](
            name = item["model_name"], 
            dimension = (w ,h,d),
            distance = distance
        )
        try :
            possible_to_place = obj.apply_placement_rule([obj.placement_rules[i] for i in item["oders"]] , room)
            if possible_to_place:
                room.add_object(obj)
            else: 
        
                dataSendFront["impossible_to_place"].append(item["model_name"])# Không thể đặt
        except :
            print("debug "+ item["model_name"])
            dataSendFront["impossible_to_place"].append(item["model_name"])
        dataSendFront["posible_to_place"] = room.export_room()
    return dataSendFront


    # bed = Bed("bed_1" , (2.27,1.51,2.42) , distance) 

    # possible_to_place = bed.apply_placement_rule([bed.placement_rules[0]] , room)
    # if possible_to_place:
    #     room.add_object(bed)
    # else: print("Không thể đặt")  # Không thể đặt

    # table = Table("desk" , (1.47,0.74,0.71) , distance)
    # possible_to_place = table.apply_placement_rule([table.placement_rules[3]] , room)
    # if possible_to_place:
    #     print(bed.direction)
    #     room.add_object(table)
    # else : print("Không thể đặt")  # Không thể đặt
