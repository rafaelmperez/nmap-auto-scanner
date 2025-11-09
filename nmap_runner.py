# utils/nmap_runner.py

import nmap
import logging

def run_nmap_scan(target, options):
    logging.info(f"[+] Escaneando objetivo: {target} con opciones: {options}")

    try:
        scanner = nmap.PortScanner()
        scanner.scan(hosts=target, arguments=options)
    except nmap.PortScannerError as e:
        logging.error(f"[!] Error al ejecutar Nmap: {e}")
        return {}
    except Exception as e:
        logging.error(f"[!] Error inesperado al escanear {target}: {e}")
        return {}

    result = {}

    for host in scanner.all_hosts():
        result[host] = {
            "status": scanner[host].state(),
            "protocols": {}
        }

        for proto in scanner[host].all_protocols():
            ports = scanner[host][proto].keys()
            result[host]["protocols"][proto] = []

            for port in sorted(ports):
                port_data = scanner[host][proto][port]
                result[host]["protocols"][proto].append({
                    "port": port,
                    "state": port_data.get("state", ""),
                    "name": port_data.get("name", ""),
                    "product": port_data.get("product", ""),
                    "version": port_data.get("version", ""),
                    "extrainfo": port_data.get("extrainfo", "")
                })

    logging.info(f"[✓] Escaneo completado para {target}")
    return result
