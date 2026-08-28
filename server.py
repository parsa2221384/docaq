import json
from http.server import BaseHTTPRequestHandler, HTTPServer


def load_documents():
    with open("documents.json", "r", encoding="utf-8") as file:
        return json.load(file)


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/documents":

            documents = load_documents()

            response = json.dumps(documents).encode("utf-8")
            # py object to json

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(response)

        elif self.path == "/questions":

            documents = load_documents()

            response = json.dumps(documents).encode("utf-8")
            # py object to json

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(response)


        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                b'{"error": "Endpoint not found"}'
            )

    def do_POST(self):

        if self.path == "/documents":

            content_length = int(self.headers["Content-Length"])

            body = self.rfile.read(content_length)

            data = json.loads(body)
            # json to py object

            print(data)

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                b'{"message": "Document created"}'
            )

        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                b'{"error": "Endpoint not found"}'
            )




server = HTTPServer(("localhost", 8000), RequestHandler)

print("Server is running on http://localhost:8000")

server.serve_forever()