import tkinter as tk
from tkinter import filedialog
from tkinter import Label
from PIL import Image, ImageTk
import tensorflow as tf
import numpy as np

# Step 1: Encapsulation - We are wrapping the functionality inside the ImageClassifier class
class ImageClassifierApp:
    def __init__(self, master): 
        self.master = master
        master.title("Image Classification App")

        self.label = Label(master, text="Select an image for classification")
        self.label.pack()

        self.upload_button = tk.Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.classify_button = tk.Button(master, text="Classify Image", command=self.classify_image)
        self.classify_button.pack()

        self.result_label = Label(master, text="")
        self.result_label.pack()

        # Load AI model (Encapsulation: Wrapping the model inside the class)
        self.model = self.load_model()

    def load_model(self):
        # Loading a pre-trained model using TensorFlow
        model = tf.keras.applications.MobileNetV2(weights='imagenet')
        return model

    def upload_image(self):
        # Multiple Inheritance Example: Inheriting tkinter's filedialog function
        file_path = filedialog.askopenfilename()
        self.image_path = file_path

        img = Image.open(file_path)
        img = img.resize((224, 224))
        img = ImageTk.PhotoImage(img)
        
        # Display image on the Tkinter window
        self.image_label = Label(self.master, image=img)
        self.image_label.image = img
        self.image_label.pack()

    def classify_image(self):
        # Polymorphism: Using the same method for various inputs (method behaves differently for different data)
        img = Image.open(self.image_path)
        img = img.resize((224, 224))

        # Convert image to numpy array and pre-process it
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

        # Make prediction
        prediction = self.model.predict(img_array)
        result = tf.keras.applications.mobilenet_v2.decode_predictions(prediction, top=1)[0][0][1]

        # Display result
        self.result_label.config(text=f"Prediction: {result}")

# Step 2: Create Tkinter root and run the application
root = tk.Tk()
app = ImageClassifierApp(root)
root.mainloop()
