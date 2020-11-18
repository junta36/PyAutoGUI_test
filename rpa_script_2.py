import pyautogui as pag
import pyocr
from PIL import Image
import sys
import subprocess
 
import pyperclip
import os
import time

# 閉じるボタン座標（アクロバット用）
# CLOSE_BUTTON_X = 14
# CLOSE_BUTTON_Y = 34

# # pdfアプリの実行ファイルパス(アクロバット)
# # acr_path = '/Applications/Adobe\ Acrobat\ Reader\ DC.app/Contents/MacOS/AdobeReader'



# 閉じるボタン座標（プレビュー用）
CLOSE_BUTTON_X = 18
CLOSE_BUTTON_Y = 40

# pdfアプリの実行ファイルパス(プレビュー)
acr_path = '/System/Applications/Preview.app/Contents/MacOS/Preview'

# 表示したいpdfのファイルパス
todokede_path = '/Users/junmac/Python/YAJIROBE/Udemy/workspace/lec_rpa/todokede_data/'
# todokede_path = '/Users/junmac/Desktop/todokede_data/'

# フォルダ内の複数のファイルを開く
todokede_list = os.listdir(todokede_path)
# print(todokede_list)

X = 770
Y = 640
NAME_W = 200
NAME_H = 25
# WAIT_TIME = 5#[sec]


# 画像の検出用
def detect_name_posi():
    pag.moveTo(1, 1) # マウスが検出画像の上にあり認識が出来ない可能性を避けるため、マウスを端に移動させる
    for count in range(5): # 上手くpdfが開けなかった場合も想定して、繰り返し5回チャレンジするようにする
        try:
            img_loc = pag.locateOnScreen('simei.png')
            break
        except Exception:
            time.sleep(1)
    return img_loc

def get_name_img(X, Y, NAME_W, NAME_H):
    name_img = pag.screenshot('temp.png', region=(X, Y, NAME_W, NAME_H))

def run_ocr(tool, name_img):
    result = tool.image_to_string(name_img, lang='jpn')
    result = result.replace(' ', '')
    print(result)
    return result

# Pythonファイルが開いたら先にメイン関数が呼ばれるようにする
if __name__ == '__main__':
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]
    # for文を使って複数ファイルを開いて閉じる処理
    # enumerate:インデックス番号と、リストの要素をセットで取得できる
    for idx, file in enumerate(todokede_list):
        # pdfを処理が終わったかどうかを確認してから次のPDFを開く
        # if idx != 0:
        #     start = time.time() # 今の現在時刻取得
        #     elapsed_time = 0 # 初期値
        #     while pdf_pro.poll() == None:
        #         elapsed_time = time.time() -start
        #         if elapsed_time > WAIT_TIME:
        #             print('STOP PORCESS')
        #             sys.exit(1)

        print('open :', file)
        # ファイルを１つずつ開いて
        pdf_pro = subprocess.Popen([acr_path, todokede_path+file])
        time.sleep(1)

        # 位置を検出して
        img_loc = detect_name_posi()
        print(img_loc)
        img_loc = pag.locateOnScreen('simei3.png')
        print(img_loc)

        name_img = get_name_img(X, Y, NAME_W, NAME_H)
        result = run_ocr(tool, name_img)

        # ファイルを閉じる
        pag.click(CLOSE_BUTTON_X, CLOSE_BUTTON_Y)
        time.sleep(1)

# 1つのファイルを開くとき［アプリのファイルパス、ファイルのパス、ファイル名］
# pdf_pro =subprocess.Popen([acr_path, todokede_path+'住所変更届_001.pdf'])

# # 5秒後に、座標の部分を左クリックする
# time.sleep(5)
# pag.click(CLOSE_BUTTON_X, CLOSE_BUTTON_Y)

# 閉じるボタンの位置を調べる
# print(pag.position())



# NAME_W = 206
# WAIT_TIME = 5#[sec]

# def detect_name_posi():
#     pag.moveTo(1, 1)
#     for count in range(50):
#         try:
#             x, y, w, h = pag.locateOnScreen('simei.png')
#             break
#         except ImageNotFoundException:
#             time.sleep(1)
#     return x, y, w, h

# def get_name_img(x, y, w, h, NAME_W):
#     start_x = x + w
#     start_y = y
#     name_img = pag.screenshot(region=(start_x, start_y, NAME_W, h))
#     return name_img

# def run_ocr(tool, name_img):
#     result = tool.image_to_string(name_img, lang='jpn')
#     result = result.replace(' ', '')
#     print(result)
#     return result

# def copy_name_data(name_list):
#     pag.moveTo(923, 306)
#     pag.click()

#     for name in name_list:
#         pyperclip.copy(name)
#         pag.hotkey('ctrl', 'v')
#         pag.press('enter')
#         pag.press('enter')

# if __name__ == '__main__':
#     tools = pyocr.get_available_tools()
#     if len(tools) == 0:
#         print("No OCR tool found")
#         sys.exit(1)
#     tool = tools[0]

#     name_list = []

# for文を使って複数ファイルを開いて閉じる処理
#     for idx, file in enumerate(todokede_list):
#         if idx != 0:
#             start = time.time()
#             elapsed_time = 0
#             while pdf_pro.poll() == None:
#                 elapsed_time = time.time() - start
#                 if elapsed_time > WAIT_TIME:
#                     print('STOP PROCESS')
#                     sys.exit(1)

#         print('open :', file)
#         pdf_pro = subprocess.Popen([acr_path, todokede_path+file])
#         time.sleep(1)

#         x, y, w, h = detect_name_posi()

#         name_img = get_name_img(x, y, w, h, NAME_W)

#         result = run_ocr(tool, name_img)
#         name_list.append(result)

#         pag.click(CLOSE_BUTTON_X, CLOSE_BUTTON_Y)

#     copy_name_data(name_list)

#     pag.alert('終了しました')
