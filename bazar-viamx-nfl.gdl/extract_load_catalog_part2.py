with open(r"d:\Downloads\Proyecto Web\index.html", 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("problemSolved: ")
if idx != -1:
    with open(r"d:\Downloads\Proyecto Web\load_catalog_part2.txt", 'w', encoding='utf-8') as f:
        f.write(content[idx:idx+1500])
    print("Wrote load_catalog_part2.txt")
else:
    print("problemSolved not found")
