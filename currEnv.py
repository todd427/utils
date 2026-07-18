import platform
import psutil
import torch
import subprocess
import sys

def run_cmd(cmd):
    """Helper to safely run shell commands and return stripped output."""
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except Exception:
        return None

def main():
    show_all = "--all" in sys.argv

    print("System:", platform.platform())
    print("Python:", platform.python_version())
    print("CPU cores:", psutil.cpu_count(logical=True))
    print("RAM (GB):", round(psutil.virtual_memory().total / 1e9, 2))

    # CPU name
    cpu_name = None
    if platform.system() == "Linux":
        cpu_info = run_cmd("lscpu | grep 'Model name'")
        if cpu_info:
            cpu_name = cpu_info.split(":")[1].strip()
    elif platform.system() == "Windows":
        lines = run_cmd("wmic cpu get Name")
        if lines:
            cpu_name = lines.splitlines()[1].strip()

    print("CPU:", cpu_name or "(unavailable)")

    # Motherboard info (sudo-only)
    if show_all and platform.system() == "Linux":
        board_info = run_cmd("sudo dmidecode -t baseboard | grep 'Product Name'")
        if board_info and ":" in board_info:
            print("Motherboard:", board_info.split(":")[1].strip())
        else:
            print("Motherboard info: (unavailable or requires sudo)")
    else:
        print("Motherboard info: (run with --all for detailed info)")

    # Drive info
    if show_all and platform.system() == "Linux":
        drives = run_cmd("lsblk -o NAME,SIZE,MODEL | grep -E 'sd|nvme'")
        print("\nDrives:\n", drives or "(no drives found)")
    else:
        print("Drive info: (run with --all for detailed info)")

    # GPU info
    print("CUDA available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            vram_gb = round(props.total_memory / 1e9, 2)
            label = "GPU:" if torch.cuda.device_count() == 1 else f"GPU {i}:"
            print(f"{label} {props.name} ({vram_gb} GB)")

if __name__ == "__main__":
    main()

