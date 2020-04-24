#!/usr/bin/env python

import threading
import SimpleHTTPServer
import SocketServer
import time


# configuracion servidor WEB:
hostName = ''         #Coge automaticamente todas las interfaces
serverPort = 6001     # Puerto por encima de 1024



class Controlador:
    """Controla la recepción de cambios y colores."""
    def __init__(self):
        """inicia el controlador"""
        self.estado = 0
        self.cambio = False
        self.ultimoColor = [0,0,0]

    def cambiarEstado(self,estado2):
        """Cambia el estado"""
        if estado2 != self.estado:
            if estado2 >= 0 and estado2 <= 10:
                self.estado=estado2
                self.cambio = True
                print ("estado es " + str(self.estado))

    def manejarString(self,datos):
        """maneja e interpreta los datos recividos por el servidor web"""
        partes=datos.split(',')
        try:
            self.cambiarEstado(int(partes[0]))

            try:
                self.ultimoColor = [int(partes[2]),int(partes[1]),int(partes[3])]
                self.cambio = True
                print ("ultimo color = "+str(self.ultimoColor))
            except:
                print ("no hay color")

        except ValueError:
            print ("eso no es un int")

class MyServer(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """Maneja las diferentes peticiones"""
    def do_GET(self):
        """maneja la petición GET"""
        print ("estodo es igual a {estado="+str(controlador.estado)+"}")
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('{"estado":'+str(controlador.estado)+'}'))
    def do_POST(self):
        """maneja la petición POST"""
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print ("se ha recibido = " + body)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(body+"\n"))
        controlador.manejarString(body)


def LeerSocket():
    """Corre el servidor web hasta que se acabe el programa"""
    global httpd
    try:
        httpd.serve_forever()
    except:
        print('\nServidor parado.')


controlador = Controlador()

httpd = SocketServer.TCPServer((hostName, serverPort), MyServer)
print("Servidor iniciado en http://%s:%s" % ('localhost', serverPort))


try:
    thread=threading.Thread(target=LeerSocket, args=()) #Transforma el servidor web en un subproceso
    thread.daemon=True
    thread.start()
except (KeyboardInterrupt, SystemExit):
    httpd.server_close()
    print('\nServidor no puedo iniciar.')

