import glob
import pandas as pd
import os

print("🔍 Debugging File Detection...")
files = glob.glob("high_accuracy_trades_*.csv")
files.sort()

print(f"📂 Found {len(files)} files:")
for f in files:
    print(f" - {f} ({os.path.getsize(f)} bytes)")

if not files:
    print("❌ No files found!")
    exit()

last_file = files[-1]
print(f"\n📄 Inspecting last file: {last_file}")

try:
    df = pd.read_csv(last_file)
    print("✅ Read successfully with pandas")
    print("Columns:", df.columns.tolist())
    print(f"Rows: {len(df)}")
    print("First row:", df.iloc[0].to_dict() if not df.empty else "Empty DataFrame")
except Exception as e:
    print(f"❌ Error reading file: {e}")
