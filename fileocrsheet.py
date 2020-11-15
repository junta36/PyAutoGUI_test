from PIL import Image
import pyautogui as pag
import sys
import pyocr

import os # 複数ファイル開く用
import subprocess # ファイル1つずつ開く用
import time # sleep用
import pyperclip # クリップボード用



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
# todokede_path = '/Users/junmac/Python/YAJIROBE/Udemy/workspace/lec_rpa/todokede_data/'
todokede_path = '/Users/junmac/Desktop/todokede_data/'

# フォルダ内の複数のファイルを開く
todokede_list = os.listdir(todokede_path)
# print(todokede_list)


def copy_name_data(name_list):
    pag.moveTo(1350, 340)
    pag.click(clicks=2, interval=0.2)
    
    # pag.click(clicks=2, interval=0.2)

    # name_listから1つずつ名前を取り出し
    for name in name_list:
        # クリップボードにコピー
        pyperclip.copy(name) 
        pag.hotkey('command', 'v')
        pag.press('return')
        # スプレットシートは2回エンターしないと入力モードにならないため
        pag.press('return')


# Pythonファイルが開いたら先にメイン関数が呼ばれるようにする
if __name__ == '__main__':
    # OCRの処理
    tools = pyocr.get_available_tools()
    # 長さが0だったら、終了させる
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]

    # 名前を格納する空のリストを作成
    name_list = []

    # for文を使って複数ファイルを開いて閉じる処理
    # enumerate:インデックス番号と、リストの要素をセットで取得できる
    for idx, file in enumerate(todokede_list):
        print('open :', file)
        # ファイルを１つずつ開いて
        pdf_pro = subprocess.Popen([acr_path, todokede_path+file])
        time.sleep(3)

        # 範囲をしてしてキャプチャーする
        # region(左から配置位置、上からの配置位置、幅、高さ)
        img = pag.screenshot('screenshot.png',region=(1540,1270,330,70)) 
        # print(img)

        # キャプチャーした画像をOCR
        txt = tool.image_to_string(
            Image.open('screenshot.png'),
            lang="jpn",
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )
        print(txt) 
        name_list.append(txt)

        # ファイルを閉じる
        pag.click(CLOSE_BUTTON_X, CLOSE_BUTTON_Y)
        time.sleep(1)
    print(name_list)
    copy_name_data(name_list)

    pag.alert('データ取り込み終了しました')

