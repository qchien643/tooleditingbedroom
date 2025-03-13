# setup.py
from setuptools import setup, find_packages

setup(
    name='snippet',            # Tên package (có thể đổi tùy ý)
    version='0.1.0',           # Phiên bản package
    packages=find_packages(),  # Tự động tìm kiếm các package con
    include_package_data=True, # Cho phép bao gồm thêm file dữ liệu nếu cần
)