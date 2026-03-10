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
        if len(celdas) < 15:
            continue

        cargo = celdas[5].strip()

        # 🔴 FILTRO DEFINITIVO (ANTI FALSOS POSITIVOS)
        if not PATRON_CARGO.search(cargo):
            continue

        puesto = {
            "vigencia_desde": cols[0].get_text(strip=True),
            "vigencia_hasta": cols[1].get_text(strip=True),
            "reg": cols[2].get_text(strip=True),
            "institucion": cols[3].get_text(strip=True),
            "domicilio": cols[4].get_text(strip=True),
            "cargo": cols[5].get_text(strip=True),
            "turno": cols[9].get_text(strip=True),
            "horario": cols[10].get_text(strip=True),
            "caracter": cols[11].get_text(strip=True),
            "desde": cols[12].get_text(strip=True),
            "hasta": cols[13].get_text(strip=True),
            "motivo": cols[14].get_text(strip=True),
            "url": URL
        }

        puestos.append(puesto)

    return puestos
