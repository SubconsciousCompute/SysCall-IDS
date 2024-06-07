from minisom import MiniSom
import numpy as np
import gensim
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

threshold = 0
char_model = None
som = None
init_called = False
pca = None


def _encode_string(string):
    global char_model

    encoded = np.zeros(char_model.vector_size)
    for char in string:
        if char in char_model.wv:
            encoded += char_model.wv[char]
    if len(string) != 0:
        encoded /= len(string)
    return encoded


def init_som(training_str_args):
    global char_model, threshold, init_called, som, pca

    embed_dim = 16
    som_dim = (10, 10)

    print("=> Initializing Self-Organizing Map")

    char_corpus = [list(str_arg) for str_arg in training_str_args]
    char_model = gensim.models.Word2Vec(char_corpus, vector_size=embed_dim, min_count=1, workers=4, sg=1)

    encoded_str_args = [_encode_string(str_arg) for str_arg in training_str_args]
    encoded_str_args = list(filter(lambda x: x is not None, encoded_str_args))

    som_data = np.array(encoded_str_args)
    som_data_norm = np.linalg.norm(som_data, axis=1, keepdims=True)
    som_data_norm = np.array([norm_comp[0] if norm_comp[0] != 0 else 1 for norm_comp in som_data_norm]).reshape(
        som_data_norm.shape)
    som_data /= som_data_norm

    pca = PCA(n_components=som_data.shape[1]//3)
    som_data = pca.fit_transform(som_data)

    som = MiniSom(som_dim[0], som_dim[1], 5, sigma=1.0, learning_rate=0.5)
    som.random_weights_init(som_data)
    som.train_random(som_data, num_iteration=1000)

    print(f"=> Shape of Map Weights: {som.get_weights().shape}")

    print("=> Calculating threshold distance for anomaly detection")

    distances = [np.linalg.norm(data_point - som.get_weights()[som.winner(data_point)]) for data_point in som_data]
    threshold = np.max(distances)

    print(f"=> Threshold distance: {threshold}")

    init_called = True

    plt.figure(figsize=(5, 5))
    plt.pcolor(som.distance_map().T, cmap='Blues')
    plt.colorbar()

    plt.title('Pathname Self-Organizing Map (SOM)')
    plt.show()


def detect_string_anomaly_som(string_array):
    global char_model, threshold, som, pca

    if not init_called:
        raise Exception("Must call `init_som` before calling `detect_string_anomaly_som`")

    string_array = list(filter(lambda x: x != "", string_array))
    encoded_strings = [_encode_string(string) for string in string_array]
    encoded_strings_norm = np.linalg.norm(encoded_strings, axis=1, keepdims=True)
    encoded_strings_norm = np.array(
        [norm_comp[0] if norm_comp[0] != 0 else 1 for norm_comp in encoded_strings_norm]).reshape(
        encoded_strings_norm.shape)
    encoded_strings /= encoded_strings_norm
    encoded_strings = pca.transform(encoded_strings)

    min_neighborhood_values = []
    for encoded_string in encoded_strings:
        distances = np.linalg.norm(som.get_weights() - encoded_string, axis=2)
        bmu_idx = distances.argmin()

        bmu_coords = np.unravel_index(bmu_idx, som.get_weights().shape[:2])
        bmu_weight_vector = som.get_weights()[bmu_coords]
        neighborhood_value = np.linalg.norm(encoded_string - bmu_weight_vector)
        min_neighborhood_values.append(neighborhood_value)

    is_abnormal = max(min_neighborhood_values) > threshold
    return is_abnormal
