import json
from http.server import BaseHTTPRequestHandler, HTTPServer


def file_loader(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/documents":

            documents = file_loader("documents.json")

            response = json.dumps(documents).encode("utf-8")
            # py object to json

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(response)

        elif self.path == "/questions":

            questions = file_loader("questions.json")

            response = json.dumps(questions).encode("utf-8")
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
            previous_data = file_loader("questions.json")
            previous_data[str(len(previous_data))] = data
            print(data)
            with open("questions.json", "w") as f:
                json.dump(previous_data, f)

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                b'{"message": "Document created"}'
            )

        elif self.path == "/questions":

            content_length = int(self.headers["Content-Length"])

            body = self.rfile.read(content_length)

            data = json.loads(body)
            # json to py object
            previous_data = file_loader("questions.json")
            previous_data[str(len(previous_data))] = data
            print(data)
            with open("questions.json", "w") as f:
                json.dump(previous_data, f)

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                b'{"message": "question created"}'
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