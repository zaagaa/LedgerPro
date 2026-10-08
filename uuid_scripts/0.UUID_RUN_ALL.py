import subprocess
import sys
import os

scripts = [
    "1.UUID_create_uuid_with_fill_step_1_OPTIMIZE.py",
    "2.UUID_update_uuid_into_child_step_2_OPTIMIZE.py",
    "3.UUID_replace_id_into_uuid_setp_3.py",
    "4.UUID_step_4.py",
    "5.UUID_remove_old_id_column_set_5.py",
    "6.UUID_set_indexes_to_uuid_column_step_6.py"
]

for script in scripts:
    script_path = os.path.abspath(script)
    print(f"\n🔄 Running: {script_path}")

    result = subprocess.run([sys.executable, script_path])

    if result.returncode != 0:
        print(f"❌ Script failed: {script} (exit code {result.returncode})")
        break
    else:
        print(f"✅ Completed: {script}")
