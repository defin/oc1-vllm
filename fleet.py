#!/usr/bin/env python3
"""Fleet management CLI for Salad vLLM container groups.

Usage:
  fleet.py status
  fleet.py start <model>
  fleet.py stop <model>
"""

import configparser
import json
import os
import subprocess
import sys
from pathlib import Path

INI = Path(os.environ.get("SALAD_INI", Path.home() / ".config/salad/salad.ini"))

STATUS_COLORS = {
    "running":   "\033[32m",
    "deploying": "\033[33m",
    "stopped":   "\033[90m",
    "failed":    "\033[31m",
}
RESET = "\033[0m"


def load_config():
    if not INI.exists():
        sys.exit(f"Config not found: {INI}\nSet SALAD_INI=/path/to/salad.ini or create {INI}")
    cfg = configparser.ConfigParser()
    cfg.read(INI)
    return cfg


def api(cfg, method, path, body=None):
    key = cfg["salad"]["api_key"]
    org = cfg["salad"]["organization"]
    proj = cfg["salad"]["project"]
    url = f"https://api.salad.com/api/public/organizations/{org}/projects/{proj}/containers/{path}"
    cmd = ["curl", "-sf", "-X", method, "-H", f"Salad-Api-Key: {key}"]
    if body:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(body)]
    cmd.append(url)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"curl exit {result.returncode}")
    return json.loads(result.stdout) if result.stdout.strip() else {}


def models(cfg):
    return [(s, dict(cfg[s])) for s in cfg.sections() if s != "salad"]


def cmd_status(cfg):
    print(f"{'MODEL':<25} {'STATUS':<12} {'RUNNING':<8} API URL")
    print("-" * 90)
    for name, opts in models(cfg):
        group = opts["container_group"]
        base_url = opts["health_url"].removesuffix("/models")
        try:
            data = api(cfg, "GET", group)
            state = data["current_state"]
            status = state["status"]
            running = state["instance_status_counts"]["running_count"]
            color = STATUS_COLORS.get(status, "")
            print(f"{name:<25} {color}{status:<12}{RESET} {running:<8} {base_url}")
        except Exception as e:
            print(f"{name:<25} {'error':<12} {'?':<8} {base_url}  ({e})")


def cmd_start(cfg, name):
    if name not in cfg:
        sys.exit(f"Unknown model: {name}")
    group = cfg[name]["container_group"]
    api(cfg, "POST", f"{group}/start")
    print(f"Started {name}")


def cmd_stop(cfg, name):
    if name not in cfg:
        sys.exit(f"Unknown model: {name}")
    group = cfg[name]["container_group"]
    api(cfg, "POST", f"{group}/stop")
    print(f"Stopped {name}")


def main():
    cfg = load_config()
    args = sys.argv[1:]

    if not args or args[0] == "status":
        cmd_status(cfg)
    elif args[0] == "start" and len(args) == 2:
        cmd_start(cfg, args[1])
    elif args[0] == "stop" and len(args) == 2:
        cmd_stop(cfg, args[1])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
