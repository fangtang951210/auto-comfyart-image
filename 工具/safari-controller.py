#!/usr/bin/env python3
"""Safari MCP 常驻控制器:单一会话。命令经 FIFO 写入,结果追加到 OUT 文件。"""
import subprocess, json, os, threading
FIFO = "/tmp/safari-ctl.fifo"
OUT = "/tmp/safari-ctl-out.jsonl"
if not os.path.exists(FIFO):
    os.mkfifo(FIFO)
open(OUT, "w").close()
p = subprocess.Popen(["/usr/bin/safaridriver", "--mcp"], stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
def pump():
    for line in p.stdout:
        s = line.strip()
        if s.startswith("{"):
            try:
                j = json.loads(s)
                if "id" in j:
                    with open(OUT, "a") as f:
                        f.write(json.dumps(j, ensure_ascii=False) + "\n")
            except Exception:
                pass
threading.Thread(target=pump, daemon=True).start()
def send(obj):
    p.stdin.write(json.dumps(obj) + "\n"); p.stdin.flush()
send({"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"ctrl","version":"1"}}})
send({"jsonrpc":"2.0","method":"notifications/initialized"})
while True:
    with open(FIFO) as f:
        for line in f:
            s = line.strip()
            if not s: continue
            try:
                cmd = json.loads(s)
            except Exception:
                continue
            send({"jsonrpc":"2.0","id":cmd["id"],"method":"tools/call",
                  "params":{"name":cmd["name"],"arguments":cmd.get("args",{})}})
