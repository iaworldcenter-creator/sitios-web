with open(r"E:\sitios web\pc-custom-lab\index.html", 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("".join(lines[:140]))
