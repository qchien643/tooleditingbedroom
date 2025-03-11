import os
import numpy as np
from pygltflib import GLTF2

def scale_gltf(input_path, scale_factor, output_path=None):
    # Tải tệp GLTF
    gltf = GLTF2().load(input_path)

    # Scale các đỉnh của mô hình
    for mesh in gltf.meshes:
        for primitive in mesh.primitives:
            # Kiểm tra xem thuộc tính 'POSITION' có tồn tại không
            if hasattr(primitive.attributes, 'POSITION'):
                accessor = gltf.accessors[primitive.attributes.POSITION]
                buffer_view = gltf.bufferViews[accessor.bufferView]
                buffer = gltf.buffers[buffer_view.buffer]

                # Đọc dữ liệu đỉnh
                data = np.frombuffer(buffer.uri, dtype=np.float32, count=accessor.count * 3)
                data = data.reshape((-1, 3))

                # Scale dữ liệu
                data *= scale_factor

                # Ghi dữ liệu đã scale lại vào buffer
                buffer.uri = data.tobytes()

    # Lưu tệp GLTF đã scale
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + '_scaled.gltf'
    gltf.save(output_path)

    print(f'Model scaled and saved to {output_path}')

# Ví dụ sử dụng
scale_gltf('../model3D_extract/door_with_cardreader/scene.gltf', 1.0)