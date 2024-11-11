# -*- coding: utf-8 -*-
"""TrainVON.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OGHa9wjKEz_6cCx_HOmOhA3lO6F58NW8
"""

from google.colab import drive
drive.mount('/content/drive')

"""##Create Data Test

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def add_noise(in_path, out_path, mean=0, std_dev=10 ):


  # Đọc dữ liệu từ file HDF5 bằng pandas
  df = pd.read_hdf(in_path, key='df')

  # Giả sử 'x_data' là thời gian và 'y_data' là các tín hiệu
  # Chuyển dữ liệu từ DataFrame sang numpy array
  x_data = df['x_data'].values
  y_data = df['y_data'].values
  print(len(x_data))


  # Tạo Gaussian noise
  noise = np.random.normal(mean, std_dev, size=y_data.shape)

  # Cộng noise vào dữ liệu
  y_data_noisy = y_data + noise

  # Tạo DataFrame mới với dữ liệu đã thêm noise
  df_noisy = pd.DataFrame({'x_data': x_data, 'y_data': y_data_noisy})



  # Lưu DataFrame với dữ liệu đã thêm noise vào file HDF5 mới
  df_noisy.to_hdf(out_path, key='df', mode='w')

  print(f'Dữ liệu đã được lưu vào file {out_path}')
add_noise(in_path='/content/drive/MyDrive/Von/adjust_0_file10_chunk_0.h5', out_path="/content/adjust_0_file10_chunk_0_noisy.h5", std_dev=10)
add_noise(in_path='/content/drive/MyDrive/Von/adjust_1_file10_chunk_0.h5', out_path="/content/adjust_1_file10_chunk_0_noisy.h5", std_dev=10)
add_noise(in_path='/content/drive/MyDrive/Von/adjust_2_file10_chunk_0.h5', out_path="/content/adjust_2_file10_chunk_0_noisy.h5", std_dev=10)
add_noise(in_path='/content/drive/MyDrive/Von/adjust_3_file10_chunk_0.h5', out_path="/content/adjust_3_file10_chunk_0_noisy.h5", std_dev=10)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt



def filter_noise(path):
  # Đọc dữ liệu từ file HDF5
  df_noisy = pd.read_hdf(path, key='df')

  # Chuyển dữ liệu từ DataFrame sang numpy array
  x_data = df_noisy['x_data'][:1600000].values
  y_data_noisy = df_noisy['y_data'][:1600000].values

  # Áp dụng bộ lọc thông thấp (Low-pass Filter) để khử nhiễu
  def low_pass_filter(data, cutoff_freq, fs, order=4):
      nyquist = 0.5 * fs
      normal_cutoff = cutoff_freq / nyquist
      b, a = butter(order, normal_cutoff, btype='low', analog=False)
      filtered_data = filtfilt(b, a, data)
      return filtered_data

  # Tần số mẫu (sample rate)
  fs = 1 / np.mean(np.diff(x_data))
  cutoff_freq = 0.1 * fs  # Tần số cắt (có thể điều chỉnh tùy thuộc vào dữ liệu của bạn)

  # Lọc dữ liệu nhiễu
  y_data_filtered = low_pass_filter(y_data_noisy, cutoff_freq, fs)

  # Hiển thị kết quả
  plt.figure(figsize=(10, 3))
  plt.plot(x_data, y_data_noisy, label='Noisy Data', linestyle='--')
  plt.plot(x_data, y_data_filtered, label='Filtered Data', linestyle='-.')
  plt.xlabel('X Data')
  plt.ylabel('Y Data')
  plt.title('Plot of Noisy Data and Filtered Data')
  plt.legend()
  plt.grid(True)
  plt.show()

filter_noise("/content/adjust_0_file10_chunk_0_noisy.h5")
filter_noise("/content/adjust_1_file10_chunk_0_noisy.h5")
filter_noise("/content/adjust_2_file10_chunk_0_noisy.h5")
filter_noise("/content/adjust_3_file10_chunk_0_noisy.h5")

def moving_average_filter(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def filter_noise_ma(path_file):
    # Đọc dữ liệu từ file HDF5
    df_noisy = pd.read_hdf(path_file, key='df')

    # Chuyển dữ liệu từ DataFrame sang numpy array
    x_data = df_noisy['x_data'][:1600000].values
    y_data_noisy = df_noisy['y_data'][:1600000].values

    # Áp dụng bộ lọc trung bình
    window_size = 50  # Kích thước của cửa sổ (có thể điều chỉnh)
    y_data_filtered_ma = moving_average_filter(y_data_noisy, window_size)

    # Hiển thị kết quả
    plt.figure(figsize=(10, 3))
    plt.plot(x_data[:len(y_data_filtered_ma)], y_data_filtered_ma, label='Filtered Data (Moving Average)', linestyle='-.')
    plt.xlabel('X Data')
    plt.ylabel('Y Data')
    plt.title('Plot of Noisy Data and Filtered Data using Moving Average')
    plt.legend()
    plt.grid(True)
    plt.show()

# Gọi hàm với đường dẫn tệp
filter_noise_ma(path_file="/content/adjust_0_file10_chunk_0_noisy.h5")
filter_noise_ma(path_file="/content/adjust_1_file10_chunk_0_noisy.h5")
filter_noise_ma(path_file="/content/adjust_2_file10_chunk_0_noisy.h5")
filter_noise_ma(path_file="/content/adjust_3_file10_chunk_0_noisy.h5")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import os

def filter_noise(path):
    # Đọc dữ liệu từ file HDF5
    df_noisy = pd.read_hdf(path, key='df')

    # Chuyển dữ liệu từ DataFrame sang numpy array
    x_data = df_noisy['x_data'][:1600000].values
    y_data_noisy = df_noisy['y_data'][:1600000].values

    # Áp dụng bộ lọc thông thấp (Low-pass Filter) để khử nhiễu
    def low_pass_filter(data, cutoff_freq, fs, order=4):
        nyquist = 0.5 * fs
        normal_cutoff = cutoff_freq / nyquist
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        filtered_data = filtfilt(b, a, data)
        return filtered_data

    # Tần số mẫu (sample rate)
    fs = 1 / np.mean(np.diff(x_data))
    cutoff_freq = 0.1 * fs  # Tần số cắt (có thể điều chỉnh tùy thuộc vào dữ liệu của bạn)

    # Lọc dữ liệu nhiễu
    y_data_filtered = low_pass_filter(y_data_noisy, cutoff_freq, fs)

    # Lưu dữ liệu nhiễu (Noisy Data)
    plt.figure(figsize=(10, 3))
    plt.plot(x_data, y_data_noisy, label='Noisy Data', linestyle='-', color='blue')
    plt.axis('off')
    noisy_image_path = os.path.splitext(path)[0] + '_noisy.png'
    plt.savefig(noisy_image_path, bbox_inches='tight', pad_inches=0)
    plt.close()

    # Lưu dữ liệu đã lọc (Filtered Data)
    plt.figure(figsize=(10, 3))
    plt.plot(x_data, y_data_filtered, label='Filtered Data', linestyle='-', color='green')
    plt.axis('off')
    filtered_image_path = os.path.splitext(path)[0] + '_filtered.png'
    plt.savefig(filtered_image_path, bbox_inches='tight', pad_inches=0)
    plt.close()

    print(f"Saved noisy image as {noisy_image_path}")
    print(f"Saved filtered image as {filtered_image_path}")

# Gọi hàm filter_noise cho các file
filter_noise("/content/adjust_0_file10_chunk_0_noisy.h5")
filter_noise("/content/adjust_1_file10_chunk_0_noisy.h5")
filter_noise("/content/adjust_2_file10_chunk_0_noisy.h5")
filter_noise("/content/adjust_3_file10_chunk_0_noisy.h5")

"""##SVM"""

import os
import torch
import numpy as np
import cv2
from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Đường dẫn tới hai thư mục chứa ảnh
image_dirs = ['/content/drive/MyDrive/VonImage', '/content/drive/MyDrive/VonImage1']

class CustomImageDataset(Dataset):
    def __init__(self, image_dirs, transform=None):
        self.image_paths = []
        self.labels = []
        self.transform = transform

        for image_dir in image_dirs:
            for image_name in os.listdir(image_dir):
                if image_name.startswith(('adjust_0', 'adjust_1', 'adjust_2', 'adjust_3')):
                    image_path = os.path.join(image_dir, image_name)
                    self.image_paths.append(image_path)

                    # Gán nhãn dựa trên tên file
                    if "adjust_0" in image_name:
                        self.labels.append(0)
                    elif "adjust_1" in image_name:
                        self.labels.append(1)
                    elif "adjust_2" in image_name:
                        self.labels.append(2)
                    elif "adjust_3" in image_name:
                        self.labels.append(3)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        label = self.labels[idx]
        image = Image.open(image_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, label

# Định nghĩa các biến đổi cho dữ liệu hình ảnh
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
])

# Tạo dataset và dataloader
dataset = CustomImageDataset(image_dirs, transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=False)

# Chuyển đổi dữ liệu từ DataLoader thành các mảng numpy để sử dụng với SVM
X = []
y = []

for images, labels in dataloader:
    images = images.numpy().reshape(images.size(0), -1)  # Flatten images
    X.extend(images)
    y.extend(labels.numpy())

X = np.array(X)
y = np.array(y)

# Áp dụng PCA để giảm chiều dữ liệu
pca = PCA(n_components=100)
X_pca = pca.fit_transform(X)

# Chia dữ liệu thành tập train và test
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)

# Train mô hình SVM
svm = SVC(kernel='linear', random_state=42)
svm.fit(X_train, y_train)

# Dự đoán trên tập test
y_pred = svm.predict(X_test)

# Tính độ chính xác
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Tính recall, f1 score cho từng lớp
recall = recall_score(y_test, y_pred, average=None)
f1 = f1_score(y_test, y_pred, average=None)
print(f'Recall per class: {recall}')
print(f'F1 score per class: {f1}')

# In kết quả chi tiết
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# In confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

import joblib

# Lưu mô hình SVM
model_filename = '/content/drive/MyDrive/VonResult/svm_model.pkl'
joblib.dump(svm, model_filename)
pca_filename = '/content/drive/MyDrive/VonResult/pca_model.pkl'
joblib.dump(pca, pca_filename)

print(f'Model saved to {model_filename}')

import joblib
import numpy as np
from PIL import Image
import torch
from torchvision import transforms

# Định nghĩa các biến đổi cho dữ liệu hình ảnh
transform = transforms.Compose([
    transforms.Resize((64, 64)),  # Đảm bảo kích thước hình ảnh giống như khi huấn luyện
    transforms.ToTensor(),        # Chuyển đổi hình ảnh thành tensor
])
pca_loaded = joblib.load('/content/drive/MyDrive/VonResult/pca_model.pkl')
def predict_image(image_path, model, transform):
    # Tải ảnh và chuyển đổi thành định dạng phù hợp
    image = Image.open(image_path).convert("RGB")
    image = transform(image)
    image = image.unsqueeze(0)  # Thêm batch dimension

    # Chuyển đổi tensor thành numpy array cho SVM
    image_np = image.numpy().reshape(1, -1)

    # Tiền xử lý dữ liệu giống như khi huấn luyện
    image_pca = pca_loaded.transform(image_np)

    # Dự đoán với mô hình SVM
    prediction = model.predict(image_pca)
    return prediction[0]

# Đường dẫn đến ảnh PNG
image_path = '/content/adjust_1_file10_chunk_0_noisy_filtered.png'
# Tải mô hình SVM
model_filename = '/content/drive/MyDrive/VonResult/svm_model.pkl'
svm_loaded = joblib.load(model_filename)
# Dự đoán
prediction = predict_image(image_path, svm_loaded, transform)
print(f'Predicted label: {prediction}')

"""##KNN"""

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Định nghĩa các thư mục chứa ảnh
folders = ['/content/drive/MyDrive/VonImage', '/content/drive/MyDrive/VonImage1']

# Danh sách để lưu dữ liệu ảnh và nhãn
images = []
labels = []

# Đọc ảnh từ các thư mục
for folder in folders:
    for filename in os.listdir(folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Thay đổi tùy theo định dạng ảnh
            img_path = os.path.join(folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Đọc ảnh thành ảnh xám
            img = cv2.resize(img, (64, 64))  # Thay đổi kích thước ảnh nếu cần
            images.append(img.flatten())  # Chuyển đổi ảnh thành vector 1D

            # Gán nhãn từ tên file
            if "adjust_0" in filename:
                label = 0
            elif "adjust_1" in filename:
                label = 1
            elif "adjust_2" in filename:
                label = 2
            elif "adjust_3" in filename:
                label = 3
            else:
                continue  # Bỏ qua các file không thuộc dạng này

            labels.append(label)

# Chuyển đổi dữ liệu thành numpy array
X = np.array(images)
y = np.array(labels)

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Tạo và huấn luyện mô hình KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Dự đoán và đánh giá mô hình
y_pred = knn.predict(X_test)
print(classification_report(y_test, y_pred, target_names=['adjust_0', 'adjust_1', 'adjust_2', 'adjust_3']))

# Tạo confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Vẽ confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['adjust_0', 'adjust_1', 'adjust_2', 'adjust_3'],
            yticklabels=['adjust_0', 'adjust_1', 'adjust_2', 'adjust_3'])
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# Đọc ảnh PNG mới
def preprocess_image(image_path, target_size=(64, 64)):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Đọc ảnh thành ảnh xám
    img = cv2.resize(img, target_size)  # Thay đổi kích thước ảnh
    img_flatten = img.flatten()  # Chuyển đổi ảnh thành vector 1D
    return img_flatten

# Đường dẫn đến ảnh PNG mới
new_image_path = '/content/adjust_0_file10_chunk_0_noisy_filtered.png'

# Tiền xử lý ảnh mới
new_image = preprocess_image(new_image_path)

# Dự đoán nhãn của ảnh mới
def predict_image(model, image_vector):
    # Dự đoán nhãn
    prediction = model.predict([image_vector])
    return prediction[0]



# Dự đoán nhãn của ảnh mới
predicted_label = predict_image(knn, new_image)

# Hiển thị kết quả
print(f'Nhãn dự đoán của ảnh là: {predicted_label}')

"""##Deep Learning"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms
import os
from PIL import Image

class CustomImageDataset(Dataset):
    def __init__(self, img_dirs, transform=None):
        self.img_dirs = img_dirs
        self.transform = transform
        self.img_labels = self._load_images()

    def _load_images(self):
        img_labels = []
        for img_dir in self.img_dirs:
            img_labels.extend([(file, self._get_label(file)) for file in os.listdir(img_dir) if file.endswith(('.png', '.jpg', '.jpeg'))])
        return img_labels

    def _get_label(self, filename):
        if 'adjust_0' in filename:
            return 0
        elif 'adjust_1' in filename:
            return 1
        elif 'adjust_2' in filename:
            return 2
        elif 'adjust_3' in filename:
            return 3

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dirs[0], self.img_labels[idx][0])
        if not os.path.exists(img_path):  # Check if the file exists in the first directory
            img_path = os.path.join(self.img_dirs[1], self.img_labels[idx][0])  # Fallback to the second directory
        image = Image.open(img_path).convert("RGB")
        label = self.img_labels[idx][1]

        if self.transform:
            image = self.transform(image)

        return image, label

# Define your image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Paths to the image directories
img_dirs = ['/content/drive/MyDrive/VonImage', '/content/drive/MyDrive/VonImage1']

# Create the dataset
dataset = CustomImageDataset(img_dirs=img_dirs, transform=transform)

# Split the dataset into training and validation sets
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

# Create data loaders
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Define the model
model = models.resnet18(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 4)  # 4 classes: 0, 1, 2, 3
model = model.to('cuda' if torch.cuda.is_available() else 'cpu')

# Define the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

from tqdm import tqdm
num_epochs = 10
device = 'cuda' if torch.cuda.is_available() else 'cpu'
best_val_loss = float('inf')
best_model_path = '/content/drive/MyDrive/VonResult/best_model_weights.pth'

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}", unit="batch")

    for images, labels in progress_bar:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)
        progress_bar.set_postfix({'Loss': running_loss / len(train_loader.dataset)})

    epoch_loss = running_loss / len(train_loader.dataset)
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}")

    # Validation
    model.eval()
    val_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    val_loss /= len(val_loader.dataset)
    print(f'Validation Loss: {val_loss:.4f}')
    print(f'Validation Accuracy: {100 * correct / total:.2f}%')

    # Save the model if the validation loss is the lowest
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        torch.save(model.state_dict(), best_model_path)
        print(f'Saved Best Model with Validation Loss: {best_val_loss:.4f}')

import matplotlib.pyplot as plt
import numpy as np
class_names = ['adjust_0', 'adjust_1', 'adjust_2', 'adjust_3']
model = models.resnet18(pretrained=False)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 4)  # 3 classes: 0, 1, 2, 3
model.load_state_dict(torch.load('/content/drive/MyDrive/VonResult/best_model_weights.pth'))
model = model.to('cuda' if torch.cuda.is_available() else 'cpu')
model.eval()  # Set the model to evaluation mode
def imshow(image, ax=None, title=None):
    """Imshow for Tensor."""
    if ax is None:
        fig, ax = plt.subplots()
    image = image.numpy().transpose((1, 2, 0))
    mean = torch.tensor([0.485, 0.456, 0.406])
    std = torch.tensor([0.229, 0.224, 0.225])
    image = std * image + mean
    image = np.clip(image, 0, 1)
    ax.imshow(image)
    if title:
        ax.set_title(title)
    ax.axis('off')
    return ax

def display_predictions(model, data_loader, num_images=5):
    images_so_far = 0
    fig = plt.figure(figsize=(15, 10))

    for i, (inputs, labels) in enumerate(data_loader):
        inputs = inputs.to('cuda' if torch.cuda.is_available() else 'cpu')
        labels = labels.to('cuda' if torch.cuda.is_available() else 'cpu')

        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)

        for j in range(inputs.size()[0]):
            images_so_far += 1
            ax = plt.subplot(num_images//5, 5, images_so_far)
            ax.axis('off')
            imshow(inputs.cpu().data[j], ax=ax, title=f'Pred: {class_names[preds[j]]}\nActual: {class_names[labels[j]]}')
            if images_so_far == num_images:
                return

# Test with validation set
display_predictions(model, val_loader, num_images=10)

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, f1_score
import seaborn as sns
from torchvision import models
import pandas as pd

class_names = ['adjust_0', 'adjust_1', 'adjust_2', 'adjust_3']
model = models.resnet18(pretrained=False)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 4)  # 4 classes: 0, 1, 2, 3
model.load_state_dict(torch.load('/content/drive/MyDrive/VonResult/best_model_weights.pth'))
model = model.to('cuda' if torch.cuda.is_available() else 'cpu')
model.eval()  # Set the model to evaluation mode

def imshow(image, ax=None, title=None):
    """Imshow for Tensor."""
    if ax is None:
        fig, ax = plt.subplots()
    image = image.numpy().transpose((1, 2, 0))
    mean = torch.tensor([0.485, 0.456, 0.406])
    std = torch.tensor([0.229, 0.224, 0.225])
    image = std * image + mean
    image = np.clip(image, 0, 1)
    ax.imshow(image)
    if title:
        ax.set_title(title)
    ax.axis('off')
    return ax

def display_predictions(model, data_loader, num_images_to_show=10, total_images=150):
    images_so_far = 0
    all_preds = []
    all_labels = []
    fig = plt.figure(figsize=(15, 10))

    for i, (inputs, labels) in enumerate(data_loader):
        inputs = inputs.to('cuda' if torch.cuda.is_available() else 'cpu')
        labels = labels.to('cuda' if torch.cuda.is_available() else 'cpu')

        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)

        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

        # Display only the first 'num_images_to_show' images
        if images_so_far < num_images_to_show:
            for j in range(inputs.size()[0]):
                if images_so_far >= num_images_to_show:
                    break
                images_so_far += 1
                ax = plt.subplot(num_images_to_show // 5, 5, images_so_far)
                ax.axis('off')
                imshow(inputs.cpu().data[j], ax=ax, title=f'Pred: {class_names[preds[j]]}\nActual: {class_names[labels[j]]}')

        if images_so_far >= num_images_to_show:
            break

    # Calculate metrics
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    acc = accuracy_score(all_labels, all_preds)
    rec = recall_score(all_labels, all_preds, average='weighted')
    f1 = f1_score(all_labels, all_preds, average='weighted')
    cm = confusion_matrix(all_labels, all_preds)

    # Display metrics
    print(f'Accuracy: {acc:.4f}')
    print(f'Recall: {rec:.4f}')
    print(f'F1 Score: {f1:.4f}')

    # Create a DataFrame for the metrics
    metrics_df = pd.DataFrame({
        'Metric': ['Accuracy', 'Recall', 'F1 Score'],
        'Score': [acc, rec, f1]
    })

    # Display the metrics table
    print("\nMetrics Table:")
    print(metrics_df)

    # Plot confusion matrix
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.show()

# Test with validation set, considering only a subset of images
display_predictions(model, val_loader, num_images_to_show=10, total_images=150)

##Test ảnh
from PIL import Image
import torch
import torchvision.transforms as transforms
model = models.resnet18(pretrained=False)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 4)  # 3 classes: 0, 1, 2, 3
model.load_state_dict(torch.load('/content/drive/MyDrive/VonResult/best_model_weights.pth'))
model = model.to('cuda' if torch.cuda.is_available() else 'cpu')
model.eval()  # Set the model to evaluation mode



# Define the image transformations (same as during training)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Load the image
image_path = '/content/adjust_1_file10_chunk_0_noisy_filtered.png'  # Replace with your image path
image = Image.open(image_path).convert("RGB")

# Apply the transformations to the image
image = transform(image)
image = image.unsqueeze(0)  # Add a batch dimension (1, C, H, W)

# Move the image to the same device as the model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
image = image.to(device)

# Make the prediction
with torch.no_grad():
    output = model(image)
    _, predicted = torch.max(output, 1)

# Convert the predicted label to a class
class_labels = {0: 'adjust_0', 1: 'adjust_1', 2: 'adjust_2', 3: 'adjust_3'}
predicted_label = class_labels[predicted.item()]

print(f"The predicted class is: {predicted_label}")
