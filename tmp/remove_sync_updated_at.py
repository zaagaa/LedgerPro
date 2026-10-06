import os
import re
from django.conf import settings

def current_unix_ms():
    import time
    return int(time.time() * 1000)

def initial_sync_offline():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'offline' else None

def initial_sync_online():
    return current_unix_ms() if settings.INSTANCE_TYPE == 'online' else None


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
EXCLUDE_DIRS = {'.venv', 'migrations', '__pycache__', 'static', 'media'}

FUNC_DEF = [
    "def current_unix_ms():\n",
    "    import time\n",
    "    return int(time.time() * 1000)\n\n"
]
FUNC_DEF_PATTERN = re.compile(r'^\s*def\s+current_unix_ms\s*\(\s*\):')
FIELD_LINE = "    sync_offline = models.BigIntegerField(null=True, blank=True, default=initial_sync_offline)
    sync_online = models.BigIntegerField(null=True, blank=True, default=initial_sync_online)\n"

# Fields to remove if found
FIELDS_TO_REMOVE = [
    re.compile(r'^\s*sync\s*=\s*models\.DateTimeField\(.*timezone\.now.*\)\s*'),
    re.compile(r'^\s*updated_at\s*=\s*models\.DateTimeField\(.*\)\s*'),
    re.compile(r'^\s*is_deleted\s*=\s*models\.BooleanField\(.*\)\s*'),
]

def should_skip(path):
    return any(skip in path for skip in EXCLUDE_DIRS)

def has_import_models(lines):
    return any("from django.db import models" in line for line in lines)

def get_insert_index_after_imports(lines):
    for i, line in enumerate(lines):
        if line.strip() == "" or line.strip().startswith("class "):
            return i
    return 0

def has_current_unix_func(lines):
    return any(FUNC_DEF_PATTERN.match(line) for line in lines)

def remove_existing_current_unix_func(lines):
    cleaned = []
    skipping = False
    for line in lines:
        if FUNC_DEF_PATTERN.match(line):
            skipping = True
            continue
        if skipping:
            if line.strip() == "" or line.lstrip().startswith("def "):
                skipping = False
        if not skipping:
            cleaned.append(line)
    return cleaned

def patch_models_py(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        original_lines = f.readlines()

    lines = original_lines[:]
    lines = remove_existing_current_unix_func(lines)

    modified = False
    new_lines = []
    inside_model = False
    model_indent = 4
    has_sync_unix = False

    # Add import line if needed
    if not has_import_models(lines):
        lines.insert(0, "from django.db import models\n")
        modified = True

    # Add current_unix_ms() if not present
    if not has_current_unix_func(lines):
        insert_idx = get_insert_index_after_imports(lines)
        for line in reversed(FUNC_DEF):
            lines.insert(insert_idx, line)
        modified = True

    for i, line in enumerate(lines):
        # Remove undesired fields
        if any(pattern.match(line) for pattern in FIELDS_TO_REMOVE):
            modified = True
            continue  # skip this line

        # Detect model start
        if re.match(r'^\s*class\s+\w+\(.*models\.Model.*\):', line):
            inside_model = True
            has_sync_unix = False
            model_indent = len(line) - len(line.lstrip())
            new_lines.append(line)
            continue

        if inside_model:
            if 'sync_unix' in line:
                has_sync_unix = True

            if line.strip() == '' or line.lstrip().startswith(('def ', 'class ', '@')):
                if not has_sync_unix:
                    new_lines.append(' ' * (model_indent + 4) + FIELD_LINE.strip() + '\n')
                    modified = True
                inside_model = False

        new_lines.append(line)

    if inside_model and not has_sync_unix:
        new_lines.append(FIELD_LINE)
        modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f" Patched: {file_path}")

def run():
    print("🔍 Scanning Python files to patch models...")
    for root, dirs, files in os.walk(PROJECT_DIR):
        dirs[:] = [d for d in dirs if not should_skip(os.path.join(root, d))]
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'models.Model' in content:
                        patch_models_py(file_path)

if __name__ == "__main__":
    run()
