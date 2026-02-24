filepath = 'src/controllers/system_manager_controller.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find reports function (around line 544)
    start = max(0, 530)
    end = min(len(lines), 560)
    
    print(f"\n📄 Lines {start}-{end} of system_manager_controller.py:\n")
    print("=" * 80)
    
    for i in range(start, end):
        line_num = i + 1
        print(f"{line_num:4d} | {lines[i]}", end='')
    
    print("=" * 80)
    
except Exception as e:
    print(f"Error: {e}")