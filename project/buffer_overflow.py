import scipy.stats as stats
import numpy as np

mean_str_len = 0
std_str_len = 0

init_called = False


def init_strlen_distribution(training_str_args):
    global mean_str_len, std_str_len, init_called

    str_arg_lens = [len(str_arg) for str_arg in training_str_args]

    mean_str_len = np.mean(str_arg_lens)
    std_str_len = np.std(str_arg_lens, ddof=1)

    init_called = True

    print(f"Mean string length: {mean_str_len:.2f}; standard deviation {std_str_len:.2f}")


def detect_str_outlier(str_arg):
    global mean_str_len, std_str_len, init_called

    if not init_called:
        raise Exception("Must call `init_strlen_distribution` before calling `detect_str_outlier`")

    threshold = stats.norm.isf(0.001, loc=mean_str_len, scale=std_str_len)
    return len(str_arg) > threshold
