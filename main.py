import json
import os
from scraper import obtener_puestos
from telegram_bot import enviar_mensaje

DATA_FILE = "data/puestos.json"
os.makedirs("data", exist_ok=True)

def cargar_json_seguro(ruta, default):
    if not os.path.exists(ruta):
        return default
    if os.path.getsize(ruta) == 0:
        return default
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default

# ------------------ MAIN ------------------

puestos_actuales = obtener_puestos()
puestos_anteriores = cargar_json_seguro(DATA_FILE, [])

set_actual = {json.dumps(p, sort_keys=True) for p in puestos_actuales}
set_anterior = {json.dumps(p, sort_keys=True) for p in puestos_anteriores}

nuevos = set_actual - set_anterior

if nuevos:
    mensaje = f"📚 *NUEVOS PUESTOS DE BIBLIOTECARIO* ({len(nuevos)})\n\n"

    for n in nuevos:
        p = json.loads(n)

        mensaje += (
            f"🆔 *Reg:* {p.get('reg', 'N/D')}\n"
            f"🏫 *Institución:* {p.get('institucion', 'N/D')}\n"
            f"📅 *Vigencia:* {p.get('vigencia_desde', 'N/D')} → {p.get('vigencia_hasta', 'N/D')}\n"
            f"📍 *Domicilio:* {p.get('domicilio', 'N/D')}\n"
            f"🕒 *Turno:* {p.get('turno', 'N/D')}\n"
            f"⏰ *Horario:* {p.get('horario', 'N/D')}\n"
            f"📌 *Carácter:* {p.get('caracter', 'N/D')}\n"
            f"📝 *Motivo:* {p.get('motivo', 'N/D')}\n\n"
            f"🔗 Para más info:\n{p.get('url', '')}\n\n"
            "────────────────────\n\n"
        )

    enviar_mensaje(mensaje)

# Guardar nuevo estado
with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(puestos_actuales, f, ensure_ascii=False, indent=2)
