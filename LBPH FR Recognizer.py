import cv2
import os
import numpy as np


# Create a face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def train_model(label):
    # Create lists to store the face samples and their corresponding labels
    faces = []
    labels = []
     
    # Load the images from the 'Faces' folder
    for file_name in os.listdir('Faces'):
        if file_name.endswith('.jpg'):
            # Extract the label (person's name) from the file name
            name = file_name.split('_')[0]
             
            # Read the image and convert it to grayscale
            image = cv2.imread(os.path.join('Faces', file_name))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
            # Detect faces in the grayscale image
            detected_faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (30, 30))
 
            # Check if a face is detected
            if len(detected_faces) > 0:
                # Crop the detected face region
                face_crop = gray[detected_faces[0][1]:detected_faces[0][1] + detected_faces[0][3],
                                 detected_faces[0][0]:detected_faces[0][0] + detected_faces[0][2]]
 
                # Append the face sample and label to the lists
                faces.append(face_crop)
                labels.append(label[name])
 
    # Train the face recognition model using the faces and labels
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
 
    # Save the trained model to a file
    recognizer.save('trained_model.xml')
    return recognizer
 

label = {
    "griffin":0,
    "dhaya":1
    }
label


# Train the model
Recognizer = train_model(label)
Recognizer


# Function to recognize faces
def recognize_faces(recognizer, label):
	# Open the camera
	cap = cv2.VideoCapture(0)
	
	# Reverse keys and values in the dictionary
	label_name = {value: key for key, value in label.items()}
	while True:
		# Read a frame from the camera
		ret, frame = cap.read()

		# Convert the frame to grayscale
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Detect faces in the grayscale frame
		faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(150, 150))
		
		# Recognize and label the faces
		for (x, y, w, h) in faces:
			# Recognize the face using the trained model
			label, confidence = recognizer.predict(gray[y:y + h, x:x + w])
			print(confidence)
			if confidence > 50:
				# Display the recognized label and confidence level
				cv2.putText(frame, label_name[label], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
	
				# Draw a rectangle around the face
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			else:
				print('Unrecognized')

		# Display the frame with face recognition
		cv2.imshow('Recognize Faces', frame)

		# Break the loop if the 'q' key is pressed
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# Release the camera and close windows
	cap.release()
	cv2.destroyAllWindows()


recognize_faces(Recognizer, label)