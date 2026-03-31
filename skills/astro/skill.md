---
description: "Start Astro dev server with livereload on port 12345. Kills any existing process on the port first."
user_invocable: true
---

```bash
# Kill existing process on port 12345
PID=$(lsof -ti:12345 2>/dev/null)
if [ -n "$PID" ]; then
  kill "$PID" 2>/dev/null
  sleep 1
  echo "Killed existing process on port 12345 (PID $PID)"
fi

# Start Astro dev server
pnpm run dev
```
