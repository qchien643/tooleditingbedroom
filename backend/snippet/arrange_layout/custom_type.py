import math
import numpy as np

def rotate_vector_y(vector, angle):
    """
    Xoay vector quanh trục y theo chiều kim đồng hồ.

    Parameters:
        vector (tuple): Vector ban đầu (x, y, z).
        angle (int): Góc xoay (đơn vị độ).

    Returns:
        tuple: Vector sau khi xoay.
    """
    x, y, z = vector
    angle_rad = math.radians(angle % 360)
    new_x = round(x * math.cos(angle_rad) + z * math.sin(angle_rad))
    new_y = y  # Trục y không thay đổi
    new_z = round(-x * math.sin(angle_rad) + z * math.cos(angle_rad))
    return (new_x, new_y, new_z)


def angle_between_vectors(A, B, axis=[0, 1, 0]):
    """
    Tính góc xoay theo chiều kim đồng hồ giữa hai vector A và B quanh trục axis.

    Parameters:
        A, B (array-like): Các vector (x, y, z).
        axis (array-like): Trục quay (mặc định [0,1,0]).

    Returns:
        int: Góc xoay (độ), đảm bảo chiều kim đồng hồ.
    """
    A, B, axis = np.array(A), np.array(B), np.array(axis)
    dot_product = np.dot(A, B)
    norm_A, norm_B = np.linalg.norm(A), np.linalg.norm(B)
    cos_theta = np.clip(dot_product / (norm_A * norm_B), -1.0, 1.0)
    theta_degrees = np.degrees(np.arccos(cos_theta))
    # Xác định chiều xoay thông qua tích có hướng
    cross_product = np.cross(A, B)
    if np.dot(cross_product, axis) > 0:
        theta_degrees = 360 - theta_degrees
    return int(theta_degrees)


def align_coordinate(base: float, base_size: float, obj_size: float, alignment: str) -> float:
    """
    Tính tọa độ căn chỉnh theo một trục dựa trên kiểu căn (left, center, right).

    Parameters:
        base (float): Tọa độ ban đầu (ví dụ: tọa độ x hoặc z của target).
        base_size (float): Kích thước của target trên trục đó.
        obj_size (float): Kích thước của đồ vật cần đặt trên cùng trục.
        alignment (str): Kiểu căn: "left", "center", "right".

    Returns:
        float: Tọa độ mới đã căn chỉnh.
    """
    if alignment == "left":
        return base
    elif alignment == "center":
        return base + (base_size - obj_size) / 2
    elif alignment == "right":
        return base + base_size - obj_size
    else:
        raise ValueError(f"Invalid alignment: {alignment}")


# --- Base Class cho các quy tắc đặt đồ ---
class PlacementRule:
    """Lớp cơ sở cho các quy tắc vị trí."""
    def apply(self, furniture, room):
        raise NotImplementedError("Subclasses must implement apply()")
    
    def get_target(self, room, target_type: str):
        """Trả về đối tượng target theo target_type trong room."""
        return next((obj for obj in room.placed_objects if obj.type == target_type), None)


# --- Quy tắc dựa trên đối tượng target ---
class RightOfFurnitureRule(PlacementRule):
    """
    Đặt đồ vật bên phải của một đồ vật target dựa trên hướng của đồ vật được đặt.
    
    Dựa vào furniture.direction, tính tọa độ:
      - Nếu direction là [0,0,-1]: đặt về phía phải theo trục x.
      - Nếu direction là [1,0,0]: đặt về phía phải theo trục z.
      - Nếu direction là [0,0,1]: đặt về bên trái theo trục x.
      - Nếu direction là [-1,0,0]: đặt về phía trái theo trục z.
    """
    def __init__(self, target_type: str, align: str = "left", distance: dict = None):
        self.target_type = target_type
        self.align = align
        self.distance = distance or {}

    def apply(self, furniture, room):
        target = self.get_target(room, self.target_type)
        if not target:
            print(f"Không tìm thấy {self.target_type} để đặt {furniture.type} bên phải.")
            return None

        tx, ty, tz = target.position
        tw, th, td = target.size
        fx, fy, fz = furniture.position
        fw, fh, fd = furniture.size
        direction = furniture.direction

        if direction == [0, 0, -1]:
            new_x = tx + tw
            new_z = align_coordinate(tz, td, fd, self.align)
        elif direction == [1, 0, 0]:
            new_z = tz + td
            new_x = align_coordinate(tx, tw, fw, self.align)
        elif direction == [0, 0, 1]:
            new_x = tx - fw
            new_z = align_coordinate(tz, td, fd, self.align)
        elif direction == [-1, 0, 0]:
            new_z = tz - td
            new_x = align_coordinate(tx, tw, fw, self.align)
        else:
            new_x, new_z = fx, fz

        new_position = [new_x, fy, new_z]
        valid = room.is_position_valid(new_position, furniture.size)
        if valid:
            print(f"Đặt {furniture.type} tại {new_position} bên phải của {target.type}.")
        else:
            print(f"Vị trí {new_position} không hợp lệ để đặt {furniture.type} bên phải của {target.type}.")
        return new_position, valid


class LeftOfFurnitureRule(PlacementRule):
    """
    Đặt đồ vật bên trái của target dựa trên hướng của furniture.

    Đối với mỗi trường hợp furniture.direction:
      - [0,0,-1]: new_x = tx - fw.
      - [1,0,0]: new_z = tz - td.
      - [0,0,1]: new_x = tx + tw.
      - [-1,0,0]: new_z = tz + td.
    """
    def __init__(self, target_type: str, align: str = "left", distance: dict = None):
        self.target_type = target_type
        self.align = align
        self.distance = distance or {}

    def apply(self, furniture, room):
        target = self.get_target(room, self.target_type)
        if not target:
            print(f"Không tìm thấy {self.target_type} để đặt {furniture.type} bên trái.")
            return None

        tx, ty, tz = target.position
        tw, th, td = target.size
        fx, fy, fz = furniture.position
        fw, fh, fd = furniture.size
        direction = furniture.direction

        if direction == [0, 0, -1]:
            new_x = tx - fw
            new_z = align_coordinate(tz, td, fd, self.align)
        elif direction == [1, 0, 0]:
            new_z = tz - td
            new_x = align_coordinate(tx, tw, fw, self.align)
        elif direction == [0, 0, 1]:
            new_x = tx + tw
            new_z = align_coordinate(tz, td, fd, self.align)
        elif direction == [-1, 0, 0]:
            new_z = tz + td
            new_x = align_coordinate(tx, tw, fw, self.align)
        else:
            new_x, new_z = fx, fz

        new_position = [new_x, fy, new_z]
        valid = room.is_position_valid(new_position, furniture.size)
        if valid:
            print(f"Đặt {furniture.type} tại {new_position} bên trái của {target.type}.")
        else:
            print(f"Vị trí {new_position} không hợp lệ để đặt {furniture.type} bên trái của {target.type}.")
        return new_position, valid


class InFrontOfFurnitureRule(PlacementRule):
    """
    Đặt đồ vật phía trước target dựa trên target.direction.

    Ví dụ:
      - Nếu target.direction == [0,0,-1]:
          new_z = tz - fd, new_x căn chỉnh theo target.width.
    """
    def __init__(self, target_type: str, align: str = "left", distance: dict = None):
        self.target_type = target_type
        self.align = align
        self.distance = distance or {}

    def apply(self, furniture, room):
        target = self.get_target(room, self.target_type)
        if not target:
            print(f"Không tìm thấy {self.target_type} để đặt {furniture.type} phía trước.")
            return None

        tx, ty, tz = target.position
        tw, th, td = target.size
        fx, fy, fz = furniture.position
        fw, fh, fd = furniture.size
        direction = target.direction

        if direction == [0, 0, -1]:
            new_z = tz - fd
            new_x = align_coordinate(tx, tw, fw, self.align)
        elif direction == [1, 0, 0]:
            new_x = tx + tw
            new_z = align_coordinate(tz, td, fd, self.align)
        elif direction == [0, 0, 1]:
            new_z = tz + td
            new_x = align_coordinate(tx, tw, fw, self.align)
        elif direction == [-1, 0, 0]:
            new_x = tx - fw
            new_z = align_coordinate(tz, td, fd, self.align)
        else:
            new_x, new_z = fx, fz

        new_position = [new_x, fy, new_z]
        valid = room.is_position_valid(new_position, furniture.size)
        return new_position, valid


class BehindFurnitureRule(PlacementRule):
    """
    Đặt đồ vật phía sau target dựa trên target.direction.

    Ví dụ:
      - Nếu target.direction == [0,0,-1]:
          new_z = tz + td, new_x căn chỉnh theo target.width.
    """
    def __init__(self, target_type: str, align: str = "left", distance: dict = None):
        self.target_type = target_type
        self.align = align
        self.distance = distance or {}

    def apply(self, furniture, room):
        target = self.get_target(room, self.target_type)
        if not target:
            print(f"Không tìm thấy {self.target_type} để đặt {furniture.type} phía sau.")
            return None

        tx, ty, tz = target.position
        tw, th, td = target.size
        fx, fy, fz = furniture.position
        fw, fh, fd = furniture.size
        direction = target.direction

        if direction == [0, 0, -1]:
            new_z = tz + td
            new_x = align_coordinate(tx, tw, fw, self.align)
        elif direction == [1, 0, 0]:
            new_x = tx - fw
            new_z = align_coordinate(tz, td, fd, self.align)
        elif direction == [0, 0, 1]:
            new_z = tz - fd
            new_x = align_coordinate(tx, tw, fw, self.align)
        elif direction == [-1, 0, 0]:
            new_x = tx + tw
            new_z = align_coordinate(tz, td, fd, self.align)
        else:
            new_x, new_z = fx, fz

        new_position = [new_x, fy, new_z]
        valid = room.is_position_valid(new_position, furniture.size)
        return new_position, valid


class OnAboveFurnitureRule(PlacementRule):
    """
    Đặt đồ vật ngay trên target (y = target.y + target.height) và căn chỉnh theo target.direction.
    """
    def __init__(self, target_type: str, align: str, distance: dict = None):
        self.target_type = target_type
        self.align = align
        self.distance = distance or {}

    def apply(self, furniture, room):
        target = self.get_target(room, self.target_type)
        if not target:
            print(f"Không tìm thấy {self.target_type} để đặt {furniture.type} trên {self.target_type}.")
            return None

        tx, ty, tz = target.position
        tw, th, td = target.size
        fx, fy, fz = furniture.position
        fw, fh, fd = furniture.size

        # Đặt y ngay trên target
        new_y = ty + th

        direction = target.direction
        if direction == [0, 0, -1]:
            new_x = tx
            new_z = align_coordinate(tz, td, fd, self.align)
        elif direction == [1, 0, 0]:
            new_z = tz
            new_x = align_coordinate(tx, tw, fw, self.align)
        elif direction == [0, 0, 1]:
            new_x = tx + tw - fw
            new_z = align_coordinate(tz, td, fd, self.align)
        elif direction == [-1, 0, 0]:
            new_z = tz + td - fd
            new_x = align_coordinate(tx, tw, fw, self.align)
        else:
            new_x, new_z = fx, fz

        new_position = [new_x, new_y, new_z]
        valid = room.is_position_valid(new_position, furniture.size)
        return new_position, valid


class UnderFurnitureRule(PlacementRule):
    """
    Đặt đồ vật ngay dưới target (y = target.y - furniture.height) và căn chỉnh theo furniture.direction.
    """
    def __init__(self, target_type: str, align: str, distance: dict = None):
        self.target_type = target_type
        self.align = align
        self.distance = distance or {}

    def apply(self, furniture, room):
        target = self.get_target(room, self.target_type)
        if not target:
            print(f"Không tìm thấy {self.target_type} để đặt {furniture.type} dưới {self.target_type}.")
            return None

        tx, ty, tz = target.position
        tw, th, td = target.size
        fx, fy, fz = furniture.position
        fw, fh, fd = furniture.size

        new_y = ty - fh  # Đặt ngay dưới target

        direction = furniture.direction
        if direction == [0, 0, -1]:
            new_z = align_coordinate(tz, td, fd, self.align)
            new_x = fx
        elif direction == [1, 0, 0]:
            new_x = align_coordinate(tx, tw, fw, self.align)
            new_z = fz
        elif direction == [0, 0, 1]:
            new_z = align_coordinate(tz, td, fd, self.align)
            new_x = fx
        elif direction == [-1, 0, 0]:
            new_x = align_coordinate(tx, tw, fw, self.align)
            new_z = fz
        else:
            new_x, new_z = fx, fz

        new_position = [new_x, new_y, new_z]
        valid = room.is_position_valid(new_position, furniture.size)
        return new_position, valid


# --- Quy tắc dựa trên tường ---
class NextToWallRule(PlacementRule):
    """
    Đặt đồ vật cạnh tường dựa trên danh sách kí hiệu hướng.
    Map:
      N: [0,0,-1], E: [1,0,0], S: [0,0,1], W: [-1,0,0]
    Nếu đặt cạnh 2 tường, vật nằm ở góc.
    """
    def __init__(self, direc_walls_sign):
        self.direc_walls_signs = direc_walls_sign
        self.sign_to_vector_map = {
            "N": [0, 0, -1],
            "E": [1, 0, 0],
            "S": [0, 0, 1],
            "W": [-1, 0, 0]
        }
        # Chuyển các kí hiệu thành vector
        self.direc_walls = [self.sign_to_vector_map[sign] for sign in self.direc_walls_signs]

    def apply(self, furniture, room):
        wR, hR, dR = room.width, room.height, room.depth
        x, y, z = furniture.position
        wF, hF, dF = furniture.size

        for direc in self.direc_walls:
            if direc == [0, 0, -1]:  # Tường phía trước
                z = 0
            elif direc == [1, 0, 0]:  # Tường phải
                x = wR - wF
            elif direc == [0, 0, 1]:  # Tường phía sau
                z = dR - dF
            elif direc == [-1, 0, 0]:  # Tường trái
                x = 0

        new_position = [x, y, z]
        if not room.is_position_valid(new_position, furniture.size):
            print("Lỗi: Vị trí đặt không hợp lệ theo tường.")
            return new_position, False
        return new_position, True


class InCenterWall(PlacementRule):
    """
    Đặt đồ vật ở trung tâm của tường chỉ định.
    Cũng xác định góc xoay cho mô hình dựa trên hướng tường.
    """
    def __init__(self, direc_walls_sign, inner_wall=False):
        self.direc_walls_sign = direc_walls_sign
        self.sign_to_vector_map = {
            "N": [0, 0, -1],
            "E": [1, 0, 0],
            "S": [0, 0, 1],
            "W": [-1, 0, 0]
        }
        self.wall_vector = self.sign_to_vector_map[self.direc_walls_sign]

    def apply(self, furniture, room):
        wR, hR, dR = room.width, room.height, room.depth
        x, y, z = furniture.position
        wF, hF, dF = furniture.size
        direc = self.wall_vector

        if direc == [0, 0, -1]:
            z = 0
            x = wR / 2 - wF / 2
        elif direc == [1, 0, 0]:
            x = wR - wF
            z = dR / 2 - dF / 2
        elif direc == [0, 0, 1]:
            z = dR - dF
            x = wR / 2 - wF / 2
        elif direc == [-1, 0, 0]:
            x = 0
            z = dR / 2 - dF / 2

        new_position = [x, y, z]
        if not room.is_position_valid(new_position, furniture.size):
            print("Lỗi: Vị trí trung tâm tường không hợp lệ.")
            return new_position, False
        return new_position, True


# --- Quy tắc điều chỉnh hướng ---
class SameDirection(PlacementRule):
    """Lấy hướng giống như của target."""
    def __init__(self, target_type: str):
        self.target_type = target_type

    def apply(self, furniture, room):
        target = self.get_target(room, self.target_type)
        if not target:
            print(f"Không tìm thấy {self.target_type} để lấy hướng cho {furniture.type}.")
            return None
        return target.direction


class OppositeDirection(PlacementRule):
    """Lấy hướng đối ngược với target."""
    def __init__(self, target_type: str):
        self.target_type = target_type

    def apply(self, furniture, room):
        target = self.get_target(room, self.target_type)
        if not target:
            print(f"Không tìm thấy {self.target_type} để lấy hướng đối ngược cho {furniture.type}.")
            return None
        return [-d for d in target.direction]


class PerpendicularPositive(PlacementRule):
    """Tính hướng vuông góc (xoay 270°) với hướng của target."""
    def __init__(self, target_type: str):
        self.target_type = target_type

    def apply(self, furniture, room):
        target = self.get_target(room, self.target_type)
        if not target:
            print(f"Không tìm thấy {self.target_type} để tính hướng vuông góc cho {furniture.type}.")
            return None
        return rotate_vector_y(target.direction, 270)


class PerpendicularNegative(PlacementRule):
    """Tính hướng vuông góc (xoay 90°) với hướng của target."""
    def __init__(self, target_type: str):
        self.target_type = target_type

    def apply(self, furniture, room):
        target = self.get_target(room, self.target_type)
        if not target:
            print(f"Không tìm thấy {self.target_type} để tính hướng vuông góc cho {furniture.type}.")
            return None
        return rotate_vector_y(target.direction, 90)


class OppostieDirectionWall(PlacementRule):
    """Lấy hướng đối ngược với hướng tường được chỉ định."""
    def __init__(self, direc_walls_sign: str):
        self.direc_walls_sign = direc_walls_sign
        self.sign_to_vector_map = {
            "N": [0, 0, -1],
            "E": [1, 0, 0],
            "S": [0, 0, 1],
            "W": [-1, 0, 0]
        }
        self.wall_vector = self.sign_to_vector_map[self.direc_walls_sign]

    def apply(self, furniture, room):
        return [-d for d in self.wall_vector]


class SameDirectionWall(PlacementRule):
    """Lấy hướng giống với hướng tường được chỉ định."""
    def __init__(self, direc_walls_sign: str):
        self.direc_walls_sign = direc_walls_sign
        self.sign_to_vector_map = {
            "N": [0, 0, -1],
            "E": [1, 0, 0],
            "S": [0, 0, 1],
            "W": [-1, 0, 0]
        }
        self.wall_vector = self.sign_to_vector_map[self.direc_walls_sign]

    def apply(self, furniture, room):
        return self.wall_vector
