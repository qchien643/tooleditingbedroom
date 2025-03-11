import random
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Định nghĩa thuộc tính (có thể mở rộng sau này)
attributes = ["hien_dai", "co_dien", "de_thuong"]

class table:
    def __init__(self):
        self.oder_ways = [
            "oder way 1 table",
            "oder way 2 table",
            "oder way 3 table"
        ]

class chair:
    def __init__(self):
        self.oder_ways = [
            "oder way 1 chair",
            "oder way 2 chair",
            "oder way 3 chair",
            "oder way 4 chair"
        ]

class light:
    def __init__(self):
        self.oder_ways = [
            "oder way 1 light",
            "oder way 2 light"
        ]

list_name_model= [
    '5x7_ojai_cali',
    '763010_unitario_lightstar_chandelier',
    'a074nn',
    'akia_hand_woven_wool_runner_66_x_200cm',
    'another_chair'
]

phan_loai = {
  "5x7_ojai_cali": table,
  "763010_unitario_lightstar_chandelier": light,
  "a074nn": table,
  "akia_hand_woven_wool_runner_66_x_200cm": table,
  "another_chair": chair
}

# Tạo dữ liệu giả
num_samples = 200
designs = []
for i in range(num_samples):
    mo_hinh_chon = {}
    cach_chon = {}
    for name in list_name_model:
        chosen = random.randint(0,1)
        mo_hinh_chon[name] = chosen
        if chosen == 1:
            model_type = phan_loai[name]()
            selected_way = random.choice(model_type.oder_ways)
            cach_chon[name] = selected_way

    num_selected = sum(mo_hinh_chon.values())
    scores = {
        "hien_dai": num_selected * random.randint(10,20) + random.randint(0,10),
        "co_dien": num_selected * random.randint(5,10) + random.randint(0,5),
        "de_thuong": num_selected * random.randint(8,15) + random.randint(0,8),
    }

    design = {
        "mo_hinh_duoc_chon": mo_hinh_chon,
        "cach_chon": cach_chon,
        "bang_diem": scores
    }
    designs.append(design)

def encode_design(design, list_name_model, phan_loai, attributes):
    vector_mo_hinh = [design["mo_hinh_duoc_chon"][name] for name in list_name_model]
    vector_cach_chon = []
    for name in list_name_model:
        model_type = phan_loai[name]()
        oder_ways = model_type.oder_ways
        if design["mo_hinh_duoc_chon"][name] == 1:
            selected_way = design["cach_chon"].get(name, None)
            vector_cach = [1 if way == selected_way else 0 for way in oder_ways]
        else:
            vector_cach = [0]*len(oder_ways)
        vector_cach_chon.extend(vector_cach)

    X = np.array(vector_mo_hinh + vector_cach_chon, dtype=np.float32)
    y = np.array([design["bang_diem"][attr] for attr in attributes], dtype=np.float32)
    return X, y

X_data = []
y_data = []
for d in designs:
    X, y = encode_design(d, list_name_model, phan_loai, attributes)
    X_data.append(X)
    y_data.append(y)

X_data = np.array(X_data)
y_data = np.array(y_data)

X_train, X_test, y_train, y_test = train_test_split(X_data, y_data,
                                                    test_size=0.2, random_state=42)

params = {
    'objective': 'reg:squarederror',
    'seed': 42,
    'n_estimators': 100,
    'max_depth': 5
}

models = {}
for i, attr in enumerate(attributes):
    model = xgb.XGBRegressor(**params)
    model.fit(X_train, y_train[:, i])
    models[attr] = model

for i, attr in enumerate(attributes):
    y_pred = models[attr].predict(X_test)
    mse = mean_squared_error(y_test[:, i], y_pred)
    print(f"MSE {attr}:", mse)

def individual_creator(list_name_model, phan_loai):
    individual = []
    for name in list_name_model:
        chosen = random.randint(0,1)
        if chosen == 1:
            model_type = phan_loai[name]()
            way_index = random.randint(0, len(model_type.oder_ways)-1)
        else:
            way_index = -1
        individual.append((chosen, way_index))
    return individual

def decode_individual(individual, list_name_model, phan_loai, attributes):
    mo_hinh_chon = {}
    cach_chon = {}
    for i, name in enumerate(list_name_model):
        chosen, way_index = individual[i]
        mo_hinh_chon[name] = chosen
        if chosen == 1:
            model_type = phan_loai[name]()
            selected_way = model_type.oder_ways[way_index]
            cach_chon[name] = selected_way

    # Placeholder điểm = 0
    scores = {attr:0 for attr in attributes}

    design = {
        "mo_hinh_duoc_chon": mo_hinh_chon,
        "cach_chon": cach_chon,
        "bang_diem": scores
    }
    return design

def predict_design(individual, list_name_model, phan_loai, attributes, models):
    design = decode_individual(individual, list_name_model, phan_loai, attributes)
    X, _ = encode_design(design, list_name_model, phan_loai, attributes)
    X = X.reshape(1, -1)
    preds = {}
    for attr in attributes:
        preds[attr] = models[attr].predict(X)[0]
    return preds

def fitness(individual, list_name_model, phan_loai, attributes, models, target_scores):
    preds = predict_design(individual, list_name_model, phan_loai, attributes, models)
    error = 0
    for attr in attributes:
        diff = target_scores[attr] - preds[attr]
        if diff > 0:
            error += diff
    return error, preds

def crossover(parent1, parent2):
    cut = random.randint(1, len(parent1)-1)
    child = parent1[:cut] + parent2[cut:]
    return child

def mutate(individual, phan_loai, list_name_model, mutation_rate=0.1):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            chosen, way_index = individual[i]
            if chosen == 1:
                if random.random() < 0.5:
                    chosen = 0
                    way_index = -1
                else:
                    name = list_name_model[i]
                    model_type = phan_loai[name]()
                    way_index = random.randint(0, len(model_type.oder_ways)-1)
            else:
                chosen = 1
                name = list_name_model[i]
                model_type = phan_loai[name]()
                way_index = random.randint(0, len(model_type.oder_ways)-1)
            individual[i] = (chosen, way_index)
    return individual

def genetic_search(target_scores,
                   list_name_model, phan_loai, attributes, models,
                   population_size=50, generations=500,
                   crossover_rate=0.7, mutation_rate=0.1):
    population = [individual_creator(list_name_model, phan_loai) for _ in range(population_size)]

    for gen in range(generations):
        fitness_results = []
        for ind in population:
            err, preds = fitness(ind, list_name_model, phan_loai, attributes, models, target_scores)
            fitness_results.append((err, ind, preds))

        fitness_results.sort(key=lambda x: x[0])
        best_error, best_ind, best_pred = fitness_results[0]

        if best_error == 0:
            # Khi tìm thấy giải pháp, ta in ra thiết kế và điểm dự đoán:
            print(f"Found a solution at generation {gen}:")
            print("Prediction:", best_pred)
            solution_design = decode_individual(best_ind, list_name_model, phan_loai, attributes)
            
            # Cập nhật bang_diem của solution_design bằng điểm dự đoán từ mô hình:
            for attr in attributes:
                solution_design["bang_diem"][attr] = best_pred[attr]

            return solution_design

        cutoff = population_size // 2
        selected = [ind for (err, ind, pred) in fitness_results[:cutoff]]

        new_population = []
        while len(new_population) < population_size:
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            if random.random() < crossover_rate:
                child = crossover(parent1, parent2)
            else:
                child = parent1[:]
            child = mutate(child, phan_loai, list_name_model, mutation_rate)
            new_population.append(child)
        
        population = new_population

    print("No solution found after all generations.")
    return None

# Ví dụ target
target_scores = {
    "hien_dai": 30,
    "co_dien": 20,
    "de_thuong": 25
}

solution = genetic_search(target_scores,
                          list_name_model, phan_loai, attributes, models,
                          population_size=50, generations=500,
                          crossover_rate=0.7, mutation_rate=0.1)

if solution is not None:
    print("Thiết kế tìm được với điểm số dự đoán:")
    print(solution)
else:
    print("Không tìm thấy thiết kế thỏa mãn yêu cầu.")

