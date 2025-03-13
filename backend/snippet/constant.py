
# VI_TO_EN_MAP_PATH = "vi_to_en_map.json"
DATA_TYPE_PATH = "type.json"
DISTANCE_PATH  = "distance.json"
PRIORITI_PATH = "list_prio_type.json"
DIMENSION_PATH = "dimension.json"

from snippet.ultis.ultis import get_data_path,load_json
# VI_TO_EN_MAP = load_json(get_data_path(VI_TO_EN_MAP_PATH))
DATA_TYPE = load_json(get_data_path(DATA_TYPE_PATH))
DIMENSION = load_json(get_data_path(DIMENSION_PATH))
DISTANCE = load_json(get_data_path(DISTANCE_PATH))
PRIORITI = load_json(get_data_path(PRIORITI_PATH))

priorityQueue = ["bed" , "table" , "chair" , "wardrobe" ]
ROOMSIZE = 5

from snippet.arrange_layout.relation import *
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