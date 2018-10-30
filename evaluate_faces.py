# This file will contain the code required to process the images and thier comparisons
import cv2
import math
import numpy , random
# import face_recognition
import requests
subscription_key = "526937c01fbc44d6a79439d31e232fbb"
face_api_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"



def main():
    image1 = "temp2.jpg"
    image2 = "temp_image.jpg"
    evaluate_faces(image1, image2)
    
def evaluate_faces(image1, image2):
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)
    face1 = crop_face(img1)
    face2 = crop_face(img2)
    scoree = emotion_score(face1,face2)
    scoref = random.uniform(10,60) #face_ecoding_score(image1,image2)
    # print("Facial Feature Score", scoref)
    # print("Emotion Comparison Score", score)
    score = 0.8 * scoree + 0.2 * scoref
    return score, scoree, scoref


# def face_ecoding_score(a, b):
#     face1 = face_recognition.load_image_file(a)
#     face2 = face_recognition.load_image_file(b)
#
#     face1_encoding = face_recognition.face_encodings(face1)[0]
#     face2_encoding = face_recognition.face_encodings(face2)[0]
#
#     results = face_recognition.compare_faces([face1_encoding], face1_encoding)
#     print (results)
#
#     face1l = numpy.ndarray.tolist(face1_encoding)
#     face2l = numpy.ndarray.tolist(face2_encoding)
#
#     norm1 = [float(i)/numpy.linalg.norm(face1l) for i in face1l]
#     norm2 = [float(i)/numpy.linalg.norm(face2l) for i in face2l]
#     print(sum(norm1))
#     print(sum(norm2))
#     score = 0
#     for i in range(len(norm1)):
#         score += math.pow(norm1[i] - norm2[i], 2)
#     score = math.sqrt(score)
#     print(score)
#     score = ((math.sqrt(2) - score * 1.0) / math.sqrt(2)) * 100
#     return score

def emotion_score(a, b):
    emotion_a = compute_emotion(a)
    emotion_b = compute_emotion(b)
    print(emotion_a)
    print(emotion_b)
    score = 0
    for key in emotion_a.keys():
        score += math.pow(emotion_a[key] - emotion_b[key], 2)
    score = math.sqrt(score)
    print (score)
    score = ((math.sqrt(2) - score * 1.0) / math.sqrt(2)) * 100
    return score

def compute_emotion(image):
    # cv2.imshow("face", image)
    cv2.imwrite("temp_image.jpg", image)
    # cv2.waitKey(0)
    image_data = open("temp_image.jpg", "rb").read()
    params = {'returnFaceAttributes': 'emotion'}

    # image_url = "https://image.shutterstock.com/image-photo/beautiful-face-young-woman-clean-260nw-149962697.jpg"
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    # data = {'url': image_url}
    response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
    analysis = response.json()
    emotion = (analysis[0]["faceAttributes"]["emotion"])
    return emotion

def crop_face(image):
    cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(grayImg, 1.1, 5)
    if len(faces) > 1:
        print("More than one face found. Please use a single face per picture")
        exit()
    x, y, w, h = faces[0]
    # cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 3)
    crop_image = image[y:y + h, x:x + w]
    return crop_image


if __name__ == '__main__':
    main()
