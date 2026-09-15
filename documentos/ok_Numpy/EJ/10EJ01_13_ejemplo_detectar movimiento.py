import cv2
import numpy as np

# Intentar abrir la webcam (usa 0, 1 o 2 según el sistema)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: No se pudo abrir la cámara.")
    exit()

# Leer el primer frame
ret, frame1 = cap.read()
if not ret:
    print("❌ Error: No se pudo leer el primer frame.")
    cap.release()
    exit()

# Preprocesar primer frame
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

while True:
    # Capturar siguiente frame
    ret, frame2 = cap.read()
    if not ret:
        print("⚠️ Advertencia: No se pudo leer el siguiente frame.")
        break

    # Convertir a gris y aplicar desenfoque
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    # Comparar frames
    delta = cv2.absdiff(gray1, gray2)
    _, thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Detectar contornos de zonas con cambio
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar rectángulos si el área del cambio es significativa
    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Mostrar el resultado
    cv2.imshow("Detección de Movimiento", frame2)

    key = cv2.waitKey(30)
    if key == 27:  # ESC para salir
        break

    # Actualizar el frame anterior
    gray1 = gray2

cap.release()
cv2.destroyAllWindows()
