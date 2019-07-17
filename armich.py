import cv2
import numpy as np
import pandas as pd
from math import sqrt,atan2,pi,asin,sin,cos,acos
class DibujarBrazo:
    def __init__(self,tonos,fondo,lb):
        self.tonos = tonos
        self.fondo = fondo
        self.hsv = cv2.cvtColor(self.fondo,cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(self.hsv, tonos[0], tonos[1])
        self.lb = lb
        self.rojo = (0,0,255)
        self.verde = (0,255,0)
        self.azul = (255,0,0)
        self.amarillo= (0,255,255)
        self.negro= (0,0,0)
        self.rad2deg = 180/pi
        self.deg2grad = pi/180

        self.interes=(0,0)

        self.h, self.w = self.fondo.shape[:2]
        self.h = int(self.h / 2)
        self.w = int(self.w / 2)
        self.h0, self.w0 = 0, 0
        self.origen = (self.w0, self.h0)
        self.origenReal = (self.w, self.h)

    def getOrigenReal(self):
        return self.origenReal

    def getGray(self):
        return cv2.cvtColor(self.fondo,cv2.COLOR_BGR2GRAY)

    def crearMarco(self):
        cv2.drawMarker(self.fondo, self.origenReal, self.rojo, markerType=2)
        cv2.line(self.fondo, (0, self.h), (2 * self.w, self.h), self.negro, 1, cv2.LINE_AA)
        cv2.line(self.fondo, (self.w, 0), (self.w, 2 * self.h), self.negro, 1, cv2.LINE_AA)
        cv2.circle(self.fondo, self.origenReal, int(0.9 * 2 * self.lb), self.rojo, 1, cv2.LINE_AA)
        cv2.circle(self.fondo, self.origenReal, int(0.1 * 2 * self.lb), self.rojo, 1, cv2.LINE_AA)
        return self.fondo

    def convertirReal(self,p1):
        xr = p1[0] + self.w
        yr = self.h - p1[1]
        return xr, yr

    def convertir(self,p1):
        xf = p1[0] - self.w
        yf = self.h - p1[1]
        return xf, yf

    def dibujarBrazo(self,brazoA, brazoB, color):
        cv2.line(self.fondo, self.origenReal, self.convertirReal(brazoA), color, 2, cv2.LINE_AA)
        cv2.circle(self.fondo, self.convertirReal(brazoA), int(6), self.amarillo, -1, cv2.LINE_AA)
        cv2.line(self.fondo, self.convertirReal(brazoA), self.convertirReal(brazoB), color, 2, cv2.LINE_AA)

    def distance(self,p1, p2):
        return sqrt(pow(p2[0] - p1[0], 2) + pow(p2[1] - p1[1], 2))

    def puntoInteres(self):
        moments = cv2.moments(self.mask)
        area = moments['m00']
        x = int(moments['m10'] / moments['m00'])
        y = int(moments['m01'] / moments['m00'])
        cv2.rectangle(self.fondo, (x, y), (x + 2, y + 2), (255, 0, 0), 2)

        cv2.line(self.fondo, self.origenReal, (x, y), (0, 255, 0), 1, cv2.LINE_AA)

        x0, y0 = self.convertir((x, y))
        self.interes=(x0,y0)
        return x0, y0

    def getData(self):
        self.puntoInteres()
        #interes=(x0,y0)
        angle = atan2(self.interes[1], self.interes[0]) * self.rad2deg
        dis = self.distance(self.origen, self.interes)
        #print("angulo: ", angle)
        #print("distancia:", dis)
        beta = 1 - ((dis ** 2) / (2 * (self.lb ** 2)))
        beta = acos(beta) * self.rad2deg
        anguloAyuda = beta
        alfa = 90 - beta / 2
        alfa = alfa + angle
        xbrazo1 = int(round(self.lb * cos(alfa * self.deg2grad), 0))
        ybrazo1 = int(round(self.lb * sin(alfa * self.deg2grad), 0))
        brazo1 = (xbrazo1, ybrazo1)
        self.dibujarBrazo(brazo1, self.interes, self.azul)
        alfa = alfa - angle
        alfa = angle - alfa
        xbrazo3 = int(round(self.lb * cos(alfa * self.deg2grad), 0))
        ybrazo3 = int(round(self.lb * sin(alfa * self.deg2grad), 0))
        brazo3 = (xbrazo3, ybrazo3)
        self.dibujarBrazo(brazo3, self.interes, self.verde)

        return self.interes,dis,angle,brazo1,brazo3,anguloAyuda

class readHSV:
    def __init__(self):
        pass
    def getMask(self):
        datahsv = pd.read_csv("current.csv")
        verde_bajos = np.array([datahsv.hMin[0], datahsv.sMin[0], datahsv.vMin[0]], dtype=np.uint8)
        verde_altos = np.array([datahsv.hMax[0], datahsv.sMax[0], datahsv.vMax[0]], dtype=np.uint8)
        tonos = (verde_bajos, verde_altos)
        return tonos

class Redraw:
    azul = (255, 0, 0)
    rojo = (0, 0, 255)
    verde = (0, 255, 0)
    amarillo = (0, 255, 255)
    morado = (255,0,255)

    # self.amarillo = (255, 255, 0)
    def __init__(self,fondo,lb,interes):
        self.fondo = fondo
        self.lb = lb
        self.rojo = (0,0,255)
        self.verde = (0,255,0)
        self.azul = (255,0,0)
        self.amarillo= (0,255,255)
        #self.amarillo = (255, 255, 0)
        self.negro= (0,0,0)
        self.rad2deg = 180/pi
        self.deg2grad = pi/180
        self.interes=interes
        self.h, self.w = self.fondo.shape[:2]
        self.h = int(self.h / 2)
        self.w = int(self.w / 2)
        self.h0, self.w0 = 0, 0
        self.origen = (self.w0, self.h0)
        self.origenReal = (self.w, self.h)

    def getOrigenReal(self):
        return self.origenReal

    def crearMarco(self):
        cv2.drawMarker(self.fondo, self.origenReal, self.rojo, markerType=2)
        cv2.line(self.fondo, (0, self.h), (2 * self.w, self.h), self.negro, 1, cv2.LINE_AA)
        cv2.line(self.fondo, (self.w, 0), (self.w, 2 * self.h), self.negro, 1, cv2.LINE_AA)
        cv2.circle(self.fondo, self.origenReal, int(0.9 * 2 * self.lb), self.rojo, 1, cv2.LINE_AA)
        cv2.circle(self.fondo, self.origenReal, int(0.1 * 2 * self.lb), self.rojo, 1, cv2.LINE_AA)
        return self.fondo

    def convertirReal(self,p1):
        xr = p1[0] + self.w
        yr = self.h - p1[1]
        return xr, yr

    def convertir(self,p1):
        xf = p1[0] - self.w
        yf = self.h - p1[1]
        return xf, yf

    def dibujarBrazo(self,brazoA, brazoB, color):
        cv2.line(self.fondo, self.origenReal, self.convertirReal(brazoA), color, 2, cv2.LINE_AA)
        cv2.circle(self.fondo, self.convertirReal(brazoA), int(6), self.amarillo, -1, cv2.LINE_AA)
        cv2.line(self.fondo, self.convertirReal(brazoA), self.convertirReal(brazoB), color, 2, cv2.LINE_AA)
        #cv2.circle(self.fondo, self.convertirReal(brazoA), 5, self.morado, -1)
        '''
        cv2.drawMarker(fondo, origenReal, rojo, markerType=2)
        cv2.line(fondo, (0, h), (2 * w, h), negro, 1, cv2.LINE_AA)
        cv2.line(fondo, (w, 0), (w, 2 * h), negro, 1, cv2.LINE_AA)
        cv2.circle(fondo, origenReal, int(0.9 * 2 * dis), rojo, 1, cv2.LINE_AA)
        cv2.circle(fondo, origenReal, int(0.1 * 2 * dis), rojo, 1, cv2.LINE_AA)
        cv2.circle(fondo, pInteres, tk, Color, -1)
        '''

    def distance(self,p1, p2):
        return sqrt(pow(p2[0] - p1[0], 2) + pow(p2[1] - p1[1], 2))

    def getDraw(self):

        angle = atan2(self.interes[1], self.interes[0]) * self.rad2deg

        dis = self.distance(self.origen, self.interes)
        beta = 1 - ((dis ** 2) / (2 * (self.lb ** 2)))
        beta = acos(beta) * self.rad2deg
        anguloAyuda = beta
        alfa = 90 - beta / 2
        alfa = alfa + angle
        xbrazo1 = int(round(self.lb * cos(alfa * self.deg2grad), 0))
        ybrazo1 = int(round(self.lb * sin(alfa * self.deg2grad), 0))
        brazo1 = (xbrazo1, ybrazo1)
        self.dibujarBrazo(brazo1, self.interes, self.azul)
        alfa = alfa - angle
        alfa = angle - alfa
        xbrazo3 = int(round(self.lb * cos(alfa * self.deg2grad), 0))
        ybrazo3 = int(round(self.lb * sin(alfa * self.deg2grad), 0))
        brazo3 = (xbrazo3, ybrazo3)
        self.dibujarBrazo(brazo3, self.interes, self.verde)
        cv2.circle(self.fondo, self.convertirReal(self.interes), 10, self.rojo, -1)

    def getPoint(self,tk,color):
        cv2.circle(self.fondo, self.convertirReal(self.interes), tk, color, -1)

