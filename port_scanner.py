import socket
import time

def scan_port(host, port, timeout=1):
    """Return True if the port is open, otherwise False."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            return result == 0
    except socket.gaierror:
        raise ValueError("Invalid or unreachable host.")
    except Exception:
        return False

def get_service_name(port):
    """Try to return a known service name for the port."""
    try:
        return socket.getservbyport(port)
    except:
        return "unknown"

def validate_ports(start_port, end_port):
    if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
        raise ValueError("Ports must be between 1 and 65535.")
    if start_port > end_port:
        raise ValueError("Start port must be less than or equal to end port.")

def main():
    print("Authorized targets only: 127.0.0.1 or scanme.nmap.org")
    host = input("Enter target host: ").strip()
    allowed_hosts = ["127.0.0.1", "localhost", "scanme.nmap.org"]

    if host not in allowed_hosts:
        print("[ERROR] Unauthorized target. Use only localhost/127.0.0.1 or scanme.nmap.org.")
        return

    try:
        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))
        validate_ports(start_port, end_port)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return

    try:
        resolved_host = socket.gethostbyname(host)
        print(f"\nScanning {host} ({resolved_host}) from port {start_port} to {end_port}...\n")

        for port in range(start_port, end_port + 1):
            is_open = scan_port(resolved_host, port)
            service = get_service_name(port) if is_open else ""
            status = "OPEN" if is_open else "CLOSED"
            if is_open:
                print(f"Port {port}: {status} ({service})")
            else:
                print(f"Port {port}: {status}")
            time.sleep(0.05)

        print("\nScan complete.")

    except ValueError as e:
        print(f"[ERROR] {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected issue: {e}")

if __name__ == "__main__":
    main()
