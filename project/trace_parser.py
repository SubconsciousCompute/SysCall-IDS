import os
import re


def list_files_in_folder(folder_path):
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return files
    except Exception as e:
        return str(e)


def get_trace_text(folder, trace_files):
    trace_text = ""
    for trace_file in trace_files:
        with open(folder+trace_file, 'r') as f:
            trace_text += f.read()
    return trace_text


def extract_syscall_info(line): # encapsulated in parse_trace_text
    syscall_pattern = re.compile(r'\d+\.\d+\s+(\w+)\((.*)\)\s*=')
    match = syscall_pattern.search(line)
    if match:
        syscall_name, args_str = match.groups()
        args = args_str.split(', ')
        return [syscall_name] + args
    return []


def parse_trace_text(trace_text): # encapsulates extract_syscall_info
    syscall_info_arr = []
    for line in trace_text.split('\n'):
        info = extract_syscall_info(line)
        if info:
            syscall_info_arr.append(info)
    return syscall_info_arr