path = r"d:\ViaMX_Global_Publico\index.html"
try:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
except Exception as e:
    print(f"Error: {e}")
    exit(1)

idx = content.find("async function applyClientGeotargeting()")
if idx != -1:
    with open(r"d:\Downloads\Proyecto Web\d_geotargeting.txt", 'w', encoding='utf-8') as f:
        f.write(content[idx:idx+3500])
    print("Wrote d_geotargeting.txt")
else:
    print("applyClientGeotargeting NOT found in d:\\ViaMX_Global_Publico\\index.html")
