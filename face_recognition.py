from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
from time import strftime
from datetime import datetime
import mysql.connector
import cv2
import os
import numpy as np


class Face_Recognotion:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("face_recognition_system")
        
        
        title_lbl= Label(self.root,text="FACE RECOGNITION",font= ("times new roman",30,"bold"),bg="white",fg="green")
        title_lbl.place(x=0,y=0,width=1530,height=45)
        #1st image
        img_top = Image.open(r"C:\Users\Dell\OneDrive\Desktop\face_recongition_system\face_recognition.jfif")
        img_top= img_top.resize((650,700),Image.ANTIALIAS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        
        f_lbl=Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=55,width=650,height=700)
        #2nd image 
        img_bottom = Image.open(r"C:\Users\Dell\OneDrive\Desktop\face_recongition_system\images\one.jpg")
        img_bottom= img_bottom.resize((950,700),Image.ANTIALIAS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
        
        f_lbl=Label(self.root,image=self.photoimg_bottom)
        f_lbl.place(x=650,y=55,width=950,height=700)
        
        #button
        b1_1=Button(f_lbl,text="Face Recognition",command=self.face_recog,cursor="hand2",font= ("times new roman",18,"bold"),bg="darkgreen",fg="white")
        b1_1.place(x=365,y=620,width=200,height=40)
        
        #=========attendance====================
    def mark_attendance(self, i, r, n, d):
        filename = "attendance.csv"
    
        with open(filename, "r+", newline="\n") as f:
            myDataList = f.readlines()  # Read all lines
            existing_records = set()  # Use a set to store existing records

            now = datetime.now()
            d1 = now.strftime("%d/%m/%Y")  # Get today's date
            dtString = now.strftime("%H:%M:%S")

        # Check for existing entries of the same person on the same date
            for line in myDataList:
                entry = line.strip().split(",")  # Remove newlines and split CSV
                if len(entry) >= 6:  # Ensure valid row structure
                    recorded_id, _, _, _, _, recorded_date, _ = entry  
                    if recorded_id == i and recorded_date == d1:
                        return  # Exit the function if entry exists

        # If no entry for today, mark attendance
            new_entry = f"{i},{r},{n},{d},{dtString},{d1},Present"
            f.write(f"{new_entry}\n")  # Append new entry
            
                
        
        
        #============ face recognition ==============
        
    def face_recog(self):
        def draw_boundray(img,classifier,scaleFactor,minNeighbors,color,text,clf):
            gray_image =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)
        
            coord=[]
        
            for(x,y,w,h) in features: 
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict=clf.predict(gray_image[y:y+h,x:x+w])
                confidence=int((100*(1-predict/300)))
            
                conn=mysql.connector.connect(host="localhost",username="root",password="unnati",database="attendance_system")
                my_cursor=conn.cursor()
                
                my_cursor.execute("select Name from student where Student_id="+str(id))
                n=my_cursor.fetchone()
                #name = n[0] if n else "Unknown"
                n="+".join(n)
                
                my_cursor.execute("select Roll from student where Student_id="+str(id))
                r=my_cursor.fetchone()
                #roll = r[0] if r else "Unk
                # nown"
                r="+".join(r)
                
                my_cursor.execute("select Dep from student where Student_id="+str(id))
                d=my_cursor.fetchone()
                #department = d[0] if d else "Unknown"
                d="+".join(d)
                
                my_cursor.execute("select Student_id from student where Student_id="+str(id))
                i=my_cursor.fetchone()
                #department = d[0] if d else "Unknown"
                i="+".join(i)
                
                
                if confidence>77:
                    cv2.putText(img,f"ID:{i}",(x,y-75),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Roll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Name:{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Department:{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    self.mark_attendance(i,r,n,d)
                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"Unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                       
                coord=[x,y,w,y]
                
            return coord
        
        def recognize(img,clf,faceCascade):
            coord = draw_boundray(img,faceCascade,1.1,10,(255,255,255),"Face",clf)
            return img
        
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")
        
        video_cap = cv2.VideoCapture(0)
        while True:
            ret,img=video_cap.read()
            img = recognize(img,clf,faceCascade)
            cv2.imshow("Welcome to face Recognition",img)
            
            if cv2.waitKey(1) == 13:
                break
        video_cap.release()
        cv2.destroyAllWindows() 

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognotion(root)
    root.mainloop()