import os

def print_tree(startpath):
    exclude_dirs = {'.git', '.idea', 'venv', '__pycache__'}
    exclude_files = {'Tree.py'}  # Add any files you want to exclude

    def tree(dir_path, prefix=''):
        # Get the contents of the directory
        try:
            contents = os.listdir(dir_path)
        except PermissionError:
            return  # Skip directories that cannot be accessed

        # Exclude hidden files/directories and specified ones
        contents = [c for c in contents if not c.startswith('.')
                    and c not in exclude_dirs.union(exclude_files)]

        # Sort contents: directories first, then files
        contents.sort(key=lambda x: (os.path.isfile(os.path.join(dir_path, x)), x.lower()))

        # Determine the connectors based on position
        pointers = ['├── '] * (len(contents) - 1) + ['└── '] if contents else []
        for pointer, content in zip(pointers, contents):
            path = os.path.join(dir_path, content)
            print(prefix + pointer + content)
            if os.path.isdir(path):
                extension = '│   ' if pointer == '├── ' else '    '
                tree(path, prefix=prefix + extension)

    base_name = os.path.basename(os.path.abspath(startpath))
    print(f"{base_name}/")
    tree(startpath)

# Use a raw string for the path or double backslashes
print_tree(r"C:\Users\FangYuan\PycharmProjects\sos_dql_project")
