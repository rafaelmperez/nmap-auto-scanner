🔍 nmap-auto-scanner

Automatiza escaneos de red utilizando Nmap, guarda los resultados en JSON y CSV, y compara cambios entre escaneos sucesivos.

---

## 🎯 Objetivo

Este proyecto fue desarrollado con un enfoque profesional para practicar y documentar habilidades en:

- Automatización defensiva
- Uso avanzado de Nmap
- Gestión de configuración con YAML
- Registro de resultados y comparación entre escaneos

Es ideal como proyecto de portafolio para profesionales de ciberseguridad y administración de sistemas.

---

## ⚙️ Tecnologías utilizadas

- [Python 3.10+](https://www.python.org/)
- [Nmap](https://nmap.org/)
- [`python-nmap`](https://pypi.org/project/python-nmap/)
- YAML para configuración
- `cron` para ejecución periódica automatizada
- `logging` para trazabilidad
- Estructura modular en carpetas `utils/`

---

## 📦 Requisitos

- Linux con acceso a terminal
- Python 3.10 o superior
- Nmap instalado en el sistema (`sudo apt install nmap`)
- Dependencias Python:

```bash
pip install -r requirements.txt
````

---

## 🗂️ Estructura del proyecto

```
nmap-auto-scanner/
├── scanner.py
├── config.yaml
├── logs/
│   └── scanner.log
├── reports/
│   └── YYYY-MM-DD_HH-MM/
│       ├── results.json
│       ├── results.csv
│       └── diff_report.txt
├── utils/
│   ├── config_loader.py
│   ├── nmap_runner.py
│   ├── report_manager.py
│   └── result_saver.py
└── requirements.txt
```

---

## 🧪 Ejecución manual

```bash
python scanner.py
```

El script:

1. Carga los objetivos desde `config.yaml`
2. Lanza escaneos Nmap
3. Guarda resultados en `reports/YYYY-MM-DD_HH-MM/`
4. Compara con el escaneo anterior si existe
5. Genera un archivo `diff_report.txt` con los cambios detectados

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

Para programar escaneos semanales:

```bash
crontab -e
```

Y añade:

```bash
0 2 * * 1 /ruta/a/venv/bin/python /ruta/a/nmap-auto-scanner/scanner.py >> /ruta/a/nmap-auto-scanner/logs/cron.log 2>&1
```

Esto lo ejecuta **todos los lunes a las 2:00 AM**.

---

## 📊 Comparación entre escaneos

El script detecta automáticamente el escaneo anterior y genera:

```
diff_report.txt
```

Con los siguientes posibles cambios:

* 🆕 Nuevos puertos abiertos
* ❌ Puertos cerrados
* 🔁 Cambios en servicios o versiones

---

## 🧑‍💻 Autor

**Rafael M. Pérez — [codebyRalph](https://rafaelmperez.github.io)**
Administrador de sistemas y futuro analista de ciberseguridad.
🌐 [www.rafaelmperez.com](https://rafaelmperez.com)
✉️ [rmp.blueteam@proton.me](mailto:rmp.blueteam@proton.me)
