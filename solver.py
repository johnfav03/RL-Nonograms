import json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
import random

# Load data from JSON files
def load_data(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data['data']

# Process data into numpy arrays
def process_data(data):
    htmaps = []
    images = []

    for testcase in data:
        htmap = np.array(testcase['htmap'])
        image = np.array(testcase['image'])

        htmaps.append(htmap)
        images.append(image)

    return np.array(htmaps), np.array(images)

# Load training and testing data
train_data = load_data('training.json')
test_data = load_data('testing.json')

# Process data
train_htmaps, train_images = process_data(train_data)
test_htmaps, test_images = process_data(test_data)

# Expand dimensions to add a channel for the CNN input
train_htmaps = np.expand_dims(train_htmaps, axis=-1)
test_htmaps = np.expand_dims(test_htmaps, axis=-1)

# Define the CNN architecture
def create_cnn_model():
    inpMap = layers.Input(shape=(10, 10, 1))
    inpPos = layers.Input(shape=(2,))
    x = layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(10, 10, 1))(inpMap)
    x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = layers.Flatten()(x)
    x = models.Model(inputs=inpMap, outputs=x)
    cmb = layers.concatenate([x.output, inpPos], axis=1)
    y = layers.Dense(128, activation='relu')(cmb)
    y = layers.Dense(64, activation='relu')(y)
    y = layers.Dense(1, activation='sigmoid')(y)
    model = models.Model(inputs=[x.input, inpPos], outputs=y)
    return model

# Create the CNN model
cnn_model = create_cnn_model()

# Compile the model
optimizer = optimizers.Adam(learning_rate=0.01)
cnn_model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

opts = [[i, j] for j in len(10) for i in len(10)]
random.shuffle(opts)

num_epochs = 50
batch_size = 1

for epoch in range(num_epochs):
    print(f"Epoch {epoch + 1}/{num_epochs}")
    
    # Shuffle the indices to randomly select rows and columns
    indices = np.random.permutation(len(train_htmaps))
    
    for i in indices:
        # Randomly select row and column
        row = np.random.randint(0, 10)
        col = np.random.randint(0, 10)
        
        # Get the corresponding input and target
        input_data = [train_htmaps[i], np.array([[row, col]])]
        target = train_images[i, row, col]  # Assuming train_images is a binary array
        
        # Train on the current example
        loss, accuracy = cnn_model.train_on_batch(input_data, np.array([target]))
        
        # Print training metrics
        print(f"Batch - Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")

# # Train the CNN model
# cnn_model.fit(train_htmaps, train_images, epochs=50, batch_size=1)

# # Evaluate the CNN model on the test set
# loss, accuracy = cnn_model.evaluate(test_htmaps, test_images)
# print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

# # Make predictions using the CNN model on new data
# new_data = np.random.rand(5, 10, 10)  # Replace this with your new data
# new_data = np.expand_dims(new_data, axis=-1)
# cnn_predictions = cnn_model.predict(new_data)
# cnn_predictions_binary = np.where(cnn_predictions >= 0.5, 1, 0)

# print("CNN Predictions:")
# print(cnn_predictions_binary)