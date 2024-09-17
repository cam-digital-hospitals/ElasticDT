import cherrypy

class TraefikEndpoints:
    @cherrypy.expose
    def index(self):
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
                    <div class="card">
                        <h3>Grafana</h3>
                        <a href="http://grafana.localhost/grafana" target="_blank">Go to Grafana</a>
                    </div>
                    <div class="card">
                        <h3>InfluxDB</h3>
                        <a href="http://influxdb.localhost" target="_blank">Go to InfluxDB</a>
                    </div>
                    <div class="card">
                        <h3>Inventory Management</h3>
                        <a href="http://inventory.localhost" target="_blank">Go to Inventory Management</a>
                    </div>
                </div>
            </body>
        </html>
        """
        return html_content

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8081})
    cherrypy.quickstart(TraefikEndpoints())
