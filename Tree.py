import os

def print_tree(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        if level > 0:  # Skip recursion into subdirectories
            continue
        print(f"{os.path.basename(root)}/")
        for file in files:
            print(f"    └── {file}")
        for dir_name in dirs:
            print(f"    ├── {dir_name}/")

# Use a raw string for the path or double backslashes
print_tree(r"C:\Users\FangYuan\PycharmProjects\sos_dql_project")
