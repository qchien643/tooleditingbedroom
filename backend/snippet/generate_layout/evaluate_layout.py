# Import các thư viện cần thiết
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error


from weight import TRAINNING_LAYOUT_TEST , TRAINNING_MARK_TEST

def return_mse_decision_tree():
    # Giả sử bạn có dữ liệu mô phỏng, ví dụ như sau:
    X = np.array(TRAINNING_LAYOUT_TEST)
    y = np.array(TRAINNING_MARK_TEST)

    # Chia dữ liệu thành tập huấn luyện và tập kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Khởi tạo Decision Tree Regressor
    decision_tree = DecisionTreeRegressor(random_state=42)

    # Huấn luyện mô hình với tập huấn luyện
    decision_tree.fit(X_train, y_train)

    # Dự đoán trên tập kiểm tra
    y_pred = decision_tree.predict(X_test)

    # Tính toán sai số
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    return mse , mae

def return_decision_tree():
    
    # Giả sử bạn có dữ liệu mô phỏng, ví dụ như sau:
    X = np.array(TRAINNING_LAYOUT_TEST)
    y = np.array(TRAINNING_MARK_TEST)

    # Chia dữ liệu thành tập huấn luyện và tập kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Khởi tạo Decision Tree Regressor
    decision_tree = DecisionTreeRegressor(random_state=42)

    # Huấn luyện mô hình với tập huấn luyện
    decision_tree.fit(X_train, y_train)

    return decision_tree


