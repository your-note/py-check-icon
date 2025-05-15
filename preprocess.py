import os
import cv2
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

def load_images_from_folders(base_dir, image_size=(78, 78)):
    data = []
    labels = []
    for label in os.listdir(base_dir):
        folder = os.path.join(base_dir, label)
        if not os.path.isdir(folder):
            continue
        for fname in os.listdir(folder):
            path = os.path.join(folder, fname)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img = cv2.resize(img, image_size)
            data.append(img.flatten())  # ベクトル化
            labels.append(label)
    return np.array(data), np.array(labels)

# 画像読み込みと前処理
X, y = load_images_from_folders("dataset")
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)  # 文字ラベルを数値に変換

# 訓練データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# SVM モデルの学習
model = SVC(kernel='linear')  # または 'rbf'
model.fit(X_train, y_train)

# 精度確認（オプション）
accuracy = model.score(X_test, y_test)
print(f"テスト精度: {accuracy:.4f}")

# モデルとラベル変換器を保存
joblib.dump(model, "svm_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
