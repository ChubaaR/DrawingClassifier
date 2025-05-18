import pickle
import os.path
import numpy as np
import PIL
import PIL.Image, PIL.ImageDraw
import cv2 as cv
from tkinter import *
from tkinter import simpledialog, filedialog
import tkinter.messagebox
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

class DrawingClassifier:
    def __init__(self):
        #just for defining attributes
        #we're going to allow the model to guess from three classes defined so this is how
        self.class1, self.class2, self.class3 = None, None, None

        #the counters are used for tracking how many examples we're feeling the model for each class
        #we should initiate them as non appropriately
        self.class1Counter, self.class2Counter, self.class3Counter = None, None, None

        #the (variable) classifier: None
        self.classifier = None

        #name of directory we're storing the items in
        self.projectName = None
        self.root = None
        self.image1 = None
        self.statusLabel = None
        self.canvas = None
        self.draw = None

        #default brush size
        self.brushwidth = 15
        self.classesPrompt()
        self.initGUI()


    def classesPrompt(self):
        message - Tk()
        message.withdraw()

        self.project_name = simpledialog.askstring("Project Name", "Please enter your project name:", parent = message)

        #this is just incase project name already exists, then we can just load it instead of creating a new project
        if os.path.exists(self.projectName):
            with open(f"{self.projectName}/model.pkl", "rb") as file:





    def initGUI(self):
        self.root = Tk()
        self.root.title("Drawing Classifier Program")
        self.canvas = Canvas(self.root, width=280, height=280, bg='white')
        self.canvas.pack()
        self.image = Image.new("L", (280, 280), 255)
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.bind("<B1-Motion>", self.paint)
        
        buttonFrame = Label(self.root)
        buttonFrame.pack()
        
        Button(buttonFrame, text="Class 1", command=lambda: self.save(1)).pack(side='left')
        Button(buttonFrame, text="Class 2", command=lambda: self.save(2)).pack(side='left')
        Button(buttonFrame, text="Class 3", command=lambda: self.save(3)).pack(side='left')
        Button(buttonFrame, text="Train Model", command=self.trainModel).pack(side='left')
        Button(buttonFrame, text="Predict", command=self.predictClass).pack(side='left')
        Button(buttonFrame, text="Clear", command=self.clear).pack(side='left')

        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.root.mainloop()

    def paint(self, event):
        x1, y1 = (event.x - self.brushWidth), (event.y - self.brushWidth)
        x2, y2 = (event.x + self.brushWidth), (event.y + self.brushWidth)
        self.canvas.create_oval(x1, y1, x2, y2, fill='black')
        self.draw.ellipse([x1, y1, x2, y2], fill='black')

    def save(self, classNumber):
        folder = f"./{self.project_name.get()}/class{classNumber}"
        count = len(os.listdir(folder))
        self.image.save(f"{folder}/{count}.png")
        self.clear()

    def clear(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (280, 280), 255)
        self.draw = ImageDraw.Draw(self.image)

    def trainModel(self):
        imageList, classList = [], []
        for i in range(1, 4):
            folder = f"./{self.project_name.get()}/class{i}"
            for file in os.listdir(folder):
                img = cv2.imread(f"{folder}/{file}", 0)
                img = cv2.resize(img, (28, 28)).flatten()
                imageList.append(img)
                classList.append(i)
        self.classifier = LinearSVC()
        self.classifier.fit(imageList, classList)
        messagebox.showinfo("Training", "Model Trained Successfully!")

    def predictClass(self):
        self.image.save("temp.png")
        img = cv2.imread("temp.png", 0)
        img = cv2.resize(img, (28, 28)).flatten()
        prediction = self.classifier.predict([img])[0]
        messagebox.showinfo("Prediction", f"Predicted Class: {prediction}")
        self.clear()

    def saveEverything(self):
        with open(f"./{self.project_name.get()}/model.pkl", "wb") as f:
            pickle.dump(self.classifier, f)
        messagebox.showinfo("Save", "Model and Data Saved Successfully!")

    def load_project(self):
        try:
            with open(f"./{self.project_name.get()}/model.pkl", "rb") as f:
                self.classifier = pickle.load(f)
            messagebox.showinfo("Load", "Model Loaded Successfully!")
        except FileNotFoundError:
            messagebox.showwarning("Load", "No previous model found. Training required.")

    def onClosing(self):
        if messagebox.askyesno("Quit", "Do you want to save before exiting?"):
            self.saveEverything()
        self.root.destroy()

if __name__ == "__main__":
    DrawingClassifier()

