import time
import psutil
import threading
import tkinter as tk
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

# ---------------- Estado global ----------------
dados = {
    "cpu": 0,
    "cpu_cores": [],
    "ram": 0,
    "bateria": None,
    "discos": []
}
mostrar_nucleos=False
rodando = True

# ---------------- Monitor ----------------
def monitor_loop():
    global dados
    while rodando:
        dados["cpu"] = psutil.cpu_percent()
        dados["cpu_cores"] = psutil.cpu_percent(percpu=True)

        mem = psutil.virtual_memory()
        dados["ram"] = mem.percent

        bat = psutil.sensors_battery()
        if bat:
            dados["bateria"] = (bat.percent, bat.power_plugged)
        else:
            dados["bateria"] = None

        discos = []
        for part in psutil.disk_partitions():
            try:
                uso = psutil.disk_usage(part.mountpoint)
                discos.append((part.device, uso.used, uso.total,uso.percent,))
            except PermissionError:
                pass

        dados["discos"] = discos

        time.sleep(1)

# ---------------- Tkinter UI (THREAD PRINCIPAL) ----------------
root = tk.Tk()
root.title("System Monitor")
root.geometry("260x260")
root.resizable(False, False)

label_cpu = tk.Label(
    root,
    font=("Consolas", 10,),
    anchor="w",
    cursor="hand2"
)
label_cpu.pack(fill="x", padx=10, pady=(5, 0))

label_info = tk.Label(
    root,
    font=("Consolas", 10),
    justify="left",
    anchor="nw"
)
label_info.pack(fill="both", expand=True, padx=10, pady=(0, 10))

label_cpu.config(cursor="hand2")
def toggle_cpu(event=None):
    global mostrar_nucleos
    mostrar_nucleos = not mostrar_nucleos
label_cpu.bind("<Button-1>", toggle_cpu)
def atualizar_ui():
    seta = " ▼" if mostrar_nucleos else " ▶"
    label_cpu.config(text=f"CPU Total: {dados['cpu']}%{seta} ")
    texto = ""
    if mostrar_nucleos:
        for i, core in enumerate(dados["cpu_cores"]):
            texto += f"Core {i}: {core}%\n"
    
    texto += f"RAM: {dados['ram']}%\n"

    if dados["bateria"]:
        percent, plugged = dados["bateria"]
        estado = "Carregando" if plugged else "Descarregando"
        texto += f"Bateria: {percent}% ({estado})\n"

    for d, used, total, percent in dados["discos"]:
        used_gb = used / (1024**3)
        total_gb = total / (1024**3)
        texto += f"{d}: {used_gb:.1f}/{total_gb:.1f} GB ({percent})%\n"
    label_info.config(text=texto)
    root.after(100, atualizar_ui)


def mostrar():
    root.deiconify()

def ocultar():
    root.withdraw()

root.after(1000, atualizar_ui)

# ---------------- Tray ----------------
def criar_icone():
    img = Image.new("RGB", (64, 64), "black")
    d = ImageDraw.Draw(img)
    d.rectangle((16, 16, 48, 48), fill="green")
    return img

def on_mostrar(icon, item):
    root.after(0, mostrar)

def on_ocultar(icon, item):
    root.after(0, ocultar)

def on_sair(icon, item):
    global rodando
    rodando = False
    icon.stop()
    root.after(0, root.destroy)

menu = (
    item("Mostrar", on_mostrar),
    item("Ocultar", on_ocultar),
    item("Sair", on_sair),
)

icon = pystray.Icon("SystemMonitor", criar_icone(), "System Monitor", menu)

# ---------------- Start ----------------
threading.Thread(target=monitor_loop, daemon=True).start()
threading.Thread(target=icon.run, daemon=True).start()

root.mainloop()
