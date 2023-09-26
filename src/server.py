from waitress import serve
import time
import webbrowser  # For launching web pages
from threading import Timer  # For waiting before launching web page
import heliodon as sun
from heliodon_app import server


def open_browser():
    """
    Open browser to localhost
    """

    webbrowser.open_new('http://127.0.0.1:8080/')


available_ports = sun.serial_ports()
port_id = range(len(available_ports))
print("Port list: ")
for n, v in zip(port_id, available_ports):
    print("{} -> {}".format(n, v))
print("Port ID: ")
id = int(input())
con = sun.connect(available_ports[id])

Timer(1, open_browser).start()  # Wait a second and then start the web page
serve(server)