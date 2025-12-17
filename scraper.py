import requests
from bs4 import BeautifulSoup

URL = "http://desecvacantes.jujuy.edu.ar/FormPublic/frmDSecSel.aspx"

def obtener_puestos():
    session = requests.Session()

    # 1. GET inicial
    r = session.get(URL)
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
    r = session.post(URL, data=data)
    soup = BeautifulSoup(r.text, "html.parser")

    tabla = soup.find("table", id="Contenido_gvCargos")
    if not tabla:
        return []

    puestos = []

    for fila in tabla.find_all("tr")[1:]:
        c = [td.get_text(strip=True) for td in fila.find_all("td")]
        puestos.append({
            "institucion": c[3],
            "cargo": c[5],
            "horas": c[6],
            "curso": f"{c[7]} {c[8]}",
            "turno": c[9]
        })

    return puestos
