import re
import json

path = r"d:\ViaMX_Global_Publico\index.html"
try:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Extract window.CATALOGO
match = re.search(r'window\.CATALOGO\s*=\s*(\[.*?\]);', content, re.DOTALL)
if not match:
    print("Could not find window.CATALOGO")
    exit(1)

catalogo = json.loads(match.group(1))

print(f"Total products in window.CATALOGO: {len(catalogo)}")

# Default filter values
query = ""
category = "all"
priceLimit = 35000.0
selectedCity = "all" # or whatever the default radio button is (which is "all")

print("\nSimulating filter with: query='', category='all', priceLimit=35000, selectedCity='all'")
filtered = []
for p in catalogo:
    matchesQuery = query in p['title'].lower() or query in p['description'].lower()
    matchesCategory = (category == 'all' or p['category'] == category)
    matchesPrice = p['price'] <= priceLimit
    
    # In JS: matchesCity = (selectedCity === 'all' || prod.city === selectedCity || prod.city === 'all')
    prod_city = p.get('city', 'all')
    matchesCity = (selectedCity == 'all' or prod_city == selectedCity or prod_city == 'all')
    
    is_match = matchesQuery and matchesCategory and matchesPrice and matchesCity
    if is_match:
        filtered.append(p)
        print(f"  MATCH: {p['id']} - {p['title']} (Price: {p['price']}, City: {prod_city}, Category: {p['category']})")
    else:
        print(f"  FILTERED OUT: {p['id']} - {p['title']} (Price: {p['price']}, City: {prod_city}, Category: {p['category']})")
        print(f"    Reasons: matchesQuery={matchesQuery}, matchesCategory={matchesCategory}, matchesPrice={matchesPrice}, matchesCity={matchesCity}")

print(f"\nFiltered count: {len(filtered)}")
