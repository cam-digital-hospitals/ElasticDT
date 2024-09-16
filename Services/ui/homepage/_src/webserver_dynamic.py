import cherrypy
import subprocess
import threading
import time

class TraefikEndpoints:
    discovered_routes = []

    def __init__(self):
        # Start the background task to update the HTTP routes every 5 minutes
        threading.Thread(target=self.update_routes_periodically, daemon=True).start()

    @cherrypy.expose
    def index(self):
        # Generate HTML with discovered HTTP routes
        html_content = """
        <html>
            <head>
                <title>EDT_Demo</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        margin: 0;
                        padding: 0;
                    }
                    .container {
                        display: flex;
                        flex-wrap: wrap;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        padding: 20px;
                    }
                    .card {
                        background-color: #ffffff;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        margin: 20px;
                        padding: 20px;
                        width: 300px;
                        text-align: center;
                        transition: transform 0.3s;
                    }
                    .card:hover {
                        transform: translateY(-5px);
                    }
                    .card h3 {
                        margin-bottom: 20px;
                        font-size: 1.5em;
                        color: #333;
                    }
                    .card a {
                        display: inline-block;
                        background-color: #4caf50;
                        color: white;
                        padding: 10px 20px;
                        text-decoration: none;
                        border-radius: 5px;
                        transition: background-color 0.3s;
                    }
                    .card a:hover {
                        background-color: #45a049;
                    }
                    h2 {
                        text-align: center;
                        color: #333;
                    }
                </style>
            </head>
            <body>
            <h1>Elastic Digital Twin (Demo)</h1>
                <div class="container">
        """

        # Dynamically add cards based on discovered routes
        for name, path in self.discovered_routes:
            color = self.get_card_color(name)
            html_content += f"""
                    <div class="card" style="background-color:{color}">
                        <h3>{name}</h3>
                        <a href="http://{path}" target="_blank">Go to {name}</a>
                    </div>
            """

        html_content += """
                </div>
            </body>
        </html>
        """
        return html_content

    def get_card_color(self, name):
        """Assign card color based on prefix of the name."""
        if name.startswith('di'):
            return 'blue'
        elif name.startswith('ds'):
            return 'green'
        elif name.startswith('ui'):
            return 'red'
        else:
            return '#ffffff'  # Default white background

    def update_routes_periodically(self):
        """Background task to update the discovered routes every 5 minutes."""
        while True:
            self.discovered_routes = self.get_httproutes('elasticdt')
            print(f"Discovered routes: {self.discovered_routes}")
            time.sleep(300)  # Sleep for 5 minutes (300 seconds)

    def get_httproutes(self, namespace):
        """Execute kubectl to get HTTP routes and return name and path."""
        try:
            # Execute the kubectl command to get httproutes
            command = f"kubectl get httproutes -n {namespace} --no-headers"
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Check if there is an error
            if result.stderr:
                print(f"Error: {result.stderr}")
                return []

            # Process the output
            httproutes = []
            for line in result.stdout.strip().split('\n'):
                columns = line.split()
                if len(columns) >= 2:
                    name = columns[0].rsplit('-', 1)[0]  # Remove the "-httproute" suffix
                    path = columns[1].strip('[]"')  # Clean up the path (remove brackets and quotes)
                    httproutes.append((name, path))

            return httproutes

        except Exception as e:
            print(f"An error occurred: {e}")
            return []

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8081})
    cherrypy.quickstart(TraefikEndpoints())
