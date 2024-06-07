import numpy as np


def syscall_info_to_feature_vector(syscall_info, syscall_type_mapping):
    syscall_type_idx = syscall_type_mapping[syscall_info[0]]
    syscall_args = syscall_info[1:]
    numeric_args = []
    string_args = []

    for arg in syscall_args:
        if arg.isdigit():
            numeric_args.append(float(arg))
        elif arg and (arg[0] == '"' and arg[-1] == '"'):
            string_args.append(arg[1:-1])
        elif arg and '\\' in arg:
            string_args.append(arg)

    feature_vector = [syscall_type_idx] + numeric_args
    return feature_vector, string_args


def padding(feature_vectors, max_len):
    padded_feature_vectors = [np.pad(vec, (0, max_len - len(vec)), 'constant', constant_values=-1)
                              for vec in feature_vectors]
    return padded_feature_vectors
