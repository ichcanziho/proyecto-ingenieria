from armich import *
datos = np.load("data.npy")

fondo = cv2.imread("blanco.png")
for dato in datos:
    interes = tuple(dato)
    draw = Redraw(fondo,180,interes)
    draw.crearMarco()
    draw.getPoint(5,draw.morado)
    cv2.imshow("draw", fondo)
    cv2.waitKey(20)
cv2.waitKey(0)
''''
for dato in datos:
    fondo = cv2.imread("blanco.png")
    interes = tuple(dato)
    draw = Redraw(fondo,180,interes)
    draw.crearMarco()
    draw.getDraw()
    cv2.imshow("draw", fondo)
    cv2.waitKey(20)
cv2.waitKey(0)
'''
cv2.destroyAllWindows()