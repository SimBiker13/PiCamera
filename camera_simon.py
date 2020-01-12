#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Il faut créer un répertoire 'photos/' dans le répertoire courant,e.g. 'home/pi/photos'

import os
import time
import json
import send_mail_simon as Mail
import csv
from picamera import PiCamera
import MotionDetection as Motion

# liste de courriel (ou un seul) a qui tu veux envoyer les courriels de detections
destinataire_list = ['ruellands@gmail.com']

# parametres d'un compte email (gmail) qui servira a envoyer des courriels (ca en prends un...), mets-le tiens ;)
compte_envoi = "ruellands@gmail.com"
password_envoi = "Lolipop12354"

# mode = 'MINIMUM' ou mode = 'MAXIMUM'
# Si mode = 'MINIMUM', prends en note les détections mais ne prends pas de photo et n'envoie pas de emails
# Si mode = 'MAXIMUM', prends des photos et envoie des emails
mode = 'MAXIMUM' # mode = 'MINIMUM' ou mode = 'MAXIMUM'

# Parametres de l'algo de detection et de capture d'image
threshold   = 33 # How Much pixel changes (0 a 255 je pense...)
sensitivity = 1000 # How many pixels change
width       = 224
height      = 160
intervalle_2_captures = 1.5

while True:
    motionFound = False
    data1 = Motion.takeMotionImage(width, height)
    time.sleep(intervalle_2_captures)
    data2 = Motion.takeMotionImage(width, height)
    motionFound = Motion.detectMotion(data1, data2, threshold, sensitivity, width, height)

    if motionFound == True: # Si mouvement détecté, prends des photos si en mode MINIMUM, autrement fais juste noter le moment de détection dans un fichier 'Detection.csv'

        if mode != "MINIMUM":
            with PiCamera() as camera:
                camera.start_preview()
                captured_image = time.strftime("%Y-%m-%d") + '_' + time.strftime("%Hh%M-%S") + '_motion.jpg'
                camera.capture('./photos/' + captured_image)
                time.sleep(0.5)
                captured_image2 = time.strftime("%Y-%m-%d") + '_' + time.strftime("%Hh%M-%S") + '_motion.jpg'
                camera.capture('./photos/' + captured_image2)
                camera.stop_preview()
            s = 'Mouvement détecté à ' + time.strftime("%Hh%M") + ' du ' + time.strftime("%Y-%m-%d")
            Mail.sendMail(compte_envoi, password_envoi, destinataire_list, 'Mouvement détecté', s, files=[captured_image, captured_image2])
            # Ou si tu ne veux pas envoyer les photos par emails, tu peux effacer la ligne ci-haut et mettre celle ci-bas a la place:
            # Mail.sendMail(destinataire_list, 'Mouvement détecté', s)

            # Tu peux enlever les 3 prochaines lignes si tu veux, c'est pour effacer les photos automatiquement dans le repertoire lorsqu'il y en a trop, ex.: plus que 15
            folder_path = '/home/pi/photos/'
            dirListing = os.listdir(folder_path)
            if len(dirListing) > 15:
                os.system("sudo rm /home/pi/photos/*.jpg")

        # Notes tous les moments de détection dans un fichiers 'Detections.csv'
        # Tu peux aussi enlever ces 4 prochaines lignes si tu ne veux pas noter les instants de détection (date et heure)
        with open('Detections.csv', mode='a') as mesures_file:
            mesures_writer = csv.writer(mesures_file, delimiter=',')
            mesures_writer.writerow(
                [time.strftime("%A"), time.strftime("%Y"), time.strftime("%m"), time.strftime("%d"), time.strftime("%H"), time.strftime("%M")])
            mesures_file.close()





