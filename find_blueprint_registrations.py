filepath = 'app.py'

print("\n📄 Searching for blueprint registrations in app.py...\n")
print("=" * 80)

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("All lines containing 'register_blueprint':\n")

for i, line in enumerate(lines):
    if 'register_blueprint' in line:
        line_num = i + 1
        spaces = len(line) - len(line.lstrip())
        print(f"Line {line_num:3d} | [{spaces:2d} spaces] {line.strip()}")

print("\n" + "=" * 80)

# Also check for blueprint creation/initialization
print("\nAll lines containing 'Blueprint':\n")

for i, line in enumerate(lines):
    if 'Blueprint' in line and 'import' in line:
        line_num = i + 1
        print(f"Line {line_num:3d} | {line.strip()}")

print("\n" + "=" * 80)

# Show the entire function where blueprints should be registered
print("\nLooking for create_app() or main initialization...\n")

in_function = False
function_lines = []

for i, line in enumerate(lines):
    if 'def create_app' in line or 'if __name__' in line:
        in_function = True
        start_line = i
    
    if in_function:
        function_lines.append((i+1, line))
        
        if len(function_lines) > 50:  # Show first 50 lines of function
            break

if function_lines:
    print(f"Found initialization section starting at line {start_line + 1}:\n")
    for line_num, line in function_lines:
        print(f"{line_num:3d} | {line}", end='')
else:
    print("Could not find standard Flask initialization")

print("\n" + "=" * 80)