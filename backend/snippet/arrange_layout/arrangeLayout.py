from .custom_type import * 
from .relation import *
import json 

type_to_classObj_map = {
    "bed" : Bed,
    "table" : Table,
    "wardrobe" : Wardrobe,
    "chair" : Chair,
}


# because bed is the root of placing obj , we need to process with bed first
def sort_obj_by_type(dict_to_sort , prio):
    sorted_dict = {key: dict_to_sort[key] for key in prio if key in dict_to_sort}
    return sorted_dict



# layout folowing as {'table': 'table', 'bed': 'poliform_bed', 'wardrobe': 'wardrobe_low_poly'} 
def arrangeLayout(layout_raw , dimension , distance ,priority , ROOM_SIZE = [5,5,5]):
    dict = []
    layout = sort_obj_by_type(layout_raw , priority)
    room = Room(ROOM_SIZE )
    for key , value in layout.items():
        
        width = float(dimension[value]["width"])
        height = float(dimension[value]["height"])
        depth = float(dimension[value]["depth"])
        
        # create Furniture object
        obj =  type_to_classObj_map[key](value , (width , height , depth) , distance)
        
        if obj.type == "bed":
            room.add_object(obj)
            continue
        
        print(obj.type)
        res = obj.apply_placement_rule(obj.placement_rules[0] , room)
    
        if res : 
            pos , direc , size= res
            obj.position = pos
            obj.direction = direc
            obj.size = size
            room.add_object(obj) 
        
    for obj in room.export_pos():
        dict.append({obj[0] : {
            "position" : obj[1],
            "direction" : obj[2],
        }})
    return dict

        




