import tkinter as tk
import csv
import cv2
import os
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

from numpy import double

window = tk.Tk()
window.title("STUDENT ATTENDANCE USING FACE RECOGNITION SYSTEM")
window.geometry('800x500')

teri baara bajau
#last pull request
efhfuehuhefuhfuehfuhueheuhufhnb dhxbzdnbs nhcbakjcfbsajcbjcbsakcbasbsacfbj
dialog_title = 'QUIT'
dialog_text = "are you sure?"
window.configure(background='aqua')
window.grid_rowconfigure(0, weight=1)ho gaya
window.grid_columnconfigure(0, weight=1) khatam sab


def clear():
    std_name.delete(0, 'end')
    res = ""
    label4.configure(text=res) kar le bhai


def clear2():
    std_number.delete(0, 'end')
    res = ""
    label4.configure(text=res)


def takeImage():
    
    name = (std_name.get())
    Id = (std_number.get())
    if name.isalpha():
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.1, 3)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum = sampleNum + 1
                # store each student picture with its name and id
                cv2.imwrite("TrainingImages\ " + name + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + h])
                cv2.imshow('FACE RECOGNIZER', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # stop the camera when the number of picture exceed 50 pictures for each student
            if sampleNum > 50:
                break

        cam.release()
        cv2.destroyAllWindows()
        # print the student name and id after a successful face capturing
        res = 'Student details saved with: \n Enrollment Number : ' + Id + ' and Name: ' + name

        row = [Id, name]

        with open('studentDetailss.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        label4.configure(text=res)
    else:

        if name.isalpha():
            res = "Enter correct Enrollment Number"
            label4.configure(text=res)


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids

def trainImage():
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    face, Ids = getImagesAndLabels("D:\STUDENT-ATTENDANCE\TrainingImages")

    recognizer.train(face, np.array(Ids))
    recognizer.save("trainner/trainner.yml")
    res = "Image Trained"
    label4.configure(text=res)


def trackImage():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    cam = cv2.VideoCapture(0)

    recognizer.read("trainner/trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("studentDetailss.csv")
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    # create a dataframe to hold the student id,name,date and time
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 3)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            #  a confidence less than 50 indicates a good face recognition
            if conf < 60:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
                aa = df.loc[df['ID'] == Id]['NAME'].values
                tt = str(Id) + "-" + aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                row2 = [Id, aa, date, timeStamp]
                #   open the attendance file for update
                with open('AttendanceFile.csv', 'a+') as csvFile2:
                    writer2 = csv.writer(csvFile2)
                    writer2.writerow(row2)
                csvFile2.close()
                # print attendance updated on the notification board of the GUI
                res = 'Attendance Marked'
                label4.configure(text=res)

            else:
                Id = 'Unknown'
                tt = str(Id)
                #  store the unknown images in the images unknown folder
                if conf > 65:
                    noOfFile = len(os.listdir("UnknownImages")) + 1
                    cv2.imwrite("UnknownImages\Image" + str(noOfFile) + ".jpg", img[y:y + h, x:x + w])
                    res = 'ID unknown, Attendance not marked'
                    label4.configure(text=res)
            # To avoid duplication in the attendance file.
            attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
            # show the student id and name
            cv2.putText(img, str(tt), (x, y + h - 10), font, 0.8, (255, 255, 255), 1)
            cv2.imshow('FACE RECOGNIZER', img)
        if cv2.waitKey(1000) == ord('q'):
            break

        cam.release()
        cv2.destroyAllWindows()


label1 = tk.Label(window, background="aqua", fg="black", text="Name :", width=10, height=1,
                  font=('Helvetica', 16))
label1.place(x=83, y=40)
std_name = tk.Entry(window, background="cyan", fg="black", width=25, font=('Helvetica', 14))
std_name.place(x=280, y=41)
label2 = tk.Label(window, background="aqua", fg="black", text="Enrollment No. :", width=14, height=1,
                  font=('Helvetica', 16))
label2.place(x=100, y=90)
std_number = tk.Entry(window, background="cyan", fg="black", width=25, font=('Helvetica', 14))
std_number.place(x=280, y=91)

clearBtn1 = tk.Button(window, background="black", command=clear, fg="white", text="Clear", width=8, height=1,
                      activebackground="pink", font=('Helvetica', 10))
clearBtn1.place(x=580, y=42)
clearBtn2 = tk.Button(window, background="black", command=clear2, fg="white", text="Clear", width=8,
                      activebackground="pink", height=1, font=('Helvetica', 10))
clearBtn2.place(x=580, y=92)

label3 = tk.Label(window, background="darkcyan", fg="white", text="Notification:", width=10, height=1,
                  font=('Helvetica', 20, 'underline'))
label3.place(x=320, y=155)
label4 = tk.Label(window, background="lightblue", fg="black", width=55, height=4, font=('Helvetica', 14, 'italic'))
label4.place(x=95, y=205)

takeImageBtn = tk.Button(window, command=takeImage, background="blue", fg="white", text="New Entry",
                         activebackground="pink",
                         width=15, height=3, font=('Helvetica', 12))
takeImageBtn.place(x=130, y=360)
trainImageBtn = tk.Button(window, command=trainImage, background="blue", fg="white", text="Train Model",
                          activebackground="pink",
                          width=15, height=3, font=('Helvetica', 12))
trainImageBtn.place(x=340, y=360)
trackImageBtn = tk.Button(window, command=trackImage, background="blue", fg="white", text="Mark Attendance", width=15,
                          activebackground="pink", height=3, font=('Helvetica', 12))
trackImageBtn.place(x=550, y=360)

window.mainloop()
