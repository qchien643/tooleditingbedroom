from snippet.arrange_layout.custom_type import *

class Room:
    def __init__(self,dimension):
        self.width ,self.height , self.depth = dimension
        self.placed_objects = []

    def is_within_bounds(self, position, size):
        x, y, z = position
        dx, dy, dz = size
        return (0 <= x <= self.width - dx and
                0 <= y <= self.height - dy and
                0 <= z <= self.depth - dz)

    def is_position_valid(self, position, size):
        if not self.is_within_bounds(position, size):
            print(f"Vị trí {position} không nằm trong giới hạn phòng.")
            return False

        for obj in self.placed_objects:
            if obj.type == "rug" : continue
            if obj.check_overlap(position, size):
                print(f"Vị trí {position} cua {obj.type} chồng chéo với {obj.type} tại vị trí {obj.position}.")
                return False
        return True

    def add_object(self, furniture):
        self.placed_objects.append(furniture)
        
    def export_room(self ):
        exportList = []
        for obj in self.placed_objects:
            
            exportList.append([ obj.name ,obj.position ,obj.orientation  ])
        return exportList


class Furniture:
    def __init__(self,name, type, dimension ):
        self.name = name
        self.type = type
        self.width , self.height ,self.depth = dimension
        self.size = (self.width, self.height,self.depth)
        self.position = [0,0,0]
        self.direction = [0,0,-1]
        self.default_direction = [0,0,-1]
        self.placement_rules = []
        self.oder_ways = []
        self.rotation_rules = []
        self.orientation   = 0
        
        # oders to place
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["N" , "W"] ,rotateRule=SameDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["N","E"] ,rotateRule=SameDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["E","N"] ,rotateRule=SameDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["E","S"] ,rotateRule=SameDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["S","E"] ,rotateRule=SameDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["S","W"] ,rotateRule=SameDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["W","N"] ,rotateRule=SameDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["W","S"] ,rotateRule=SameDirectionWall  )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["N"] ,rotateRule=SameDirectionWall  )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["E"] ,rotateRule=SameDirectionWall )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["S"] ,rotateRule=SameDirectionWall )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["W"] ,rotateRule=SameDirectionWall  )

   
    
    def add_placement_rule(self , rule, align = "left" , wall_signs = [] , target_type_pos = None ,target_type_rotate = None , distance=0 , rotateRule = None   ):
         
        self.oder_ways.append([f"{rule.__name__} {target_type_pos} {wall_signs} {align}",f"{rotateRule.__name__} {target_type_rotate} {wall_signs}"])
       
        if target_type_pos and target_type_rotate:
            self.placement_rules.append([rule(target_type = target_type_pos,align = align , distance = distance) , rotateRule(target_type_rotate) ])
            
        elif not target_type_pos and  target_type_rotate:
            self.placement_rules.append([rule(direc_walls_sign = wall_signs[0]),rotateRule(target_type_rotate)])
            
        elif target_type_pos and not target_type_rotate:
            self.placement_rules.append([rule(target_type =target_type_pos,align = align , distance = distance) , rotateRule(wall_signs[0])])
        elif not target_type_pos and not target_type_rotate:
            if rule == NextToWallRule :
                self.placement_rules.append([rule(direc_walls_sign =wall_signs),rotateRule(wall_signs[0])])
            elif rule == InCenterWall :
                self.placement_rules.append([rule(direc_walls_sign =wall_signs[0]),rotateRule(wall_signs[0])])
               
        

    def apply_placement_rule(self, placement_rules , room ):
        
        for id , placement_rule in enumerate(placement_rules):
            default_direc = self.direction
            rule , rotate = placement_rule
            print("current" + str(self.type) + " " + str(rule) + " " + str(rotate))
            print("current rotate" + str(rotate))
            # print("expected rotate" + str(rotate_vector_y([])))
            new_direc = rotate.apply(self,room)
            print("new_direc" + str(new_direc))
            self.change_direction(new_direc)
            self.orientation   = angle_between_vectors(self.default_direction , self.direction)
            new_pos , is_possible_place = rule.apply(self, room)
            print(new_pos)
            if (not is_possible_place) and id == len(placement_rules) -1 : 
                self.change_direction(default_direc)
                print(str(new_pos) + " " + "loi")
                return False  
             
            self.position = new_pos
           
        return True
    
    def change_direction(self , direc):
        # self.direction = direc
        angel = angle_between_vectors(self.direction , direc)

        w,h,d = self.size
        size = (w , h ,d)
        # do vật chỉ xoay một góc chia hết 90 nên chỉ có hai trường hợp là kích thước giữ nguyên hoặc chiều dài và chiều sâu hoán đổi 
        if angel in [90 , 270]:
            size = (d,h,w)
        self.size = size
        self.direction = direc
            

    def check_overlap(self, other_position, other_size):
        x1, y1, z1 = self.position
        dx1, dy1, dz1 = self.size
        x2, y2, z2 = other_position
        dx2, dy2, dz2 = other_size

        overlap_x = (x1 < x2 + dx2) and (x2 < x1 + dx1)
        overlap_y = (y1 < y2 + dy2) and (y2 < y1 + dy1)
        overlap_z = (z1 < z2 + dz2) and (z2 < z1 + dz1)
        
        return overlap_x and overlap_y and overlap_z

class Bed(Furniture):
    def __init__(self, name , dimension ,distance  ):
        super().__init__( name , "bed" ,dimension)



class Table(Furniture):
    def __init__(self,name , dimension, distance):
        super().__init__(name , "table",dimension)
        # Đặt khoảng cách riêng cho từng quy tắc
        self.add_placement_rule(rule = RightOfFurnitureRule, target_type_pos="bed",target_type_rotate ="bed" , distance=distance["table"]["bed"]["right"] ,rotateRule=SameDirection  )
        self.add_placement_rule(rule=LeftOfFurnitureRule,target_type_pos= "bed" ,target_type_rotate ="bed" ,distance=distance["table"]["bed"]["left"] ,rotateRule=SameDirection)

class Chair(Furniture):
    def __init__(self,name , dimension, distance ):
        super().__init__(name , "chair",dimension)
        self.placement_rules = []
        self.oder_ways = []
        self.add_placement_rule(rule=BehindFurnitureRule,align="center" , target_type_pos="table" ,target_type_rotate ="table" , distance=distance["wardrobe"]["table"]["behind"] ,rotateRule=SameDirection)
        
class Wardrobe(Furniture):
    def __init__(self,name , dimension, distance ):
        super().__init__(name , "wardrobe",dimension)
        self.direction = [0,0,1]
        self.default_direction = [0,0,1]

        self.placement_rules = []
        self.oder_ways = []
        
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["N" , "W"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["N","E"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["E","N"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["E","S"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["S","E"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["S","W"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["W","N"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["W","S"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["N"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["E"] ,rotateRule=OppostieDirectionWall )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["S"] ,rotateRule=OppostieDirectionWall )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["W"] ,rotateRule=OppostieDirectionWall  )

        # Đặt khoảng cách riêng cho từng quy tắc
        self.add_placement_rule(rule = BehindFurnitureRule ,target_type_pos="bed" , target_type_rotate ="bed" ,distance=distance["wardrobe"]["bed"]["behind"] , rotateRule=PerpendicularPositive)
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["E" ,"S"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["W" , "S"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["N"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["E"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["S"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["W"] ,rotateRule=OppostieDirectionWall  )
        

class Door(Furniture):
    def __init__(self,name , dimension, distance ):
        super().__init__(name , "door",dimension)


class Window(Furniture):
    def __init__(self,name , dimension, distance ):
        super().__init__(name , "window",dimension)
        self.placement_rules = []
        self.oder_ways = []
        self.position = [0,5/2 - self.height/2,0]
        self.add_placement_rule(rule= OnAboveFurnitureRule , target_type_pos="bed" ,target_type_rotate="bed" ,rotateRule=OppositeDirection)
        self.add_placement_rule(rule= OnAboveFurnitureRule , target_type_pos="table" ,target_type_rotate="table" ,rotateRule=OppositeDirection)
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["W" ] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["E"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["S"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=NextToWallRule , wall_signs=["N"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["N"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["E"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["S"] ,rotateRule=OppostieDirectionWall  )
        self.add_placement_rule(rule=InCenterWall , wall_signs=["W"] ,rotateRule=OppostieDirectionWall  )

class Rug(Furniture):
    def __init__(self, name, dimension,distance):
        super().__init__(name, "rug", dimension)
        
        
        self.add_placement_rule(rule = RightOfFurnitureRule, target_type_pos="bed",target_type_rotate ="bed" , distance=distance["rug"]["bed"]["right"] ,rotateRule=PerpendicularPositive  )
        self.add_placement_rule(rule=LeftOfFurnitureRule,target_type_pos= "bed" ,target_type_rotate ="bed" ,distance=distance["rug"]["bed"]["left"] ,rotateRule=PerpendicularPositive)
        self.add_placement_rule(rule=BehindFurnitureRule,target_type_pos= "bed" ,target_type_rotate ="bed" ,distance=distance["rug"]["bed"]["left"] ,rotateRule=SameDirection)
        self.add_placement_rule(rule=BehindFurnitureRule,target_type_pos= "door" ,target_type_rotate ="door" ,align="center" ,distance=distance["rug"]["bed"]["left"] ,rotateRule=SameDirection)
class DecorateFurniture(Furniture) :
    def __init__(self, name, dimension,distance):
        super().__init__(name, "decorateFurniture", dimension)       
