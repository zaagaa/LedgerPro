import subprocess
import os
import shutil
import stat
from setuptools import setup
from Cython.Build import cythonize

# ==== PERMISSION FIX FUNCTION ====
def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# ==== CONFIG ====
SOURCE_DIR = os.getcwd()
OUTPUT_DIR = os.path.join(SOURCE_DIR, "LedgerPro")
VERSION_FILE = os.path.join(SOURCE_DIR, "version.txt")

INCLUDE_FILES = ["views.py", "urls.py", "forms.py", "models.py", "middleware.py"]
EXCLUDE_COPY_DIRS = ["__pycache__", "LedgerPro", ".git", ".idea", ".venv"]
EXCLUDE_COPY_FILES = ["db_config.json", "db.sqlite3"]
EXCLUDE_DELETE = [".venv", ".idea"]

# ==== Step 0: Bump version ====
def bump_version():
    with open(VERSION_FILE, "r+") as f:
        version = f.read().strip()
        major, minor, patch = map(int, version.split('.'))
        patch += 1
        if patch >= 10:
            patch = 0
            minor += 1
            if minor >= 10:
                minor = 0
                major += 1
        new_version = f"{major}.{minor}.{patch}"
        f.seek(0)
        f.write(new_version)
        f.truncate()
    print(f"🔖 Version bumped from {version} → {new_version}")
    return new_version

print("🚀 Bumping version before copy...")
new_ver = bump_version()

# ==== Step 1: Clean OUTPUT_DIR ====
if os.path.exists(OUTPUT_DIR):
    print(f"🧨 Cleaning contents of {OUTPUT_DIR}...")
    for item in os.listdir(OUTPUT_DIR):
        if item in EXCLUDE_DELETE:
            print(f"⏩ Skipping protected: {item}")
            continue
        item_path = os.path.join(OUTPUT_DIR, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
                print(f"🗑️ Removed file: {item}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path, onerror=remove_readonly)
                print(f"🗑️ Removed folder: {item}")
        except Exception as e:
            print(f"❌ Failed to remove {item_path}: {e}")
else:
    print(f"📁 Creating {OUTPUT_DIR}...")
    os.makedirs(OUTPUT_DIR)

# ==== Step 2: Copy project ====
print(f"📁 Copying project to {OUTPUT_DIR} (with exclusions)...")

def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def custom_ignore(dirpath, names):
    return [name for name in names if name in EXCLUDE_COPY_DIRS or name in EXCLUDE_COPY_FILES]

shutil.copytree(
    SOURCE_DIR,
    OUTPUT_DIR,
    dirs_exist_ok=True,
    ignore=custom_ignore
)

# ==== Step 3: Collect files to compile ====
print("🔍 Collecting files to compile...")
py_files = []
for root, _, files in os.walk(OUTPUT_DIR):
    if any(skip in root for skip in ['site-packages', 'Lib', 'django', '.venv']):
        continue
    for file in files:
        if file in INCLUDE_FILES and file.endswith(".py"):
            full_path = os.path.join(root, file)
            py_files.append(full_path)
            print("✅ Will compile:", full_path)

print(f"📦 Total files to compile: {len(py_files)}")

# ==== Step 4: Compile using Cython ====
os.chdir(OUTPUT_DIR)
extensions = cythonize(
    py_files,
    compiler_directives={"language_level": "3"},
    build_dir="build"
)

setup(
    script_args=["build_ext", "--inplace"],
    ext_modules=extensions
)

# ==== Step 5: Delete .py files ====
print("🧹 Deleting compiled .py source files...")
for path in py_files:
    if os.path.exists(path):
        os.remove(path)
        print(f"🗑️ Deleted {path}")

# ==== Step 6: Run collectstatic ====
print("📦 Running collectstatic...")
subprocess.run([
    os.path.join(SOURCE_DIR, ".venv", "Scripts", "python.exe"),
    "manage.py",
    "collectstatic",
    "--noinput"
])

# ==== Step 7: Git Commit + Push ====
print("🚀 Committing version and pushing to Git...")
subprocess.run(["git", "add", VERSION_FILE])
subprocess.run(["git", "commit", "-m", f"🔖 Version updated to {new_ver}"])
subprocess.run(["git", "push"])

# ==== Step 7.1: Git Tag ====
print(f"🏷️ Creating Git tag v{new_ver}...")
subprocess.run(["git", "tag", f"v{new_ver}"])
subprocess.run(["git", "push", "origin", f"v{new_ver}"])

# ==== Step 8: Run Push Script ====
print("🚀 Running push_ledgerpro.bat...")
subprocess.call(["push_ledgerpro.bat"], shell=True)

# ==== DONE ====
print("\n✅ DONE: Protected Django copy is in 'LedgerPro/'")
print("✅ DONE: Version bumped, committed and pushed.")
