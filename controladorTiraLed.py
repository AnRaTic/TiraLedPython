#!/usr/bin/env python

import socketTiraLed
import time
from neopixel import *
import argparse

# configuracion tira led:
LED_COUNT      = 16      # Numero de Leds.
LED_PIN        = 18      # GPIO pin conectado a la tira (el 18 usa PWM!).
#LED_PIN        = 10      # GPIO pin conectado a la tira (el 10 usa SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # Frecunecia de la señal Led en hercios (normalmente 800khz)
LED_DMA        = 10      # Canal DMA a usar para generar la señal (try 10)
LED_BRIGHTNESS = 255     # Poner a 0 para el mas oscuro y 255 para el mas brillante
LED_INVERT     = False   # True para invertir la señal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # Poner a 1 para GPIOs 13, 19, 41, 45 or 53



# Funciones que animan los leds de diferentes maneras.
def LadoALado(strip,color,wait_ms=50):
    """Hace rafagas de lado a lado del color indicado."""
    longitud=strip.numPixels()
    for i in range(longitud-1):
        strip.setPixelColor(i+1, color)
        strip.setPixelColor(i, color)
        strip.setPixelColor(i-1, Color(0, 0, 0))
        strip.show()
        time.sleep(wait_ms/1000.0)
        if socketTiraLed.controlador.cambio:
            socketTiraLed.controlador.cambio = False
            return
    for i in range(longitud-1):
        strip.setPixelColor(longitud-i, Color(0, 0, 0))
        strip.setPixelColor(longitud-1-i, color)
        strip.setPixelColor(longitud-2-i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        if socketTiraLed.controlador.cambio:
            socketTiraLed.controlador.cambio = False
            return

def Rafagas(strip,color,wait_ms=120):
    """Hace rafagas del color indicado."""
    longitud=strip.numPixels()
    for i in range(longitud/2+2):
        j=longitud/2+i+longitud%2
        k=longitud/2-1-i
        strip.setPixelColor(j-2, Color(0, 0, 0))
        strip.setPixelColor(k+2, Color(0, 0, 0))
        strip.setPixelColor(j, color)
        strip.setPixelColor(j-1, color)
        strip.setPixelColor(k, color)
        strip.setPixelColor(k+1, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        if socketTiraLed.controlador.cambio:
            socketTiraLed.controlador.cambio = False
            return 5

def Apagar():
    """Apaga la tira."""
    Fijo(strip,Color(0,0,0))

def ApagarYSalir(wait_ms=50):
    """Apaga la tira y salir."""
    longitud=strip.numPixels()
    for i in range(longitud/2+2):
        j=longitud/2+i+longitud%2
        k=longitud/2-1-i
        strip.setPixelColor(j, Color(0,0,0))
        strip.setPixelColor(j-1, Color(0,0,0))
        strip.setPixelColor(k, Color(0,0,0))
        strip.setPixelColor(k+1, Color(0,0,0))
        strip.show()
        time.sleep(wait_ms/1000.0)

def Fijo(strip,color,wait_ms=50):
    """Pone un color fijo constante."""
    longitud=strip.numPixels()
    for i in range(longitud/2+2):
        j=longitud/2+i+longitud%2
        k=longitud/2-1-i
        strip.setPixelColor(j, color)
        strip.setPixelColor(j-1, color)
        strip.setPixelColor(k, color)
        strip.setPixelColor(k+1, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        if socketTiraLed.controlador.cambio:
            socketTiraLed.controlador.cambio = False
            return
    while not socketTiraLed.controlador.cambio:
        time.sleep(wait_ms/1000.0)
    socketTiraLed.controlador.cambio = False

def RafagasRGB(strip,wait_ms=50):
    """Hace rafagas de color verde rojo y azul sucesivamente"""
    if Rafagas(strip,Color(0,255,0)) == 5:
        return
    if Rafagas(strip,Color(255,0,0)) == 5:
        return
    if Rafagas(strip,Color(0,0,255)) == 5:
        return

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Genera colores arcoiris de 0-255 posiciones."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def ArcoirisFijo(strip, wait_ms=60):
    """Todas las luces cambian pasando por todos los colores conjuntamente."""
    for j in range(256):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
        if socketTiraLed.controlador.cambio:
            socketTiraLed.controlador.cambio = False
            return

def CicloArcoiris(strip, invertido=0, wait_ms=20):
    """Las luces cambian pasando por todos los colores no simétricamente."""
    for j in range(256):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + (1-invertido)*(255-j)+ invertido*j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
        if socketTiraLed.controlador.cambio:
            socketTiraLed.controlador.cambio = False
            return


def CicloArcoirisEspejo(strip, invertido=0, wait_ms=20):
    """Las luces cambian pasando por todos los colores simétricamente."""
    longitud=strip.numPixels()
    for j in range(256):
        for i in range(longitud/2):
            l=longitud/2+i
            k=longitud/2-((longitud+1)%2)-i
            strip.setPixelColor(l, wheel((int(i * 256 / strip.numPixels()) + (1-invertido)*(255-j)+ invertido*j) & 255))
            strip.setPixelColor(k, wheel((int(i * 256 / strip.numPixels()) + (1-invertido)*(255-j)+ invertido*j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
        if socketTiraLed.controlador.cambio:
            socketTiraLed.controlador.cambio = False
            return

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            if socketTiraLed.controlador.cambio:
                socketTiraLed.controlador.cambio = False
                return
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

# Programa principal:
if __name__ == '__main__':

    # Crea el objeto de la tira de leds.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Inicializa la libreria.
    strip.begin()

    print ('Aprienta Ctrl-C para salir.')

    try:

        while True:
            estado = socketTiraLed.controlador.estado
            if estado == 0:
                Apagar()
            if estado == 1:
                CicloArcoirisEspejo(strip)
            if estado == 2:
                CicloArcoirisEspejo(strip,1)
            if estado == 3:
                RafagasRGB(strip)
            if estado == 4:
                color = socketTiraLed.controlador.ultimoColor
                Fijo(strip, Color(color[0],color[1],color[2]))
            if estado == 5:
                color = socketTiraLed.controlador.ultimoColor
                Rafagas(strip, Color(color[0],color[1],color[2]))
            if estado == 6:
                color = socketTiraLed.controlador.ultimoColor
                LadoALado(strip, Color(color[0],color[1],color[2]))
            if estado == 7:
                CicloArcoiris(strip)
            if estado == 8:
                CicloArcoiris(strip,1)
            if estado == 9:
                ArcoirisFijo(strip)
            
    except KeyboardInterrupt:
        socketTiraLed.httpd.server_close()
        ApagarYSalir()
        print('Servidor parado y tira de leds apagada.\n')
