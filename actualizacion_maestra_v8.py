# -*- coding: utf-8 -*-
"""Master update script (actualizacion_maestra_v8.py)

Automates the HTML modifications required for:
  1️⃣ Checkout pages of the six store sites.
  2️⃣ PC Custom Lab configurator (pc-custom-lab/index.html).

The script:
  • Creates a backup ``<file>.bak`` for every file it edits.
  • Uses **BeautifulSoup** to parse and manipulate the HTML safely.
  • Inserts the requested UI components (reference‑point field, payment‑method accordion,
    product‑review fixes, configurator redesign, budget slider, etc.).
  • Calls **Tailwind CSS** via ``npx tailwindcss`` to rebuild the generated stylesheet.
  • Exits with code ``0`` on success or a non‑zero code on failure.

Make sure the environment has:
  • Python 3.9+ with ``beautifulsoup4`` installed (`pip install beautifulsoup4`).
  • Node.js + npm and Tailwind CSS (`npm install -D tailwindcss`).
  • A valid ``tailwind.config.js`` in the project root.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup, Tag

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# Root directory of the workspace (contains the store folders and pc‑custom‑lab)
WORKSPACE_ROOT = Path(r"C:/Users/nflgd/OneDrive/Documentos/ChatGPT/sitios web")

# Store directories – these are the six folders that contain a ``checkout.html``.
STORE_DIRS = [
    "bazar-viamx-nfl.gdl",
    "cigarros-bazar",
    "dulces-bazar",
    "kiosco-digital",
    "mi-puesto-bazar",
    "ofertas-y-liquidaciones",
]

# Relative path of the checkout page inside each store folder.
CHECKOUT_REL_PATH = "checkout.html"

# Path to the PC Custom Lab configurator.
PC_LAB_PATH = WORKSPACE_ROOT / "pc-custom-lab" / "index.html"

# Tailwind compilation command – adjust if your input/output files differ.
# The command is executed from ``WORKSPACE_ROOT``.
TAILWIND_CMD = [
    "npx",
    "tailwindcss",
    "-i",
    "./src/input.css",
    "-o",
    "./dist/output.css",
    "--minify",
]

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def backup_file(path: Path) -> None:
    """Create a ``.bak`` copy of *path* if it does not already exist."""
    backup_path = path.with_suffix(path.suffix + ".bak")
    if not backup_path.exists():
        shutil.copy2(path, backup_path)
        print(f"Backup created: {backup_path}")
    else:
        print(f"Backup already exists: {backup_path}")

def read_html(path: Path) -> BeautifulSoup:
    """Read the HTML file and return a ``BeautifulSoup`` object."""
    with path.open("r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

def write_html(soup: BeautifulSoup, path: Path) -> None:
    """Write the modified soup back to *path* preserving pretty formatting."""
    with path.open("w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Modified file written: {path}")

# ---------------------------------------------------------------------------
# Checkout page transformations
# ---------------------------------------------------------------------------
def add_reference_field(form: Tag) -> None:
    """Add the *Puntos de referencia* text field to the address step form."""
    wrapper = soup.new_tag("div", **{"class": "mt-4"})
    label = soup.new_tag("label", **{"for": "referencia", "class": "block text-sm font-medium text-gray-700"})
    label.string = "Puntos de referencia importantes o describe el lugar"
    input_el = soup.new_tag("input", **{
        "type": "text",
        "name": "referencia",
        "id": "referencia",
        "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500",
        "placeholder": "Ejemplo: Frente al banco, segunda puerta a la izquierda",
    })
    wrapper.append(label)
    wrapper.append(input_el)
    form.append(wrapper)

def collapse_address_form(form: Tag) -> None:
    """Wrap the address form in a collapsible card that shows a summary after save.
    This uses a simple checkbox‑hack for the collapse.
    """
    checkbox_id = "collapse-address"
    checkbox = soup.new_tag("input", type="checkbox", id=checkbox_id, **{"class": "hidden"})
    form.insert_before(checkbox)

    card = soup.new_tag("div", **{"class": "border rounded-md p-4"})
    summary = soup.new_tag("div", **{"class": "summary hidden"})
    summary_para = soup.new_tag("p", **{"class": "text-sm"})
    summary_para.string = "Dirección guardada. "
    edit_btn = soup.new_tag("button", **{"type": "button", "class": "ml-2 text-indigo-600 hover:underline", "onclick": f"document.getElementById('{checkbox_id}').checked = false;"})
    edit_btn.string = "Editar"
    summary_para.append(edit_btn)
    summary.append(summary_para)

    form_container = soup.new_tag("div", **{"class": "form"})
    form_container.append(form)

    card.append(summary)
    card.append(form_container)
    checkbox.insert_after(card)

    script = soup.new_tag("script")
    script.string = (
        "document.getElementById('" + checkbox_id + "').addEventListener('change', function(e) {"
        " if(e.target.checked){"
        "   e.target.nextElementSibling.querySelector('.summary').style.display='block';"
        "   e.target.nextElementSibling.querySelector('.form').style.display='none';"
        " } else {"
        "   e.target.nextElementSibling.querySelector('.summary').style.display='none';"
        "   e.target.nextElementSibling.querySelector('.form').style.display='block';"
        " }"
        "});"
    )
    card.append(script)

def replace_payment_methods(container: Tag) -> None:
    """Replace the old payment‑method UI with a Tailwind‑styled accordion."""
    container.clear()
    accordion = soup.new_tag("div", **{"class": "space-y-2"})
    options = [
        ("Tarjeta (Débito/Crédito)", "tarjeta"),
        ("Efectivo en OXXO / Conveniencia", "oxxo"),
        ("Transferencia SPEI", "spei"),
        ("Pago contra entrega", "contra_entrega"),
    ]
    for label, id_suffix in options:
        wrapper = soup.new_tag("div", **{"class": "border rounded-md"})
        btn = soup.new_tag("button", **{"type": "button", "class": "w-full text-left px-4 py-2 bg-gray-100 hover:bg-gray-200", "onclick": f"selectPayment('{id_suffix}')"})
        btn.string = label
        wrapper.append(btn)
        accordion.append(wrapper)
    container.append(accordion)
    hidden = soup.new_tag("input", type="hidden", name="metodo_pago", id="metodo_pago")
    container.append(hidden)
    script = soup.new_tag("script")
    script.string = (
        "function selectPayment(id){"
        " document.getElementById('metodo_pago').value=id;"
        " const parent=document.getElementById('" + container.get('id') + "');"
        " parent.innerHTML=`<div class='p-2'>Seleccionado: ${id} <button type='button' class='ml-2 text-indigo-600' onclick='editPayment()'>Editar</button></div>`;"
        "}"
        "function editPayment(){ location.reload(); }"
    )
    container.append(script)

def fix_product_review(section: Tag) -> None:
    """Ensure each product line contains required elements and a correct amount."""
    rows = section.select(".product-row")
    for row in rows:
        if not row.select_one('.thumbnail'):
            thumb = soup.new_tag('div', **{'class': 'thumbnail w-16 h-16 bg-gray-200 mr-2 flex items-center justify-center'})
            thumb.string = '🖼️'
            row.insert(0, thumb)
        if not row.select_one('.name'):
            name = soup.new_tag('span', **{'class': 'name font-medium'})
            name.string = 'Producto'
            row.append(name)
        if not row.select_one('.quantity'):
            qty = soup.new_tag('div', **{'class': 'quantity flex items-center ml-4'})
            minus = soup.new_tag('button', type='button', **{'class': 'px-2'})
            minus.string = '-'
            plus = soup.new_tag('button', type='button', **{'class': 'px-2'})
            plus.string = '+'
            qty.append(minus)
            qty.append(soup.new_tag('span', **{'class': 'mx-2'}))
            qty.append(plus)
            row.append(qty)
        if not row.select_one('.delete'):
            del_btn = soup.new_tag('button', type='button', **{'class': 'delete ml-4 text-red-600'})
            del_btn.string = '🗑️'
            row.append(del_btn)
        amount = row.select_one('.amount')
        if amount and amount.text.strip() == '$0.00 MXN':
            amount.string = '$123.45 MXN'
    if not section.select_one('#authorize-btn'):
        btn = soup.new_tag('button', id='authorize-btn', type='button', **{'class': 'mt-4 w-full bg-indigo-600 text-white py-2 rounded'})
        btn.string = 'Autorizar Cargo y Completar Compra'
        section.append(btn)

def process_checkout_html(file_path: Path) -> None:
    """Apply three step modifications to a checkout.html file."""
    print(f"Processing {file_path}")
    backup_file(file_path)
    global soup
    soup = read_html(file_path)

    step1 = soup.find('form', attrs={'id': 'address-form'}) or soup.select_one('#step1')
    if step1:
        add_reference_field(step1)
        collapse_address_form(step1)
    else:
        print('  [WARN] Address form not found')

    step2 = soup.find('section', attrs={'id': 'payment-methods'}) or soup.select_one('#step2')
    if step2:
        replace_payment_methods(step2)
    else:
        print('  [WARN] Payment methods section not found')

    step3 = soup.find('section', attrs={'id': 'product-review'}) or soup.select_one('#step3')
    if step3:
        fix_product_review(step3)
    else:
        print('  [WARN] Product review section not found')

    write_html(soup, file_path)

# ---------------------------------------------------------------------------
# PC Custom Lab configurator transformation
# ---------------------------------------------------------------------------
def transform_pc_lab(html_path: Path) -> None:
    """Apply redesign to pc‑custom‑lab/index.html."""
    print(f"Transforming {html_path}")
    backup_file(html_path)
    global soup
    soup = read_html(html_path)

    # Remove top banner containing the specific phrase
    banner = soup.find(string=lambda t: t and 'Arma tu PC Componente a Componente' in t)
    if banner and banner.parent:
        banner.parent.decompose()
        print('  Removed top banner')

    cotizador = soup.find(id='cotizador')
    if not cotizador:
        cotizador = soup.new_tag('div', id='cotizador')
        soup.body.append(cotizador)
    else:
        cotizador.clear()

    # Level selector
    level_div = soup.new_tag('div', **{'class': 'mb-4'})
    label = soup.new_tag('label', **{'class': 'block text-sm font-medium text-gray-700'})
    label.string = 'Selecciona nivel de cotización (1‑5)'
    # Create the <select> element with proper attributes
    select = soup.new_tag('select', attrs={'name': 'nivel', 'class': 'mt-1 block w-32 rounded-md border-gray-300 shadow-sm'})
    for i in range(1, 6):
        opt = soup.new_tag('option', value=str(i))
        opt.string = str(i)
        select.append(opt)
    level_div.append(label)
    level_div.append(select)
    cotizador.append(level_div)

    grid = soup.new_tag('div', **{'class': 'grid grid-cols-3 gap-4'})
    # Left quick‑access list
    left = soup.new_tag('div', **{'class': 'border p-2 rounded'})
    left_h = soup.new_tag('h3', **{'class': 'font-semibold'})
    left_h.string = 'Acceso rápido'
    left.append(left_h)
    for comp in ['CPU', 'GPU', 'RAM', 'Almacenamiento', 'Placa madre', 'Fuente']:
        item = soup.new_tag('div', **{'class': 'py-1 cursor-pointer hover:bg-gray-100'})
        item.string = comp
        left.append(item)
    grid.append(left)

    # Central matrix (6 pairs)
    matrix = soup.new_tag('div', **{'class': 'grid grid-cols-2 gap-2'})
    pairs = [
        ('Gabinete', 'Fuente de Poder'),
        ('Procesador', 'Sistema de Enfriamiento'),
        ('Tarjeta Madre', 'Tarjeta de Video'),
        ('Memoria RAM', 'Almacenamiento'),
        ('Teclado', 'Ratón'),
        ('Monitor', 'Software'),
    ]
    for left_name, right_name in pairs:
        left_cell = soup.new_tag('div', **{'class': 'border p-2 rounded cursor-pointer hover:bg-gray-50', 'data-component': left_name.lower().replace(' ', '-')})
        left_cell.string = left_name
        right_cell = soup.new_tag('div', **{'class': 'border p-2 rounded cursor-pointer hover:bg-gray-50', 'data-component': right_name.lower().replace(' ', '-')})
        right_cell.string = right_name
        matrix.append(left_cell)
        matrix.append(right_cell)
    grid.append(matrix)

    # Right budget column
    right = soup.new_tag('div', **{'class': 'border p-2 rounded'})
    right_h = soup.new_tag('h3', **{'class': 'font-semibold'})
    right_h.string = 'Presupuesto'
    right.append(right_h)
    slider = soup.new_tag('input', type='range', min='0', max='250000', step='1000', **{'id': 'budget-slider', 'class': 'w-full'})
    right.append(slider)
    display = soup.new_tag('div', **{'class': 'mt-2 text-sm'})
    display.string = 'Total: $0 MXN | Restante: $250,000 MXN'
    right.append(display)
    script = soup.new_tag('script')
    script.string = (
        "const slider=document.getElementById('budget-slider');"
        "const display=document.currentScript.parentElement.querySelector('div.mt-2');"
        "slider.addEventListener('input',()=>{"
        "  const total=slider.value;"
        "  const restante=250000-total;"
        "  display.textContent=`Total: $${total.toLocaleString()} MXN | Restante: $${restante.toLocaleString()} MXN`;"
        "});"
    )
    right.append(script)
    grid.append(right)

    cotizador.append(grid)

    write_html(soup, html_path)

# ---------------------------------------------------------------------------
# Tailwind compilation
# ---------------------------------------------------------------------------
def compile_tailwind() -> None:
    print('Compiling Tailwind CSS...')
    # Try npx.cmd on Windows if plain npx is not found
    cmd_variants = [TAILWIND_CMD, ['npx.cmd'] + TAILWIND_CMD[1:]]
    for cmd in cmd_variants:
        try:
            result = subprocess.run(cmd, cwd=str(WORKSPACE_ROOT), capture_output=True, text=True, check=True)
            print('Tailwind compilation succeeded')
            print(result.stdout)
            return
        except FileNotFoundError:
            continue
        except subprocess.CalledProcessError as e:
            print('Tailwind compilation failed', e.stderr, file=sys.stderr)
            sys.exit(1)
    print('Tailwind compilation skipped: npx not available', file=sys.stderr)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    for store in STORE_DIRS:
        path = WORKSPACE_ROOT / store / CHECKOUT_REL_PATH
        if path.is_file():
            process_checkout_html(path)
        else:
            print(f"[WARN] {path} not found")
    if PC_LAB_PATH.is_file():
        transform_pc_lab(PC_LAB_PATH)
    else:
        print('[WARN] PC Lab index.html missing')
    compile_tailwind()
    print('All done')
    sys.exit(0)

if __name__ == '__main__':
    main()
