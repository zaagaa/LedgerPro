import os
import re

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_ROOT = os.path.join(PROJECT_DIR)  # Adjust this if needed

IMPORTS = [
    "import uuid",
    "from django.utils import timezone"
]

FIELDS = [
    "id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)",
    "sync = models.DateTimeField(default=timezone.now, null=True, blank=True)",
    "created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)",
    "updated_at = models.DateTimeField(null=True, blank=True)",
    "is_deleted = models.BooleanField(default=False)"
]

def inject_fields(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # ✅ Add required imports if missing
    imports_to_add = []
    for imp in IMPORTS:
        if not any(imp in line for line in lines):
            imports_to_add.append(imp)

    if imports_to_add:
        # Find position to insert after all import lines
        insert_at = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("import") or line.strip().startswith("from"):
                insert_at = i + 1
        for imp in reversed(imports_to_add):
            lines.insert(insert_at, imp + "\n")

    updated_lines = lines[:]
    modified = False

    # Process each model class
    for idx, line in enumerate(updated_lines):
        match = re.match(r'^(\s*)class\s+(\w+)\(.*models\.Model.*\):', line)
        if match:
            class_indent = match.group(1)
            class_start = idx
            body_indent = class_indent + "    "

            # Look ahead to find the body and check what fields are missing
            block_end = class_start + 1
            seen_fields = set()
            while block_end < len(updated_lines):
                line_inside = updated_lines[block_end]
                if line_inside.strip() == '':
                    block_end += 1
                    continue
                if not line_inside.startswith(body_indent):
                    break  # end of class
                for field in FIELDS:
                    if field.split("=")[0].strip() in line_inside:
                        seen_fields.add(field)
                block_end += 1

            # Insert missing fields
            missing = [field for field in FIELDS if field not in seen_fields]
            for i, field in enumerate(FIELDS):
                if field not in seen_fields:
                    updated_lines.insert(class_start + 1 + i, body_indent + field + '\n')
                    modified = True

    if modified or imports_to_add:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        print(f"✅ Injected sync fields into: {filepath}")
    else:
        print(f"⚠️ Skipped (already has all fields): {filepath}")

def walk_and_process():
    for root, dirs, files in os.walk(MODELS_ROOT):
        for file in files:
            if file == 'models.py':
                inject_fields(os.path.join(root, file))

if __name__ == '__main__':
    print("🔍 Processing model files for sync fields...")
    walk_and_process()
    print("✅ Injection complete.")
