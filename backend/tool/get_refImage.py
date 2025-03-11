import os

# Danh sách các tên
tname = [
  'bed_1',
  'bed_simple',
   'bhadoi_rug',
  'celestine_four_door_wardrobeobj',
  'desk', 

  'door_with_cardreader',


  'fly_dinner_chair',
   'folding_table', 
   'gaming_chair', 
   'ikea_markus_office_chair',
    'industrial_table', 
    'kuuma_ye_rug_by_kristiina_lassus', 
    'lewie_console_table', 
    'modern_door',
     'modern_door_1',
      'modern_industrial_desk', 
      'modern_metal_windowed_door', 
      'modern_wood_door', 
      'noguchi_coffee_table', 
      'office_chair',
      'office_desk_140x60', 
       'poliform_bed', 
      'pvc_still_window_with_sill',

      'queen-bed', 

      'quersus_gaming_chair_vaos.3.1_pearl_white', 
      'shelf', 
      'soviet_table',
      'table', 

      'table_1', 

      'table_furniture', 
      'wardrobe_classic', 
      'wardrobe_low_poly',
       'window_1', 
       'window_3', 
       'window_4',
       'window_5', 
       'wooden_cupboard_with_door'
  ];
  # Thay thế bằng danh sách của bạn

# Tạo thư mục chính
main_folder = "ref_image"
os.makedirs(main_folder, exist_ok=True)

# Tạo các thư mục con
for name in names:
    subfolder_path = os.path.join(main_folder, name)
    os.makedirs(subfolder_path, exist_ok=True)

print(f"Đã tạo thư mục '{main_folder}' và các thư mục con.")