import numpy as np
from project.clustering import features_to_states
from project.sequence_model import generate_ngrams
from project.dos_detection import detect_dos
from project.string_anomaly_som import detect_string_anomaly_som
from project.buffer_overflow import detect_str_outlier
import joblib

pca = None
scaler = None


def initialize_pca():
    global pca, scaler
    pca = joblib.load('../models/pca_model.pkl')
    scaler = joblib.load('../models/scaler.pkl')


def get_cluster_probability(feature_vector, syscall_to_cluster):
    global pca, scaler

    syscall_idx = feature_vector[0]
    clustering = syscall_to_cluster.get(syscall_idx, None)
    eps = 1e-8


    if not clustering:
        return 0.0
    else:
        vec = scaler.transform([np.array(feature_vector[1:])])
        vec = pca.transform(vec)[0]

        # -- Kmeans --
        # distances = clustering.transform([vec])
        # min_distance = np.min(distances)
        # max_distance = np.max(distances)
        # P_c = 1 - (min_distance / (max_distance + eps))

        # -- Gaussian Mixture --
        P_c = max(clustering.predict_proba([vec])[0])

        return P_c


def sequence_probability(feature_vectors, str_args, n, syscall_to_cluster, transition_probabilities, with_dos=True):
    states_sequence = features_to_states(feature_vectors)

    log_Ps = 0
    log_Pp = 0
    eps = 1e-8

    ngrams_sequence = generate_ngrams(states_sequence, n)

    if with_dos and detect_dos(states_sequence, n):
        return 0, 0

    for i in range(len(ngrams_sequence) - 1):
        current_ngram = tuple(ngrams_sequence[i])
        next_state = tuple(ngrams_sequence[i + 1][0])
        P_c = get_cluster_probability(feature_vectors[i + n], syscall_to_cluster)
        P_m = transition_probabilities[current_ngram][next_state] + eps
        P_p = P_c * P_m

        strargs_i = str_args[n + i]
        strargs_i = list(filter(lambda str: str != "", strargs_i))
        if len(strargs_i) > 0 and (detect_str_outlier(strargs_i) or detect_string_anomaly_som(strargs_i)):
            log_Ps += np.log(eps)
        else:
            log_Ps += np.log(transition_probabilities[current_ngram][next_state] + eps)

        log_Pp += np.log(P_p + eps)

    Ps = np.exp(log_Ps / (2 * len(ngrams_sequence)))
    Pp = np.exp(log_Pp / (2 * len(ngrams_sequence)))

    return Ps, Pp