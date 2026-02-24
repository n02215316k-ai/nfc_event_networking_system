filepath = 'src/controllers/profile_controller.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"\n📄 First 50 lines of profile_controller.py:\n")
    print("=" * 80)
    
    for i in range(min(50, len(lines))):
        line_num = i + 1
        print(f"{line_num:4d} | {lines[i]}", end='')
    
    print("=" * 80)
    
    # Also show around line 317
    print(f"\n📄 Lines 310-325 (around the error):\n")
    print("=" * 80)
    
    for i in range(max(0, 309), min(325, len(lines))):
        line_num = i + 1
        marker = ">>> " if i == 316 else "    "
        print(f"{marker}{line_num:4d} | {lines[i]}", end='')
    
    print("=" * 80)

except Exception as e:
    print(f"Error: {e}")