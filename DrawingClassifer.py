import pickle
import os.path
import numpy as np
import PIL
import PIL.Image
from PIL import ImageDraw
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
        message = Tk()
        message.withdraw()

        self.projectName = simpledialog.askstring("Project Name", "Please enter your project name:", parent = message)

        #this is just incase project name already exists, then we can just load it instead of creating a new project
        if os.path.exists(self.projectName):
            with open(f"{self.projectName}/model.pkl", "rb") as file:
                data = pickle.load(file)
            self.class1 = data['c1']
            self.class2 = data['c2']
            self.class3 = data['c3']
            self.class1Counter = data['c1c']
            self.class2Counter = data['c2c']
            self.class3Counter = data['c3c']
            self.classifier = data['classifier']
            self.projectName = data['projectName']
        else:
            self.class1 = simpledialog.askstring("Class 1", "Please enter the name of class 1:", parent = message)
            self.class2 = simpledialog.askstring("Class 2", "Please enter the name of class 2:", parent = message)
            self.class3 = simpledialog.askstring("Class 3", "Please enter the name of class 3:", parent = message)

            self.class1Counter = 1
            self.class2Counter = 1
            self.class3Counter = 1

            self.classifier = LinearSVC()

            os.mkdir(self.projectName)
            os.chdir(self.projectName)
            os.mkdir(self.class1)
            os.mkdir(self.class2)
            os.mkdir(self.class3)
            os.chdir("..")

    def initGUI(self):
        #this is where we create the GUI for the system

        WIDTH = 500
        HEIGHT = 500
        WHITE = (255, 255, 255)
        self.root = Tk()
        self.root.title(f"Drawing Classifier Program {self.projectName}")

        self.canvas = Canvas(self.root, width = WIDTH-10, height = HEIGHT-10, bg='white')
        self.canvas.pack(expand = YES, fill = BOTH)

        #binding the motion of clicking a button with a function
        self.canvas.bind("<B1-Motion>", self.paint)

        self.image1 = PIL.Image.new("RGB", (WIDTH, HEIGHT), WHITE)
        self.draw = ImageDraw.Draw(self.image1)

        buttonFrame = tkinter.Frame(self.root)
        buttonFrame.pack(fill= X, side=BOTTOM)
        buttonFrame.columnconfigure(0, weight=1)
        buttonFrame.columnconfigure(1, weight=1)
        buttonFrame.columnconfigure(2, weight=1)

        class1Button = Button(buttonFrame, text = self.class1, command = lambda: self.save(1))
        class1Button.grid(row = 0, column = 0, sticky = W + E)

        class2Button = Button(buttonFrame, text = self.class2, command = lambda: self.save(2))
        class2Button.grid(row = 0, column = 1, sticky = W + E)

        class3Button = Button(buttonFrame, text = self.class3, command = lambda: self.save(3))
        class3Button.grid(row = 0, column = 2, sticky = W + E)

        brushSizeMinusButton = Button(buttonFrame, text = "Brush Size", command = lambda: self.brushminus)
        brushSizeMinusButton.grid(row = 1, column = 0, sticky = W + E)

        clearButton = Button(buttonFrame, text="Clear", command = self.clear)
        clearButton.grid(row = 1, column = 1, sticky = W + E)

        brushSizeMinusButton = Button(buttonFrame, text = " + Brush Size", command = lambda: self.brushplus)
        brushSizeMinusButton.grid(row = 1, column = 2, sticky = W + E)

        trainButton = Button(buttonFrame, text = "Train Model", command = self.trainModel)
        trainButton.grid(row = 2, column = 0, sticky = W + E)

        saveModelButton = Button(buttonFrame, text="Save Model", command = self.saveModel)
        saveModelButton.grid(row = 2, column = 1, sticky = W + E)

        loadModelButton = Button(buttonFrame, text="Load Model", command = self.loadModel)
        loadModelButton.grid(row = 2, column = 2, sticky = W + E)

        changeModelButton = Button(buttonFrame, text = "Change Model", command = self.changeModel)
        changeModelButton.grid(row = 3, column = 0, sticky = W + E)

        predictButton = Button(buttonFrame, text = "Predict Class", command = self.predictClass)
        predictButton.grid(row = 3, column = 1, sticky = W + E)

        saveEverythingButton = Button(buttonFrame, text = "Save Everything", command = self.saveEverything)
        saveEverythingButton.grid(row = 3, column = 2, sticky = W + E)


        self.statusLabel = Label(buttonFrame, text=f"Current Model: {type(self.classifier).__name__}")
        self.statusLabel.config(font=("Arial", 10))
        self.statusLabel.grid(row = 4, column = 1, sticky = W + E)

        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.root.attributes("-topmost", True)
        self.root.mainloop()


    def paint(self, event):
        x1, y1 = (event.x -1), (event.y -1)
        x2, y2 = (event.x +1), (event.y +1)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill='black', width=self.brushwidth)
        self.draw.rectangle([x1, y1, x2 + self.brushwidth, y2 + self.brushwidth], fill='black', width = self.brushwidth)

    def save(self, classNumber):
        self.image1.save("temp.png")
        image = PIL.Image.open("temp.png")
        image.thumbnail((50, 50), PIL.Image.LANCZOS)

        if classNumber == 1:
            image.save(f"{self.projectName}/{self.class1}/{self.class1Counter}.png", "PNG")
            self.class1Counter += 1
        
        elif classNumber == 2:
            image.save(f"{self.projectName}/{self.class2}/{self.class2Counter}.png", "PNG")
            self.class2Counter += 1
        
        elif classNumber == 3:
            image.save(f"{self.projectName}/{self.class3}/{self.class3Counter}.png", "PNG")
            self.class3Counter += 1

        self.clear()


    def brushminus(self):
        if self.brushwidth > 1:
            self.brushwidth -= 1

    def brushplus(self):
        if self.brushwidth < 100:
            self.brushwidth += 1
        
    def clear(self):
        self.canvas.delete("all")

        #not just the canvas needs to be clear, whatever we drew using PIL should be cleared accordingly as well
        self.draw.rectangle([0, 0, 800, 800], fill="white")

    def trainModel(self):
        imageList = np.array([])
        classList = np.array([])

        for x in range(1, self.class1Counter):
            image = cv.imread(f"{self.projectName}/{self.class1}/{x}.png")[:,:,0]
            image = image.reshape(2500)
            imageList = np.append(imageList, [image])
            classList = np.append(classList, 1)

        for x in range(1, self.class2Counter):
            image = cv.imread(f"{self.projectName}/{self.class2}/{x}.png")[:,:,0]
            image = image.reshape(2500)
            imageList = np.append(imageList, [image])
            classList = np.append(classList, 2)
        
        for x in range(1, self.class3Counter):
            image = cv.imread(f"{self.projectName}/{self.class3}/{x}.png")[:,:,0]
            image = image.reshape(2500)
            imageList = np.append(imageList, [image])
            classList = np.append(classList, 3)

        imageList = imageList.reshape(self.class1Counter -1 + self.class2Counter -1 + self.class3Counter - 1, 2500)

        self.classifier.fit(imageList, classList)
        tkinter.messagebox.showinfo("Drawing Classifier", "Model successfully trained!", parent = self.root)

    def saveModel(self):
        filePath = filedialog.asksaveasfilename(defaultextension="pickle")
        with open(filePath, "wb") as f:
            pickle.dump(self.classifier, f)
        tkinter.messagebox.showinfo("Drawing Classifier", f"Model successfully saved!", parent = self.root)
        
    def loadModel(self):
        filePath = filedialog.askopenfilename()
        with open(filePath, "rb") as f:
            self.classifier = pickle.load(f)
        tkinter.messagebox.showinfo("Drawing Classifier", f"Model successfully loaded!", parent = self.root)

    def changeModel(self):
        if isinstance(self.classifier, LinearSVC):
            self.classifier = KNeighborsClassifier()
        elif isinstance(self.classifier, KNeighborsClassifier):
            self.classifier = LogisticRegression()
        elif isinstance(self.classifier, LogisticRegression):
            self.classifier = DecisionTreeClassifier()
        elif isinstance(self.classifier, DecisionTreeClassifier):
            self.classifier = GaussianNB()
        elif isinstance(self.classifier, GaussianNB):
            self.classifier = LinearSVC()

        self.statusLabel.config(text=f"Current Model: {type(self.classifier).__name__}")

    def predictClass(self):
        self.image1.save("temp.png")
        image = PIL.Image.open("temp.png")
        image.thumbnail((50, 50), PIL.Image.LANCZOS)
        image.save("predictClass.png", "PNG")

        image = cv.imread("predictClass.png")[:,:,0]
        image = image.reshape(2500)
        prediction = self.classifier.predict([image])
        if prediction[0] == 1:
            tkinter.messagebox.showinfo("Drawing Classifier", f"This is probably a(n) {self.class1}", parent = self.root)

        elif prediction[0] == 2:
            tkinter.messagebox.showinfo("Drawing Classifier", f"This is probably a(n) {self.class2}", parent = self.root)
        
        elif prediction[0] == 3:
            tkinter.messagebox.showinfo("Drawing Classifier", f"This is probably a(n) {self.class3}", parent = self.root)

    def saveEverything(self):
        data = {"c1": self.class1, 
                "c2": self.class2, 
                "c3": self.class3,
                "c1c": self.class1Counter,
                "c2c": self.class2Counter,
                "c3c": self.class3Counter,
                "classifier": self.classifier,
                "projectName": self.projectName}
        with open(f"{self.projectName}/model.pkl", "wb") as f:
            pickle.dump(data, f)

        tkinter.messagebox.showinfo("Drawing Classifier", "Project successfully saved!", parent = self.root)

    def onClosing(self):
        answer = tkinter.messagebox.askyesno("Quit?", "Do you want to save?", parent = self.root)

        if answer is not None:
            if answer:
                self.saveEverything
            self.root.destroy()
            exit()

# Run the program
DrawingClassifier()

