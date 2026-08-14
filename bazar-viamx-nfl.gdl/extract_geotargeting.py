with open(r"d:\Downloads\Proyecto Web\index.html", 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("function applyClientGeotargeting()")
if idx != -1:
    with open(r"d:\Downloads\Proyecto Web\geotargeting_fn.txt", 'w', encoding='utf-8') as f:
        f.write(content[idx:idx+1500])
    print("Wrote geotargeting_fn.txt")
else:
    # Let's search for applyClientGeotargeting without function keyword
    idx2 = content.find("applyClientGeotargeting")
    if idx2 != -1:
        with open(r"d:\Downloads\Proyecto Web\geotargeting_fn.txt", 'w', encoding='utf-8') as f:
            f.write(content[idx2-50:idx2+1500])
        print("Wrote geotargeting_fn.txt (using general keyword search)")
    else:
        print("applyClientGeotargeting not found")
