import numpy as np
import matplotlib.pyplot as plt


from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical

print("Loading MNIST dataset...")
(X_train, y_train), (X_test, y_test) = mnist.load_data()


X_train = X_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0  # Normalise 0→1
X_test  = X_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0


y_train_cat = to_categorical(y_train, 10)
y_test_cat  = to_categorical(y_test, 10)

print(f"Training samples : {X_train.shape[0]}")
print(f"Test samples     : {X_test.shape[0]}")


model = Sequential([
    
    Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1),
           name='Conv_Block1'),
    MaxPooling2D(pool_size=(2, 2), name='MaxPool1'),

   
    Conv2D(64, kernel_size=(3, 3), activation='relu', name='Conv_Block2'),
    MaxPooling2D(pool_size=(2, 2), name='MaxPool2'),

    
    Flatten(name='Flatten'),
    Dense(128, activation='relu', name='FullyConnected'),
    Dropout(0.3, name='Dropout'),         
    Dense(10, activation='softmax', name='Output_10digits')  
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print("\n========== Model Architecture ==========")
model.summary()


print("\nTraining model...")
history = model.fit(
    X_train, y_train_cat,
    epochs=5,                  
    batch_size=128,
    validation_split=0.1,      
    verbose=1
)


test_loss, test_acc = model.evaluate(X_test, y_test_cat, verbose=0)
print(f"\n========== Test Results ==========")
print(f"Test Accuracy : {test_acc * 100:.2f}%")
print(f"Test Loss     : {test_loss:.4f}")


predictions = model.predict(X_test, verbose=0)
predicted_labels = np.argmax(predictions, axis=1)


fig, axes = plt.subplots(3, 5, figsize=(14, 8))
fig.suptitle(f"MNIST Digit Classifier  |  Test Accuracy: {test_acc*100:.2f}%",
             fontsize=13, fontweight='bold')

for i, ax in enumerate(axes.flat):
    ax.imshow(X_test[i].reshape(28, 28), cmap='gray')
    pred  = predicted_labels[i]
    actual = y_test[i]
    colour = 'green' if pred == actual else 'red'
    ax.set_title(f"Pred: {pred}  |  True: {actual}",
                 color=colour, fontsize=9)
    ax.axis('off')

plt.tight_layout()
plt.savefig("mnist_predictions.png", dpi=120)
plt.show()
print("Prediction chart saved as 'mnist_predictions.png'")


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle("Training History", fontsize=13, fontweight='bold')

ax1.plot(history.history['accuracy'],     label='Train Accuracy')
ax1.plot(history.history['val_accuracy'], label='Val Accuracy')
ax1.set_title("Accuracy per Epoch")
ax1.set_xlabel("Epoch"); ax1.set_ylabel("Accuracy")
ax1.legend(); ax1.grid(True)

ax2.plot(history.history['loss'],     label='Train Loss')
ax2.plot(history.history['val_loss'], label='Val Loss')
ax2.set_title("Loss per Epoch")
ax2.set_xlabel("Epoch"); ax2.set_ylabel("Loss")
ax2.legend(); ax2.grid(True)

plt.tight_layout()
plt.savefig("mnist_training_history.png", dpi=120)
plt.show()
print("Training history saved as 'mnist_training_history.png'")


from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, predicted_labels)
fig, ax = plt.subplots(figsize=(9, 7))
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                               display_labels=list(range(10)))
disp.plot(cmap='Blues', ax=ax, colorbar=False)
ax.set_title("Confusion Matrix – Digit Classification (0–9)",
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig("mnist_confusion_matrix.png", dpi=120)
plt.show()
print("Confusion matrix saved as 'mnist_confusion_matrix.png'")


model.save("mnist_digit_classifier.h5")
print("\nModel saved as 'mnist_digit_classifier.h5'")
print("\nDone! The model can now distinguish digits 0–9.")
