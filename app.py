# app.py
import os
import threading
import time
import webbrowser
import psutil
from flask import Flask, render_template, jsonify, request

# ────────────────────────────────────────────────────────────────
# Flask setup
# ────────────────────────────────────────────────────────────────
app = Flask(__name__, template_folder='templates', static_folder='static')

# Disk-I/O tracking
_last_disk = psutil.disk_io_counters()
_last_time = time.time()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/stats')
def stats():
    """Return current CPU / RAM / disk-I/O / network stats."""
    global _last_disk, _last_time

    cpu_usage = psutil.cpu_percent(interval=0.5)
    ram_usage = psutil.virtual_memory().percent

    current_disk = psutil.disk_io_counters()
    now = time.time()
    duration = now - _last_time if now != _last_time else 1.0

    read_bps  = (current_disk.read_bytes  - _last_disk.read_bytes)  / duration
    write_bps = (current_disk.write_bytes - _last_disk.write_bytes) / duration
    disk_mb_s = (read_bps + write_bps) / (1024 * 1024)

    _last_disk, _last_time = current_disk, now

    net_io = psutil.net_io_counters()
    sent_mb     = net_io.bytes_sent     / (1024 * 1024)
    received_mb = net_io.bytes_recv     / (1024 * 1024)

    return jsonify(
        cpu=round(cpu_usage, 2),
        ram=round(ram_usage, 2),
        disk=round(disk_mb_s, 2),
        network_sent=round(sent_mb, 2),
        network_received=round(received_mb, 2)
    )


# ────────────────────────────────────────────────────────────────
# Shutdown route
# ────────────────────────────────────────────────────────────────
def _shutdown_server():
    """Tell Werkzeug to shut down, then force-exit the process."""
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    # Give the server half a second to shut down cleanly, then kill process
    threading.Timer(0.5, lambda: os._exit(0)).start()
    return "Shutting down…", 200

@app.route('/api/stop', methods=['POST'])
def stop():
    return _shutdown_server()


# ────────────────────────────────────────────────────────────────
# Utility: kill old copies of this exe so we can rebuild
# ────────────────────────────────────────────────────────────────
def kill_other_instances(exe_name: str):
    """End any *other* process whose name matches exe_name."""
    me = os.getpid()
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['pid'] == me:
            continue                      # do NOT kill ourselves
        if proc.info['name'] and proc.info['name'].lower() == exe_name.lower():
            try:
                proc.kill()
                print(f"Killed stale {exe_name} (PID {proc.pid})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass


# ────────────────────────────────────────────────────────────────
# Main entry
# ────────────────────────────────────────────────────────────────
def run_flask():
    # use_reloader=False prevents the double-launch issue under PyInstaller
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # 1. Kill any previous copy (helpful when rebuilding with PyInstaller)
    kill_other_instances('app.exe')

    # 2. Start Flask in a daemon thread
    server_thread = threading.Thread(target=run_flask, daemon=True)
    server_thread.start()

    # 3. Wait a moment and open the browser
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5000')

    # 4. Keep the main thread alive while Flask runs
    server_thread.join()
