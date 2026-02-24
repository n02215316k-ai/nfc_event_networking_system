filepath = 'src/controllers/system_manager_controller.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the reports function
    for i, line in enumerate(lines):
        if "def reports():" in line:
            print(f"\n📍 Found 'def reports():' at line {i + 1}\n")
            print("=" * 80)
            
            # Show 20 lines before and 60 lines after
            start = max(0, i - 5)
            end = min(len(lines), i + 60)
            
            for j in range(start, end):
                line_num = j + 1
                marker = ">>> " if j == i else "    "
                print(f"{marker}{line_num:4d} | {lines[j]}", end='')
            
            print("=" * 80)
            break
    else:
        print("Could not find 'def reports():' function")

except Exception as e:
    print(f"Error: {e}")