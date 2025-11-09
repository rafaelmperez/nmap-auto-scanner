# scanner.py

import os
import sys
import json
import csv
import logging
from datetime import datetime

# Importar módulos propios
from utils.config_loader import load_config
from utils.nmap_runner import run_nmap_scan
from utils.report_manager import load_scan_results, compare_scans, save_diff_report

# ───── Configurar logging ───── #
logging.basicConfig(
    filename="logs/scanner.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def create_output_dir(base_dir):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    full_path = os.path.join(base_dir, timestamp)
    os.makedirs(full_path, exist_ok=True)
    return full_path

def save_json(data, filepath):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def save_csv(data, filepath):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Host", "Protocol", "Port", "State", "Service", "Product", "Version", "Extra Info"])

        for host, details in data.items():
            for proto, ports in details["protocols"].items():
                for port_info in ports:
                    writer.writerow([
                        host,
                        proto,
                        port_info["port"],
                        port_info["state"],
                        port_info["name"],
                        port_info["product"],
                        port_info["version"],
                        port_info["extrainfo"],
                    ])

def main():
    try:
        config = load_config("config.yaml")
    except Exception as e:
        print(f"[!] Error al cargar configuración: {e}")
        sys.exit(1)

    output_dir = create_output_dir(config["output_dir"])
    all_results = {}

    for target in config["targets"]:
        result = run_nmap_scan(target, config["nmap_options"])
        all_results.update(result)

    # Guardar resultados
    save_json(all_results, os.path.join(output_dir, "results.json"))
    save_csv(all_results, os.path.join(output_dir, "results.csv"))

    print(f"\n[✓] Escaneo completado. Resultados guardados en: {output_dir}\n")
    logging.info(f"[✓] Todos los resultados guardados en {output_dir}")

    # ─── Comparar con escaneo anterior ─── #
    try:
        all_report_folders = sorted(os.listdir(config["output_dir"]))
        if len(all_report_folders) >= 2:
            prev_folder = all_report_folders[-2]
            prev_results_path = os.path.join(config["output_dir"], prev_folder, "results.json")
            current_results_path = os.path.join(output_dir, "results.json")

            old_data = load_scan_results(prev_results_path)
            new_data = load_scan_results(current_results_path)

            changes = compare_scans(old_data, new_data)
            diff_path = os.path.join(output_dir, "diff_report.txt")
            save_diff_report(changes, diff_path)

            print(f"[~] Comparación con escaneo anterior completada. Reporte: {diff_path}")
        else:
            print("[~] No hay escaneos anteriores para comparar.")
    except Exception as e:
        print(f"[!] Error comparando escaneos: {e}")

if __name__ == "__main__":
    main()

