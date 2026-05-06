import os
import subprocess
from google.genai import types #type: ignore

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a specific python file. It reads from the working directory and takes optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="OPTIONAL arguments added when running the 'file_path' python file"
                )
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(target_dir):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    elif not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    
    try:
        command = ["python", file_path]
        if args:
            command.extend(args)

        completed = subprocess.run(command, cwd=working_dir_abs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)

        output = ""
        if completed.returncode != 0:
            output += f"Process exited with code {completed.returncode}\n"
        if completed.stdout and completed.stderr:
            output += f"No output produced\n"
        output += f"STDOUT: {completed.stdout}\nSTDERR: {completed.stderr}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"