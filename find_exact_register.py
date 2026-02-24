with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = None
end = None

for i, line in enumerate(lines):
    if "@app.route('/register'" in line:
        start = i
        print(f"Registration starts at line {i+1}")
    
    if start is not None and end is None:
        if i > start and (line.startswith('@app.route') or (line.startswith('def ') and not line.startswith('    '))):
            end = i
            print(f"Registration ends at line {i}")
            break

if start:
    print(f"\nShowing registration route (lines {start+1} to {end}):\n")
    for i in range(start, end if end else start + 50):
        print(f"{i+1:4d}: {lines[i]}", end='')