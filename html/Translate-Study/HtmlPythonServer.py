import http.server
import socketserver

# Define the port you want to use
PORT = 3456

# Set the directory where your HTML files are located
DIRECTORY = './'

# Create a server handler
Handler = http.server.SimpleHTTPRequestHandler

# Start the server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Server running at http://localhost:{}/".format(PORT))
    # Serve files indefinitely until interrupted
    httpd.serve_forever()
