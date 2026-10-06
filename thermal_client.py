# thermal_agent.py
import http.server
import socketserver
import subprocess
import urllib.parse

PORT = 9999  # local-only port

class PrintHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/print":
            query = urllib.parse.parse_qs(parsed_path.query)
            server_ip = query.get("server_ip", [""])[0]
            invoice_id = query.get("invoice_id", [""])[0]

            if server_ip and invoice_id:
                try:
                    subprocess.Popen(["python", "thermal_client.py", server_ip, invoice_id])
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Print job sent.")
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(f"Error: {e}".encode())
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing parameters.")
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(("localhost", PORT), PrintHandler) as httpd:
    print(f"Thermal agent running on port {PORT}")
    httpd.serve_forever()
