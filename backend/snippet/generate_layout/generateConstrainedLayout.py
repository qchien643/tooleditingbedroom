from deap import base, creator, tools, algorithms
from evaluate_layout import return_decision_tree
from weight import DESIRED_SCORE,NUM_MODELS
import numpy as np

user_selected_models = [3]
decision_tree = return_decision_tree()


# Hàm đánh giá bố cục dựa trên mô hình decision tree
def evaluate(individual):
    layout = np.array([individual])
    predicted_score = decision_tree.predict(layout)[0]
    return (predicted_score,)

def generate_constrained_based_layout(num_models, user_selected_models):
    layout = np.random.randint(0, 2, size=(num_models)).flatten()
    for model in user_selected_models:
        layout[model] = 1  # Đảm bảo các mô hình bắt buộc luôn có mặt
    return layout.tolist()

# Tùy chỉnh để thêm các mô hình bắt buộc
def mutate_with_constraints(individual, user_selected_models):
    for model in user_selected_models:
        individual[model] = 1  # Đảm bảo các mô hình bắt buộc luôn có mặt
    return individual,

def generateConstrainedLayout(user_selected_models):
    # Thiết lập môi trường di truyền với các ràng buộc
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # Đăng ký hàm khởi tạo cá thể dựa trên generate_constrained_based_layout
    toolbox = base.Toolbox()
    toolbox.register("individual", lambda: creator.Individual(generate_constrained_based_layout(NUM_MODELS, user_selected_models)))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)


    # Đăng ký các thao tác khác trong toolbox
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate_with_constraints, user_selected_models=user_selected_models)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evaluate)

    # Tạo quần thể ban đầu
    population = toolbox.population(n=50)

    # Áp dụng thuật toán di truyền để tối ưu hóa bố cục
    num_generations = 20
    result, logbook = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=num_generations, verbose=False)

    # Lấy ra cá thể tốt nhất (bố cục tối ưu)
    best_individual = tools.selBest(population, 1)[0]
    best_layout = np.array([best_individual])
    best_score = decision_tree.predict(best_layout)[0]

    return best_layout, best_score

def generateBestLayout():
    # Tạo hàm fitness, mục tiêu là tìm bố cục có điểm hiện đại cao hơn DESIRED_SCORE
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    # Thiết lập các tham số cho thuật toán di truyền

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", np.random.randint, 0, 2)  # 0 hoặc 1 cho mỗi gene (mô hình)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=NUM_MODELS)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evaluate)

    # Tạo quần thể ban đầu
    population = toolbox.population(n=50)

    # Áp dụng thuật toán di truyền
    num_generations = 20
    result, logbook = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=num_generations, verbose=False)

    # Lấy ra cá thể tốt nhất
    best_individual = tools.selBest(population, 1)[0]
    best_layout = np.array([best_individual])
    best_score = decision_tree.predict(best_layout)[0]
    return best_layout , best_score




