with open(r"d:\Downloads\Proyecto Web\index.html", 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("window.CATALOGO.push(normalizedProd);")
if idx != -1:
    with open(r"d:\Downloads\Proyecto Web\load_catalog_part3.txt", 'w', encoding='utf-8') as f:
        f.write(content[idx:idx+1500])
    print("Wrote load_catalog_part3.txt")
else:
    print("window.CATALOGO.push not found")
