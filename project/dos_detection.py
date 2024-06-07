from collections import defaultdict
import scipy.stats as stats
import numpy as np

from project.sequence_model import get_transition_probs
from project.clustering import features_to_states
from project.utils import process_trace
from project.preprocessing import padding

train_edge_frequencies = np.array([])


def get_edge_frequencies(transition_probs):
    edge_frequencies = defaultdict(list)
    total_num_edges = 0
    for ngram, transitions in transition_probs.items():
        for next_state, freq in transitions.items():
            edge = ngram + (next_state,)
            total_num_edges += freq
            edge_frequencies[edge] = freq

    for edge, freq in edge_frequencies.items():
        edge_frequencies[edge] = freq / total_num_edges

    return edge_frequencies


def init_edge_frequencies(trace_files_clean, clean_folder, n, syscall_type_mapping):
    global train_edge_frequencies
    train_edge_frequencies = np.array([])

    counter = 0

    for clean_file in trace_files_clean[:int(.75 * len(trace_files_clean))]:
        counter += 1

        padded_feature_vectors, str_args, _ = process_trace(clean_folder, clean_file, syscall_type_mapping)
        states_sequence = features_to_states(padded_feature_vectors)

        transition_probabilities = get_transition_probs(states_sequence, n, normalize=False)
        edge_frequencies = get_edge_frequencies(transition_probabilities)

        train_edge_frequencies = np.concatenate((train_edge_frequencies, np.array(list(edge_frequencies.values()))))

        if counter % int(.25 * .75 * len(trace_files_clean)) == 0:
            print(f'Edge traversal training: {counter // int(0.25 * .75 * len(trace_files_clean)) * 25}% complete')


def fit_beta_distribution(edge_frequencies):
    edge_frequencies = np.array(list(edge_frequencies))
    means = np.mean(edge_frequencies)
    variances = np.var(edge_frequencies)
    alphas = means * ((means * (1 - means)) / variances - 1)
    betas = (1 - means) * (alphas / means)
    return alphas, betas


# in this implementation- we've fixated 'n'-gram
def detect_dos(states, n, percentile=1.0 - (1e-9)):
    global train_edge_frequencies

    alpha, beta = fit_beta_distribution(train_edge_frequencies)
    threshold = stats.beta.ppf(percentile, alpha, beta)

    transition_probs = get_transition_probs(states, n, normalize=False)
    edge_frequencies = get_edge_frequencies(transition_probs)

    for freq in edge_frequencies.values():
        if freq > threshold:
            return True

    return False
