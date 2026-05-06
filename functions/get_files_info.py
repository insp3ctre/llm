import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(target_dir):
        return f'Error: "{valid_target_dir}" is not a directory'
    s = ""
    for item in os.listdir(target_dir):
        # save name, file size, is_dir
        path = os.path.join(target_dir, item)
        try:
            name = item
        except:
            return f'Error: "{path}" file not found'
        try:
            size = os.path.getsize(path)
        except:
            return f'Error: "{path} size not found'
        try:
            is_dir = os.path.isdir(path)
        except:
            return f'Error: "{path} is_dir not found'
        res = f"\t- {name}: file_size={size}, is_dir={is_dir}"
        s += res + "\n"
    return s
        

