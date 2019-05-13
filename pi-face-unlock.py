print("Running face recognizer.")
print("Loading modules...")
from pygame import camera
import pygame.image
from subprocess import call
from time import sleep
import sys

print("Initializing camera...")
camera.init()
if len(camera.list_cameras()) == 0:
    print("No webcams found.")
    sys.exit()
cam = camera.Camera(camera.list_cameras()[0], (320, 240))
#cam.start()

print("Loading face recognizer...")
import face_recognition as fr

print("Loading known face encodings...")
imageNames = ["Benjamin", "Julie", "Zoe"]
loaded_images = []
known_faces = []

for imageName in imageNames:
    path = "Images/" + imageName + ".jpg"
    loaded_images.append(fr.load_image_file(path))

for image in loaded_images:
    try:
        known_faces.append(fr.face_encodings(image)[0])
    except IndexError:
        print("--- ALERT: One of the face encodings does not contain a face. ---")

def addFace():
    print("You are not recognized.")

call(['rm', 'Images/PreviousLogin.jpg'])
call(['mv', 'Images/lastImg.jpg', 'Images/PreviousLogin.jpg'])
call(['cp', 'Images/nothing.jpg', 'Images/lastImg.jpg'])
print("Please look at camera.")

face_encodings = []
lastFrameWasFace = True

def search():
    global lastFrameWasFace
    imgSurf = cam.get_image()
    pygame.image.save(imgSurf, "Images/lastImg.jpg")
    img = fr.load_image_file('Images/lastImg.jpg')
    face_locations = fr.face_locations(img)
    if len(face_locations) > 0 or lastFrameWasFace:
        print("found {} face(s)".format(len(face_locations)))
    if len(face_locations) > 0:
        lastFrameWasFace = True
    else:
        lastFrameWasFace = False
    face_encodings = fr.face_encodings(img, face_locations)
    
    for face in face_encodings:
        matches = fr.compare_faces(known_faces, face)

        for i in range(len(matches)):
            if matches[i]:
                print("Hello, {}".format(imageNames[i]))
                #login(usernames[i])
            
        #addFace()

cam.start()
attempt_count = 0

try:
    while True:
        search()
        attempt_count += 1
        if attempt_count >= 10:
            print("Please look at the camera.")
            attempt_count = 0

except KeyboardInterrupt:
    print("Goodbye!")
    cam.stop()
    sleep(1)
    sys.exit()
    
    
            
    
        
