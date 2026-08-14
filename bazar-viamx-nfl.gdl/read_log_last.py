with open(r"d:\Downloads\Proyecto Web\log_operativo.txt", 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print(f"Total lines in log: {len(lines)}")
print("--- Last 100 lines ---")
for line in lines[-100:]:
    print(line, end='')
