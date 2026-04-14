---
description: "Start Astro dev server with livereload on port 12345. Kills any existing process on the port first."
user_invocable: true
---

Run these steps sequentially:

1. Kill any existing process on port 12345 and nearby ports (Astro auto-increments when blocked):
```bash
for port in 12345 12346 12347; do PID=$(lsof -ti:$port 2>/dev/null); if [ -n "$PID" ]; then kill -9 $PID 2>/dev/null; echo "Killed PID(s) on port $port: $PID"; fi; done; sleep 1; lsof -ti:12345 2>/dev/null && echo "WARNING: port 12345 still occupied" || echo "Port 12345 is free"
```

2. Start the Astro dev server in the background:
```bash
pnpm run dev
```
Run this command in the background.

3. Wait for the server to be ready, then verify it responds:
```bash
for i in $(seq 1 15); do curl -s -o /dev/null -w "%{http_code}" http://localhost:12345/ 2>/dev/null && break; sleep 1; done
curl -s -o /dev/null -w "Astro dev server verified: HTTP %{http_code}\n" http://localhost:12345/
```
