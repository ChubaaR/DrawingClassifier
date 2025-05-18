# 🖌️ Drawing Classifier

A simple GUI-based machine learning tool built with Tkinter and scikit-learn that allows users to draw shapes, classify them into three categories, and train/predict using various classifiers.

## ✨ Features

* Draw directly on a canvas with a variable brush size
* Classify drawings into three custom categories
* Train and switch between different ML models:

  * Linear SVM
  * K-Nearest Neighbors
  * Logistic Regression
  * Decision Tree
  * Gaussian Naive Bayes
* Save and load models
* Persistent project saving with classification data and model

## 🛠️ Technologies Used

* Python 3
* Tkinter (GUI)
* PIL (Image processing)
* OpenCV (Image reading)
* scikit-learn (ML models)
* NumPy
* Pickle (Model saving/loading)

## 📸 Screenshots

![Screenshot 2025-05-18 184522](https://github.com/user-attachments/assets/95f4f446-04ab-4f38-9304-797d4795c2da)


## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3 installed. Then install the required libraries:

```bash
pip install numpy opencv-python scikit-learn pillow
```

### Running the Project

```bash
python drawing_classifier.py
```

### Usage

1. When prompted, enter a **project name**.
2. Enter names for **three classes** (e.g., Circle, Square, Triangle).
3. Draw examples for each class and click the class buttons to save.
4. Train the model using the **Train Model** button.
5. Use **Predict Class** to classify new drawings.
6. Use **Save Everything** to save your current project state.

## 🧠 Model Switching Order

You can cycle through the following models using the **Change Model** button:

```
LinearSVC → KNeighborsClassifier → LogisticRegression → DecisionTreeClassifier → GaussianNB → back to LinearSVC
```

## 📁 Project Structure

```
<project_name>/
├── class1/
│   ├── 1.png
│   └── ...
├── class2/
├── class3/
└── model.pkl
```

## 💾 Save & Load

* **Save Model** saves only the trained classifier.
* **Save Everything** saves classifier, class names, counters, and project name.
* **Load Model** loads a previously saved classifier (`.pkl` file).

## ⚠️ Notes

* All images are resized to 50x50 before training.
* Brush strokes are drawn in black over a white canvas.
* Keep the saved images consistent in size and drawing style for better model accuracy.

## 📜 License

This project is licensed under the MIT License.

## 🤝 Contributions

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
