from escpos.printer import Win32Raw
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import traceback

logging.basicConfig(level=logging.INFO)

class PrintHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handle preflight CORS
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            # Log received data for debugging
            logging.info("Received POST data: %s", post_data.decode("utf-8"))

            data = json.loads(post_data)
            raw_text = data.get("print_text", "")
            printer_name = data.get("printer_name", "")  # Dynamic name

            # Connect to printer
            printer = Win32Raw(printer_name)
            printer.set(bold=False, underline=0, width=1, height=1)
            printer.set(align='center')
            for raw_line in raw_text.splitlines():
                line = raw_line.strip()
                width = 1
                height = 1
                bold = False
                use_small = False
                printer.set(font='a')

                if "**LEFT**" in line:
                    printer.set(align='left')
                    line = line.replace("**LEFT**", "")
                if "**CENTER**" in line:
                    printer.set(align='center')
                    line = line.replace("**CENTER**", "")

                if "**QR**" in line:
                    qr_data = line.replace("**QR**", "").strip()
                    if qr_data:
                        printer.qr(qr_data, size=6, model=2)
                    continue

                if "**H1**" in line:
                    width, height, bold = 2, 2, True
                    line = line.replace("**H1**", "")
                elif "**H2**" in line:
                    width, height, bold = 2, 1, True
                    line = line.replace("**H2**", "")
                elif "**H3**" in line:
                    width, height, bold = 1, 1, True
                    line = line.replace("**H3**", "")
                elif "**H4**" in line:
                    width, height, bold = 1, 1, False
                    line = line.replace("**H4**", "")
                elif "**SMALL**" in line:
                    use_small = True
                    line = line.replace("**SMALL**", "")

                # ESC/POS text formatting
                if use_small:
                    printer.set(font='b')
                elif width == 2 and height == 2:
                    printer._raw(b'\x1d!\x11')
                elif width == 2 and height == 1:
                    printer._raw(b'\x1d!\x10')
                elif width == 1 and height == 2:
                    printer._raw(b'\x1d!\x01')
                else:
                    printer._raw(b'\x1d!\x00')

                printer.set(bold=bold, underline=0)
                printer.text(line + "\n")



            printer.set(bold=False, underline=0, width=1, height=1)
            printer.cut()
            printer.close()

            # Response
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")  # CORS
            self.end_headers()
            self.wfile.write(b"Printed successfully")

        except Exception as e:
            logging.exception("Error during printing")
            tb = traceback.format_exc()
            error_message = f"Print failed: {e}\n{tb}"
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")  # CORS
            self.end_headers()
            self.wfile.write(error_message.encode("utf-8"))

import socket

def get_local_ip():
    """Get the LAN IP of the machine"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This IP doesn't need to be reachable
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def run(server_class=ThreadingHTTPServer, handler_class=PrintHandler, port=9999):
    server_address = ('0.0.0.0', port)  # bind to all interfaces
    httpd = server_class(server_address, handler_class)
    lan_ip = get_local_ip()
    logging.info(f"Print agent running at http://{lan_ip}:{port}")
    print(f"Print agent running at http://{lan_ip}:{port}")
    httpd.serve_forever()



if __name__ == "__main__":
    run()

# pyinstaller agent.spec