import os
import re

# === CONFIGURATION ===
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # Current folder
EXCLUDE_DIRS = {'.venv', 'env', '__pycache__', 'migrations'}

# === REGEX ===
filter_update_pattern = re.compile(r"(\w+)\.objects\.filter\((.*?)\)\.update\((.*?)\)")
no_filter_update_pattern = re.compile(r"(\w+)\.objects\.update\((.*?)\)")

def is_commented(line):
    stripped = line.strip()
    return stripped.startswith("#") or "# " in stripped.split("update")[0]

def convert_update_to_save(line):
    line = line.strip("\n")
    match = filter_update_pattern.search(line)
    if match:
        model, filters, updates = match.groups()
    else:
        match = no_filter_update_pattern.search(line)
        if match:
            model, updates = match.groups()
            filters = None
        else:
            return line  # no match at all

    leading_spaces = re.match(r"^(\s*)", line).group(1)
    update_pairs = [u.strip() for u in updates.split(",") if "=" in u]

    converted = f"{leading_spaces}try:\n"
    if filters:
        converted += f"{leading_spaces}    obj = {model}.objects.get({filters})\n"
    else:
        converted += f"{leading_spaces}    obj = {model}.objects.first()\n"  # safe default; could change to .get(pk=...) if needed

    for pair in update_pairs:
        if "=" not in pair:
            continue
        field, val = pair.split("=", 1)
        val = val.strip()
        if val.count("(") > val.count(")"):
            print(f"⚠️ Skipping unbalanced value: {pair}")
            continue
        converted += f"{leading_spaces}    obj.{field.strip()} = {val}\n"

    converted += f"{leading_spaces}    obj.save()\n"
    converted += f"{leading_spaces}except {model}.DoesNotExist:\n"
    converted += f"{leading_spaces}    pass"
    return converted

def process_python_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as read_err:
        print(f"❌ Could not read {file_path}: {read_err}")
        return

    new_lines = []
    modified = False
    multiline_flag = False
    update_block = []

    for line in lines:
        if multiline_flag:
            update_block.append(line)
            if ")" in line:
                full_line = "".join(update_block)
                if not is_commented(full_line) and (
                    filter_update_pattern.search(full_line) or no_filter_update_pattern.search(full_line)
                ):
                    try:
                        converted = convert_update_to_save(full_line)
                        new_lines.append(converted + "\n")
                        modified = True
                    except Exception as e:
                        print(f"❌ Error at {file_path}: {e}")
                        new_lines.extend(update_block)
                else:
                    new_lines.extend(update_block)
                multiline_flag = False
                update_block = []
            continue

        if (filter_update_pattern.search(line) or no_filter_update_pattern.search(line)) and not is_commented(line):
            if ")" not in line:
                multiline_flag = True
                update_block = [line]
                continue
            try:
                converted = convert_update_to_save(line)
                new_lines.append(converted + "\n")
                modified = True
            except Exception as e:
                print(f"❌ Error at {file_path}: {e}")
                new_lines.append(line)
        else:
            new_lines.append(line)

    if modified:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print(f"✅ Converted: {file_path}")
        except Exception as write_err:
            print(f"❌ Could not write to {file_path}: {write_err}")

# === FILE WALK ===
for root, dirs, files in os.walk(PROJECT_ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    if root == PROJECT_ROOT:
        continue

    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            process_python_file(file_path)
