import subprocess
import sys
from pathlib import Path

# Automatically find the path to manage.py
manage_py = Path(__file__).parent / "manage.py"

# Step 1: Dumpdata using current Python executable (from venv)
try:
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(manage_py), "dumpdata", "--indent=2"],
        capture_output=True,
        text=True,
        check=True
    )
except subprocess.CalledProcessError as e:
    print("❌ Error running manage.py dumpdata:")
    print(e.stderr)
    sys.exit(1)

# Step 2: Write to file with fixed encoding
with open("fixed_data.json", "w", encoding="utf-8") as f:
    f.write(result.stdout)

print("✅ Fixed file saved as fixed_data.json (UTF-8 without BOM)")
