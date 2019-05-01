import os
import cv2
import numpy as np
from PIL import Image

recognizer = cv2.createLBPHFaceRecognizer();
path = 'C:/Python27/Scripts/faceRecog/dataset'


def getImagesWithID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L');
        faceNp = np.array(faceImg, 'uint8')
        print (os.path.split(imagePath)[-1].split('.')[1])
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        # print (os.path.split(imagePath)[-1].split('.')[0])
        print ID
        faces.append(faceNp)
        # print(ID)
        IDs.append(ID)
        cv2.imshow("training", faceNp)
        cv2.waitKey(10)
    return np.array(IDs), faces


Ids, faces = getImagesWithID(path)
recognizer.train(faces,Ids)
recognizer.save('C:/Python27/Scripts/faceRecog/trainingData.yml')
cv2.destroyAllWindows()

