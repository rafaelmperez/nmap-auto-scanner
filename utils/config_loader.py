# utils/config_loader.py

import yaml
import os

def load_config(config_path="config.yaml"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {config_path}")

    with open(config_path, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error al parsear el archivo YAML: {e}")

    # Validaciones básicas
    if "targets" not in config or not config["targets"]:
        raise ValueError("Debes definir al menos un objetivo en 'targets'")

    if "nmap_options" not in config:
        config["nmap_options"] = "-sS -sV -T4"

    if "output_dir" not in config:
        config["output_dir"] = "./reports"

    # Configurar alertas por defecto si no existen
    config.setdefault("notifications", {})
    config["notifications"].setdefault("email", {"enabled": False})
    config["notifications"].setdefault("telegram", {"enabled": False})

    return config
