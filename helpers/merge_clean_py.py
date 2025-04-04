import os
import re
from collections import OrderedDict

print("Ufa")

# Set directory and output file
directory = "../../../Documents/Workspace/blender_plus_python-main/All"
output_file = "merged_and_cleaned.py"

print("Here:")

# Regex patterns for matching imports, functions, and the main block
import_pattern = re.compile(r"^\s*import .+|^\s*from .+ import .+")
function_pattern = re.compile(r"^\s*def (\w+)\s*\(")
main_pattern = re.compile(r"if\s+__name__\s*==\s*['\"]__main__['\"]:")

print("directory:")

# Sets and OrderedDict to store imports and functions
imports = set()
functions = OrderedDict()
function_list = []

# Debugging: Track steps and decisions
print("Starting merging process for files in directory:", directory)

# Step 1: Iterate through each Python file
for filename in os.listdir(directory):
    if filename.endswith(".py"):
        print(f"Processing file: {filename}")
        
        with open(os.path.join(directory, filename), "r") as file:
            inside_main_block = False
            function_name = None
            current_function_lines = []

            for line in file:
                # Collect import lines
                if import_pattern.match(line):
                    imports.add(line.strip())
                    print(f"Collected import: {line.strip()}")

                # Detect function definitions
                elif match := function_pattern.match(line):
                    function_name = match.group(1)
                    function_list.append(function_name)  # Add to function list
                    print(f"Detected function: {function_name}")

                    # Add the previous function, if any, to functions dict
                    if current_function_lines:
                        func_def = "\n".join(current_function_lines)
                        functions[function_name] = func_def
                        print(f"Added function to list: {function_name}")
                        current_function_lines = []

                    # Start collecting new function definition
                    current_function_lines.append(line)

                # Continue collecting lines within a function
                elif function_name:
                    current_function_lines.append(line)

                # Detect and skip main blocks
                elif main_pattern.match(line):
                    inside_main_block = True
                    print("Skipping main block")
                elif inside_main_block:
                    if line.strip() == "":  # End of main block
                        inside_main_block = False
                        print("Exited main block")

            # Finalize the last function, if any
            if current_function_lines:
                func_def = "\n".join(current_function_lines)
                functions[function_name] = func_def
                print(f"Added final function to list: {function_name}")

print("Finished processing files. Writing merged output.")

# Step 2: Write imports, function list, and functions to the output file
with open(output_file, "w") as output:
    # Write all import statements
    output.write("# Merged and cleaned Python file\n\n")
    for imp in sorted(imports):
        output.write(imp + "\n")
    output.write("\n")

    # Write function list as comments
    output.write("# Function list:\n")
    for function_name in function_list:
        output.write(f"# - {function_name}\n")
    output.write("\n")

    # Write unique functions
    for func_def in functions.values():
        output.write(func_def + "\n")

print(f"Merged and cleaned Python files saved as {output_file}")

