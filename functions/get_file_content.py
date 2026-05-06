import os

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_dir, "r") as f:
            contents = f.read(10000)
            if f.read(1):
                contents += f'[...File "{file_path}" truncated at 10000 characters]'
            return contents
    except:
        return f'Error: could not open "{file_path}"'
