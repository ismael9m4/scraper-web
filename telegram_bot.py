import requests
import os
import re

def escape_md(text):
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', str(text))

def enviar_mensaje(texto):
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    texto = escape_md(texto)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": texto,
            "parse_mode": "MarkdownV2"
        }
    )
