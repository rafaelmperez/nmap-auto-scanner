# utils/report_manager.py

import json
import os
import logging

def load_scan_results(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"[!] No se pudo cargar {path}: {e}")
        return {}

def compare_scans(old, new):
    changes = []

    old_hosts = set(old.keys())
    new_hosts = set(new.keys())

    added_hosts = new_hosts - old_hosts
    removed_hosts = old_hosts - new_hosts

    for host in added_hosts:
        changes.append(f"[+] Nuevo host detectado: {host}")

    for host in removed_hosts:
        changes.append(f"[-] Host eliminado: {host}")

    for host in old_hosts & new_hosts:
        old_ports = old[host]["protocols"]
        new_ports = new[host]["protocols"]

        for proto in new_ports:
            old_proto_ports = {p["port"]: p for p in old_ports.get(proto, [])}
            new_proto_ports = {p["port"]: p for p in new_ports.get(proto, [])}

            added_ports = set(new_proto_ports.keys()) - set(old_proto_ports.keys())
            removed_ports = set(old_proto_ports.keys()) - set(new_proto_ports.keys())

            for port in added_ports:
                changes.append(f"[+] Nuevo puerto abierto en {host}/{proto}: {port}")

            for port in removed_ports:
                changes.append(f"[-] Puerto cerrado en {host}/{proto}: {port}")

            for port in set(old_proto_ports) & set(new_proto_ports):
                old_data = old_proto_ports[port]
                new_data = new_proto_ports[port]

                if old_data != new_data:
                    changes.append(f"[~] Cambio en {host}/{proto}:{port}")
                    changes.append(f"     Antes: {old_data}")
                    changes.append(f"     Ahora: {new_data}")

    return changes

def save_diff_report(changes, output_path):
    with open(output_path, "w") as f:
        if not changes:
            f.write("No se detectaron diferencias entre escaneos.\n")
        else:
            for line in changes:
                f.write(line + "\n")
