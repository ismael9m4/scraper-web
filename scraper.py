import requests
from bs4 import BeautifulSoup
import re

URL = "http://desecvacantes.jujuy.edu.ar/FormPublic/frmDSecSel.aspx"

# Regex robusta:
# - bibliotecario
# - bibliotecaria
# - bibliotecario/a
# - sin importar mayúsculas
PATRON_CARGO = re.compile(
    r"\bBIBLIOTECARI(O|A)(/A)?\b",
    re.IGNORECASE
)

def obtener_puestos():
    session = requests.Session()

    # 1. GET inicial
    r = session.get(URL, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    # 2. Extraer campos ocultos
    data = {
        "__VIEWSTATE": soup.find(id="__VIEWSTATE")["value"],
        "__VIEWSTATEGENERATOR": soup.find(id="__VIEWSTATEGENERATOR")["value"],
        "__EVENTVALIDATION": soup.find(id="__EVENTVALIDATION")["value"],
        "Contenido_txtEspacioCurricular": "BIBLIOTECARIO",
        "Contenido_btnBuscar": "Buscar"
    }

    # 3. POST con búsqueda
    r = session.post(URL, data=data, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    tabla = soup.find("table", id="Contenido_gvCargos")
    if not tabla:
        return []

    puestos = []

    for fila in tabla.find_all("tr")[1:]:
        celdas = [td.get_text(strip=True) for td in fila.find_all("td")]
        if len(celdas) < 10:
            continue

        cargo = celdas[5].strip()

        # 🔴 FILTRO DEFINITIVO (ANTI FALSOS POSITIVOS)
        if not PATRON_CARGO.search(cargo):
            continue

        puestos.append({
            "institucion": celdas[3],
            "cargo": cargo,
            "horas": celdas[6],
            "curso": f"{celdas[7]} {celdas[8]}",
            "turno": celdas[9]
        })

    return puestos
