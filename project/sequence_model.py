from collections import defaultdict

def generate_ngrams(sequence, n):
    return [tuple(sequence[i:i+n]) for i in range(len(sequence) - n + 1)]


def get_transition_probs(states, n=1, normalize=True):
    ngrams = generate_ngrams(states, n)
    transition_probabilities = defaultdict(lambda: defaultdict(float))

    # record transitions
    for i in range(len(ngrams) - 1):
        current_ngram = ngrams[i]
        next_state = ngrams[i + 1][0]
        transition_probabilities[current_ngram][next_state] += 1

    # normalize to obtain transition probabilities
    if normalize:
        for state, transitions in transition_probabilities.items():
            total_transitions = sum(transitions.values())
            for next_state in transitions:
                transition_probabilities[state][next_state] /= total_transitions

    return transition_probabilities
