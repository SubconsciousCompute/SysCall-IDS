import numpy as np
# from sklearn.preprocessing import LabelEncoder
from scipy.signal import savgol_filter, find_peaks

def autocorrelation(states_numeric):
    n = len(states_numeric)
    mean = np.mean(states_numeric)
    autocorr = np.correlate(states_numeric - mean, states_numeric - mean, mode='full')[-n:]
    return autocorr / (np.var(states_numeric) * np.arange(n, 0, -1))


def soe(states_numeric):
    states_numeric = states_numeric
    autocorr = autocorrelation(states_numeric)
    smoothed_autocorr = savgol_filter(autocorr, window_length=50, polyorder=2)
    peaks = np.where(smoothed_autocorr > np.percentile(smoothed_autocorr, 90))[0]

    min_peak_distance = 10
    filtered_peaks = []
    prev_peak = peaks[0]
    for peak in peaks:
        if peak - prev_peak >= min_peak_distance:
            filtered_peaks.append(peak)
            prev_peak = peak

    segments = list(filter(lambda x: len(x) != 1, [states_numeric[i:j] for i, j in zip(filtered_peaks[:-1], filtered_peaks[1:])]))

    return segments


def process_segments(segments):
    segment_groups = {}
    length_range = 10
    for segment in segments:
        segment_length = len(segment)
        group_key = (segment_length // length_range) * length_range
        if group_key not in segment_groups:
            segment_groups[group_key] = []
        segment_groups[group_key].append(segment)

    max_group_key = max(segment_groups, key=lambda k: len(segment_groups[k]))
    segments_rep = segment_groups[max_group_key]
    return segments_rep


# def longest_common_subsequence(segments):
#     if not segments:
#         return []
#
#     def lcs_two(arr1, arr2):
#         m, n = len(arr1), len(arr2)
#         dp = [[0] * (n + 1) for _ in range(m + 1)]
#
#         for i in range(1, m + 1):
#             for j in range(1, n + 1):
#                 if arr1[i - 1] == arr2[j - 1]:
#                     dp[i][j] = dp[i - 1][j - 1] + 1
#                 else:
#                     dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
#
#         lcs = []
#         i, j = m, n
#         while i > 0 and j > 0:
#             if arr1[i - 1] == arr2[j - 1]:
#                 lcs.append(arr1[i - 1])
#                 i -= 1
#                 j -= 1
#             elif dp[i - 1][j] > dp[i][j - 1]:
#                 i -= 1
#             else:
#                 j -= 1
#
#         return list(reversed(lcs))
#
#     def lcs_multiple(segments):
#         result = segments[0]
#         for i in range(1, len(segments)):
#             result = lcs_two(result, segments[i])
#         return result
#
#     return lcs_multiple(segments)


def segment_sequence(sequence, start_of_execs):
    segments = []
    start_index = 0

    for i, item in enumerate(sequence):
        for start_of_exec in start_of_execs:
            start_of_exec_len = len(start_of_exec)
            if np.array_equal(sequence[i:i + start_of_exec_len], start_of_exec):
                if (i - start_index > 6):
                    segments.append(sequence[start_index:i])
                    start_index = i

    segments.append(sequence[start_index:])

    return segments

def merge_segments(segments):
    merged_segments = []
    current_segment = segments[0]
    for i in range(1, len(segments)):
        if len(current_segment) < 50:
            current_segment = np.concatenate([current_segment, segments[i]])
        else:
            merged_segments.append(current_segment)
            current_segment = segments[i]

    if len(current_segment) < 50 and len(merged_segments) > 0:
        merged_segments[-1] = np.concatenate([merged_segments[-1], current_segment])
    else:
        merged_segments.append(current_segment)

    return merged_segments