import platform
import socket
import psutil
import wmi
import requests
import os

def convert_bytes_to_readable(bytes_value):
    if bytes_value < 1024:
        return f"{bytes_value} B"
    elif bytes_value < 1024 ** 2:
        return f"{bytes_value / 1024:.2f} KB"
    elif bytes_value < 1024 ** 3:
        return f"{bytes_value / (1024 ** 2):.2f} MB"
    else:
        return f"{bytes_value / (1024 ** 3):.2f} GB"

def get_system_info():
    system_info = {}

    system_info["TipoDeEquipo"] = platform.node().lower()
    system_info["S.O."] = platform.platform()

    c = wmi.WMI()
    memory = c.Win32_PhysicalMemory()
    total_ram = sum([int(m.Capacity) for m in memory])
    system_info["RAM"] = str(total_ram // (1024 ** 3)) + " GB"

    for mem_module in memory:
        if hasattr(mem_module, 'Speed'):
            system_info["FrecuenciaRAM"] = f"{mem_module.Speed} MHz"
            break

    for board in c.Win32_BaseBoard():
        system_info["PlacaMadre"] = board.Product

    processor = c.Win32_Processor()[0]
    system_info["Procesador"] = processor.Name

    network_adapters = psutil.net_if_addrs()
    system_info["ListaAdaptadores"] = list(network_adapters.keys())

    system_info["IP"] = socket.gethostbyname(socket.gethostname())

    partitions = psutil.disk_partitions()
    storage_info = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        storage_info.append(
            f"{partition.device} Libre:{convert_bytes_to_readable(usage.free)} Usado:{convert_bytes_to_readable(usage.used)}"
        )

    system_info["Almacenamiento"] = storage_info
    system_info["CantidadDiscos"] = len(partitions)

    return system_info

def send_telegram(message):
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})

if __name__ == "__main__":
    info = get_system_info()

    mensaje = "📡 *Reporte del sistema*\n\n"
    for k, v in info.items():
        mensaje += f"{k}: {v}\n"

    send_telegram(mensaje)
