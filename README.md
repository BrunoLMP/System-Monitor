# 🖥️ System Monitor (Python)

Um monitor de sistema leve para Windows, desenvolvido em Python, que exibe informações em tempo real diretamente na bandeja do sistema.

## ✨ Funcionalidades

- 📊 Uso total da CPU
- 🧠 Núcleos da CPU (expandir/recolher)
- 💾 Uso de memória RAM
- 🔋 Status da bateria (notebooks)
- 💽 Monitoramento de múltiplos discos
- 🧭 Ícone na bandeja do sistema
- 🪟 Janela com tamanho fixo
- 🚫 Sem necessidade de permissões administrativas

## 🧰 Tecnologias utilizadas

- Python 3
- Tkinter
- psutil
- pystray
- Pillow

## ▶️ Como executar (modo desenvolvimento)

```bash
pip install psutil pystray pillow
python monitor.py
```
## 📦 Gerar executável (.exe)
```bash
pyinstaller --onefile --windowed --icon=icon.ico monitor.py
```
O executável será criado na pasta dist/.

## 🖼️ Interface

Clique na linha da CPU para expandir os núcleos
Controle pela bandeja do sistema (mostrar / ocultar / sair)
