from project.trace_parser import get_trace_text, parse_trace_text
from project.preprocessing import syscall_info_to_feature_vector, padding

max_len = 0


def process_trace(trace_folder, process_trace_file, syscall_type_mapping):
    global max_len

    trace_text = get_trace_text(trace_folder, [process_trace_file])
    syscall_info_arr = parse_trace_text(trace_text)

    features = [syscall_info_to_feature_vector(si, syscall_type_mapping) for si in syscall_info_arr]
    feature_vectors = [feature[0] for feature in features]
    str_args = [feature[1] for feature in features]

    max_len_curr = max([len(fv) for fv in feature_vectors])
    if max_len_curr > max_len:
        max_len = max_len_curr

    padded_feature_vectors = padding(feature_vectors, max_len)
    return padded_feature_vectors, str_args, max_len
