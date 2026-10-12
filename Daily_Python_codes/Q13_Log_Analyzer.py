logs = [
    "2026-10-12T08:01:00Z INFO nvme0 Controller ready",
    "2026-10-12T08:02:00Z ERROR nvme0 I/O timeout detected",
    "2026-10-12T08:03:00Z WARNING nvme1 Temperature threshold exceeded",
    "2026-10-12T08:04:00Z ERROR nvme0 Namespace reset failed",
    "2026-10-12T08:05:00Z INFO kernel Device registered",
    "2026-10-12T08:06:00Z ERROR nvme1 Controller initialization failed"
]

result = {}

for i in logs:
    parts = i.split(maxsplit=3)

    if len(parts) < 4:
        continue
    timestamp, level, component, message = parts

    if level not in ['WARNING', 'ERROR']:
        continue

    if component not in result:
        result[component] = {'ERROR':0, 'WARNING':0}

    result[component][level] += 1

print(result)




