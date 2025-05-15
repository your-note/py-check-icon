import cv2
import joblib
import mss
import time
import numpy as np
import os
import psutil
from playsound import playsound
import win32gui

STREET_FIGHTER_6 = "Street Fighter 6"

width_ratio = 78/2560
height_ratio = 78/1440
left_ratio = 1240/2560
top_ratio = 648/1440

TARGET_PROCESS = "StreetFighter6.exe"  # チェック対象の実行ファイル名

def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        #print (proc.info['name'])
        if proc.info['name'] == process_name:
            return True
    return False


# モデルとラベルを読み込み
model = joblib.load("svm_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")


def predict_image(img):
    # 入力画像の前処理
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (78, 78))
    img_flat = img.flatten().reshape(1, -1)

    # 推論
    pred_encoded = model.predict(img_flat)
    pred_label = label_encoder.inverse_transform(pred_encoded)

    return pred_label[0]

def get_window_rect(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        return None
    rect = win32gui.GetWindowRect(hwnd)
    # rect: (left, top, right, bottom)
    return {"left": rect[0], "top": rect[1], "width": rect[2] - rect[0], "height": rect[3] - rect[1]}

def save_screen_every_second():
    with mss.mss() as sct:
        while True:
            if not is_process_running(TARGET_PROCESS):
                #print(f"{TARGET_PROCESS} が実行されていません。")
                time.sleep(1)
                continue
            win_rect = get_window_rect(STREET_FIGHTER_6)
            if win_rect is None:
                #print("ウィンドウが見つかりません")
                time.sleep(1)
                continue
            monitor = {
                "left": win_rect["left"],
                "top": win_rect["top"],
                "width": win_rect["width"],
                "height": win_rect["height"]
            }
            sct_img = sct.grab(monitor)
            img = np.array(sct_img)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            # 縦横を得る
            org_height, orig_width, _ = img.shape
            width = int(orig_width * width_ratio)
            height = int(org_height * height_ratio)
            left = int(orig_width * left_ratio)
            top = int(org_height * top_ratio)
            # 指定領域を切り出し
            cropped = img[top:top+height, left:left+width]
            # 画像保存せずに推論
            result = predict_image(cropped)
            # 予測結果に応じて音声再生
            if result == "ok":
                playsound("ok.mp3")
            elif result == "warn":
                playsound("ng.mp3")
            time.sleep(1/2)


if __name__ == "__main__":
    save_screen_every_second()
