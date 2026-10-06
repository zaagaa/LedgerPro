import os

project_root = os.path.dirname(os.path.abspath(__file__))
deleted = []

for root, dirs, files in os.walk(project_root):
    # Skip virtual environment folders
    if '.venv' in root or 'env' in root or 'Lib' in root:
        continue

    if 'migrations' in dirs:
        migration_dir = os.path.join(root, 'migrations')
        for file in os.listdir(migration_dir):
            file_path = os.path.join(migration_dir, file)
            if file != '__init__.py' and file.endswith('.py'):
                os.remove(file_path)
                deleted.append(file_path)
            elif file.endswith('.pyc'):
                os.remove(file_path)

print(f"✅ Deleted {len(deleted)} migration files.")
