#!/usr/bin/env python3
"""Generate and PATCH the Salad container command with the startup script embedded."""

import base64
import json
import subprocess
import sys
from pathlib import Path

STARTUP   = Path("/gitea/dev/oc1-image/startup.py")
API_KEY   = "salad_cloud_user_xXzG8yl4OUpBTcxQyiUDlueEQntfdPBzdYzLG5hammx2REKxr"
API_URL   = "https://api.salad.com/api/public/organizations/tempinfo/projects/default/containers/oc1"

encoded = base64.b64encode(STARTUP.read_bytes()).decode()

# The container will decode, write to /tmp/s.py, and exec it
inline = (
    f"import base64,os,sys;"
    f"open('/tmp/s.py','w').write(base64.b64decode('{encoded}').decode());"
    f"os.execv(sys.executable,[sys.executable,'/tmp/s.py'])"
)

cmd = ["python3", "-c", inline]

body = {"container": {"command": cmd}}

result = subprocess.run([
    "curl", "-sf", "-X", "PATCH",
    "-H", f"Salad-Api-Key: {API_KEY}",
    "-H", "Content-Type: application/merge-patch+json",
    "-d", json.dumps(body),
    API_URL,
], capture_output=True, text=True)

if result.returncode != 0:
    print("PATCH failed:", result.stdout or result.stderr, file=sys.stderr)
    sys.exit(1)

data = json.loads(result.stdout)
print("Command set:", json.dumps(data["container"]["command"][:2]) + " ...<encoded>]")
print("Version:", data.get("version"))
