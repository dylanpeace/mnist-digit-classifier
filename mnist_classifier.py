import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers



# Load MNIST directly from Keras 
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

print("=" * 50)
print("         MNIST Dataset Loaded Successfully")
print("=" * 50)
print(f"Training images : {x_train.shape}")   # (60000, 28, 28)
print(f"Training labels : {y_train.shape}")   # (60000,)
print(f"Test images     : {x_test.shape}")    # (10000, 28, 28)
print(f"Test labels     : {y_test.shape}")    # (10000,)
print(f"Classes         : {np.unique(y_train)}")  # [0 1 2 3 4 5 6 7 8 9]
print()

# Visualise Sample Images

plt.figure(figsize=(12, 3))
for i in range(10):
    plt.subplot(1, 10, i + 1)
    plt.imshow(x_train[i], cmap='gray')
    plt.title(f"Label: {y_train[i]}", fontsize=8)
    plt.axis('off')
plt.suptitle("Sample MNIST Images (one per digit)", fontsize=12)
plt.tight_layout()
plt.savefig("sample_images.png", dpi=100)
plt.show()
print("Sample images saved to 'sample_images.png'")
print()

# Preprocess the Data

# Normalise pixel values from [0, 255] to [0.0, 1.0]
x_train = x_train.astype("float32") / 255.0
x_test  = x_test.astype("float32")  / 255.0

# Flatten 28×28 images into 784-dimensional vectors
x_train_flat = x_train.reshape(-1, 28 * 28)
x_test_flat  = x_test.reshape(-1, 28 * 28)

print("Data preprocessed:")
print(f"  - Pixel values normalised to [0, 1]")
print(f"  - Images flattened: {x_train_flat.shape[1]} features per image")
print()

#  Build the Neural Network Model

model = keras.Sequential([
    layers.Input(shape=(784,)),               # Input layer  – 784 neurons
    layers.Dense(256, activation='relu'),     # Hidden layer – 256 neurons
    layers.Dropout(0.2),                      # Dropout for regularisation
    layers.Dense(128, activation='relu'),     # Hidden layer – 128 neurons
    layers.Dropout(0.2),
    layers.Dense(10, activation='softmax')    # Output layer – 10 classes (0–9)
], name="MNIST_Classifier")

model.summary()
print()

# Compile the Model

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',   # Integer labels (not one-hot)
    metrics=['accuracy']
)


#Train the Model

print("Training the model...")
history = model.fit(
    x_train_flat, y_train,
    epochs=10,
    batch_size=128,
    validation_split=0.1,   # Reserve 10 % of training data for validation
    verbose=1
)
print()
#Evaluate on Test Data

test_loss, test_accuracy = model.evaluate(x_test_flat, y_test, verbose=0)
print("=" * 50)
print("           Evaluation on Test Set")
print("=" * 50)
print(f"Test Loss     : {test_loss:.4f}")
print(f"Test Accuracy : {test_accuracy * 100:.2f}%")
print()


# Plot Training History

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Accuracy
ax1.plot(history.history['accuracy'],     label='Train Accuracy')
ax1.plot(history.history['val_accuracy'], label='Val Accuracy')
ax1.set_title('Model Accuracy over Epochs')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.legend()
ax1.grid(True)

# Loss
ax2.plot(history.history['loss'],     label='Train Loss')
ax2.plot(history.history['val_loss'], label='Val Loss')
ax2.set_title('Model Loss over Epochs')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Loss')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig("training_history.png", dpi=100)
plt.show()
print("Training history saved to 'training_history.png'")
print()

#  Make Predictions & Visualise Results

predictions = model.predict(x_test_flat, verbose=0)
predicted_labels = np.argmax(predictions, axis=1)

# Show 10 test images with predictions
plt.figure(figsize=(14, 3))
for i in range(10):
    plt.subplot(1, 10, i + 1)
    plt.imshow(x_test[i], cmap='gray')
    color = 'green' if predicted_labels[i] == y_test[i] else 'red'
    plt.title(f"P:{predicted_labels[i]}\nA:{y_test[i]}", fontsize=7, color=color)
    plt.axis('off')
plt.suptitle("Predictions (P=Predicted, A=Actual) | Green=Correct, Red=Wrong", fontsize=10)
plt.tight_layout()
plt.savefig("predictions.png", dpi=100)
plt.show()
print("Predictions saved to 'predictions.png'")
print()

# Save the Trained Model

model.save("mnist_model.keras")
print("Trained model saved to 'mnist_model.keras'")
print()
print("Done! ✓")
