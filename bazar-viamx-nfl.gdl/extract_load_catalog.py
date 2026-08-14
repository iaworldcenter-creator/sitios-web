import re

with open(r"d:\Downloads\Proyecto Web\index.html", 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("async function loadCatalogData()")
if idx != -1:
    # Let's extract 5000 characters from there
    fn_content = content[idx:idx+5000]
    
    # We find the end of the function. Let's write it to a file.
    with open(r"d:\Downloads\Proyecto Web\load_catalog_fn.txt", 'w', encoding='utf-8') as f:
        f.write(fn_content)
    print("Extracted loadCatalogData successfully.")
else:
    print("Could not find loadCatalogData definition.")
