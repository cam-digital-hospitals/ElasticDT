import cherrypy

class TraefikEndpoints:
    @cherrypy.expose
    def index(self):
        html_content = """
        <html>
            <head><title>Traefik Endpoints</title></head>
            <body>
                <h2>Available Endpoints</h2>
                <ul>
                    <li><a href="http://grafana.localhost/grafana" target="_blank">Grafana</a></li>
                    <li><a href="http://influxdb.localhost" target="_blank">InfluxDB</a></li>
                    <li><a href="http://telegraf.localhost" target="_blank">Telegraf</a></li>
                </ul>
            </body>
        </html>
        """
        return html_content

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8081})
    cherrypy.quickstart(TraefikEndpoints())
