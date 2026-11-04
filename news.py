import urllib.request
import xml.etree.ElementTree as ET
import os
import textwrap

# Ruta del archivo ASCII de la taza
ascii_path = os.path.expanduser('~/elArregladorStudio.txt')

# Cargar líneas del arte ASCII
ascii_lines = open(ascii_path).read().splitlines() if os.path.exists(ascii_path) else []
max_ascii_w = max([len(l) for l in ascii_lines], default=0)

# Obtener noticias de Google News (Prensa de España) - Cambiado a 4 titulares
url = 'https://news.google.com/rss?hl=es&gl=ES&ceid=ES:es'
root = ET.fromstring(urllib.request.urlopen(url).read())
items = root.findall('.//item')[:4]

# Formatear filas de noticias manteniendo hipervínculos funcionales para Warp
rows = []
for i, item in enumerate(items):
    title = f"{i+1}. {item.find('title').text}"
    link = item.find('link').text
    wrapped_lines = textwrap.wrap(title, width=55)
    
    for line in wrapped_lines:
        rows.append((f"\033]8;;{link}\033\\{line}\033]8;;\033\\", len(line)))
    rows.append(('', 0))  # Espacio entre titulares

# Imprimir taza a la izquierda y noticias alineadas a la derecha
max_len = max(len(ascii_lines), len(rows))
for i in range(max_len):
    ascii_col = (ascii_lines[i] if i < len(ascii_lines) else "").ljust(max_ascii_w)
    news_col = rows[i][0] if i < len(rows) else ""
    print(f"{ascii_col}   {news_col}")
