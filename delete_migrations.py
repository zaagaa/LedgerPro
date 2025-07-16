import os
import subprocess

# Step 1: Delete migration files
for root, dirs, files in os.walk("."):
    if "migrations" in dirs:
        mig_path = os.path.join(root, "migrations")
        for file in os.listdir(mig_path):
            if file != "__init__.py" and (file.endswith(".py") or file.endswith(".pyc")):
                file_path = os.path.join(mig_path, file)
                os.remove(file_path)
                print("Deleted:", file_path)

# Step 2: Run makemigrations
print("\n📦 Running makemigrations...")
subprocess.run(["python", "manage.py", "makemigrations"])
