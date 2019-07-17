from armich import*
import pandas as pd
puntos,distancias,angulos,angulos2,joints1,joints2 = [],[],[],[],[],[]
mask = readHSV()
tonos = mask.getMask()
longitud_brazo = 160

#video = cv2.VideoCapture("bolaVerde.wmv")
video = cv2.VideoCapture(0)
_, fondo = video.read()

while(1):
    try:
        _, fondo = video.read()
        db = DibujarBrazo(tonos, fondo, longitud_brazo)
        db.crearMarco()
        punto, distancia, angulo, joint1, joint2, angulo2 = db.getData()
        cv2.imshow("Procesado",fondo)
        puntos.append(punto)
        distancias.append(distancia)
        angulos.append(angulo)
        joints1.append(joint1)
        joints2.append(joint2)
        angulos2.append(angulo2)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    except:
        cv2.waitKey(0)
        break;
video.release()
cv2.destroyAllWindows()

dict = {"Punto[x,y]": puntos,
        "Distancia":distancias,
        "Angulo": angulos,
        "Joint 1[x,y]":joints1,
        "Joint 2[x,y]":joints2,
        "Angulo Ayuda":angulos2
        }
data = pd.DataFrame(dict)
print(data)