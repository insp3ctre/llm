import os
from google.genai import types #type: ignore

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Open and overwrite content to the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that you would like to add into the specified file"
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    elif os.path.isdir(target_dir):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    os.makedirs(os.path.dirname(target_dir), exist_ok=True)

    try:
        with open(target_dir, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except:
        return f'Error: could not write to "{file_path}"'