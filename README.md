# 🔍 nmap-auto-scanner


[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://nmap.org/)
[![Maintained](https://img.shields.io/badge/status-actively--maintained-brightgreen)](https://github.com/rafaelmperez/nmap-auto-scanner/commits/main)

Automatiza escaneos de red con Nmap, genera reportes en JSON/CSV y detecta cambios entre ejecuciones para facilitar auditorías técnicas y tareas de blue team. Ideal para profesionales de ciberseguridad, sysadmins y estudiantes de análisis de vulnerabilidades.

---

## 📑 Tabla de contenidos

- [🎯 Objetivo](#-objetivo)
- [⚙️ Tecnologías utilizadas](#️-tecnologías-utilizadas)
- [📦 Requisitos](#-requisitos)
- [🛠 Instalación](#-instalación)
- [🚀 Ejecución](#-ejecución)
- [🗂️ Estructura del proyecto](#️-estructura-del-proyecto)
- [⚙️ Ejemplo de config.yaml](#️-ejemplo-de-configyaml)
- [⏰ Ejecución automática con cron](#-ejecución-automática-con-cron)
- [📊 Comparación entre escaneos](#-comparación-entre-escaneos)
- [🧪 Ejemplo de salida](#-ejemplo-de-salida)
- [🧩 Mejoras futuras](#-mejoras-futuras)
- [👨‍💻 Autor](#-autor)

---

## 🎯 Objetivo

`nmap-auto-scanner` nace como herramienta de automatización defensiva para entornos Linux. Escanea redes de forma regular, analiza los servicios activos y permite comparar resultados entre escaneos con el fin de detectar cambios, nuevos servicios o posibles amenazas.

🔐 Útil para:
- Auditorías periódicas de red
- Tareas de bastionado
- Detección temprana de exposición
- Gestión de activos

---

## ⚙️ Tecnologías utilizadas

| Herramienta      | Uso principal                           |
|------------------|------------------------------------------|
| [Python 3.10+](https://www.python.org/)     | Lógica de automatización             |
| [Nmap](https://nmap.org/)                 | Escaneo de red                       |
| [python-nmap](https://pypi.org/project/python-nmap/) | Wrapper para ejecutar Nmap desde Python |
| YAML + Logging    | Configuración modular + trazabilidad    |
| `cron`            | Ejecución programada semanal            |

---

## 📦 Requisitos

- Linux con acceso a terminal
- Python 3.10 o superior
- Nmap instalado (`sudo apt install nmap`)
- Dependencias Python:

```bash
pip install -r requirements.txt
````

---

## 🛠 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/rafaelmperez/nmap-auto-scanner.git
cd nmap-auto-scanner
```

2. Crea y activa un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Configura tu archivo `config.yaml` (ver ejemplo más abajo).

---

## 🚀 Ejecución

Ejecuta el escáner de forma manual:

```bash
python scanner.py
```

Esto realizará:

1. Lectura del archivo `config.yaml`
2. Escaneo de todos los objetivos listados
3. Generación de:

   * `results.json`
   * `results.csv`
4. Comparación con el escaneo anterior (si existe)
5. Creación de `diff_report.txt` (diferencias detectadas)

---

## 🗂️ Estructura del proyecto

```bash
nmap-auto-scanner/
├── scanner.py
├── config.yaml
├── requirements.txt
├── logs/
│   └── scanner.log
├── reports/
│   └── 2025-11-09_00-56/
│       ├── results.json
│       ├── results.csv
│       └── diff_report.txt
├── utils/
│   ├── config_loader.py
│   ├── nmap_runner.py
│   ├── report_manager.py
│   └── result_saver.py
```

---

## ⚙️ Ejemplo de `config.yaml`

```yaml
targets:
  - 192.168.1.1
  - scanme.nmap.org

nmap_options: "-sS -sV -T4"
output_dir: "./reports"

notifications:
  email:
    enabled: false
  telegram:
    enabled: false
```

---

## ⏰ Ejecución automática con `cron`

Para ejecutar el escaneo cada lunes a las 2:00 AM:

```bash
crontab -e
```

Agrega:

```bash
0 2 * * 1 /ruta/a/venv/bin/python /ruta/a/nmap-auto-scanner/scanner.py >> /ruta/a/nmap-auto-scanner/logs/cron.log 2>&1
```

> Asegúrate de usar rutas absolutas y tener permisos adecuados.

---

## 📊 Comparación entre escaneos

Cuando el script detecta escaneos anteriores, genera un archivo `diff_report.txt` con diferencias entre el último y el penúltimo resultado:

```
📍 45.33.32.156
🆕 Puerto abierto: 9929/tcp - Servicio: nping-echo
❌ Puerto cerrado: 8080/tcp - Servicio: http-proxy
🔁 Cambio: puerto 22/tcp cambió de OpenSSH 6.6 a OpenSSH 9.0
```

Esto te permite detectar nuevas exposiciones o cambios sospechosos automáticamente.

---

## 🧪 Ejemplo de salida

```plaintext
[✓] Escaneo completado. Resultados guardados en: ./reports/2025-11-09_00-56
[~] Comparación con escaneo anterior completada. Reporte: ./reports/2025-11-09_00-56/diff_report.txt
```
## 📸 Ejemplo de salida (JSON + diff_report)

A continuación un ejemplo real de salida: a la izquierda se muestra la salida JSON parseada con los puertos y servicios detectados; a la derecha, el `diff_report.txt` indicando que **no se detectaron diferencias** entre escaneos.

<figure>
  <img src="./images/report_snapshot.png" alt="Salida JSON y diff_report" style="max-width:100%;height:auto;">
  <figcaption>Figura — Ejemplo de `results.json` (izq.) y `diff_report.txt` (der.). <strong>Nota:</strong> datos sensibles redactados.</figcaption>
</figure>

---

## 🧩 Mejoras futuras

* ✅ Notificaciones por correo o Telegram cuando haya cambios
* ✅ Filtro de puertos críticos (SSH, RDP, HTTP, etc.)
* ❌ Exportación HTML del informe de diferencias
* ❌ Dashboard web básico con resultados

---

## 👨‍💻 Autor

**Rafael M. Pérez — [codebyRalph](https://rafaelmperez.github.io)**
Administrador de sistemas y futuro analista de ciberseguridad
🌐 [www.rafaelmperez.com](https://rafaelmperez.com)
✉️ [rmp.blueteam@proton.me](mailto:rmp.blueteam@proton.me)
🔗 [LinkedIn](https://www.linkedin.com/in/rafaelmperez)

---

## 🪪 Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Consulta el archivo [`LICENSE`](LICENSE) para más información.



