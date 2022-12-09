# 使用するライブラリ
import os
import cv2
import pyocr
import pyocr.builders
import numpy as np
from PIL import Image
import time
from tqdm import tqdm
from moviepy.editor import *
import sys


def main():
    # windowsの場合これを実行する
    # path_tesseract = "C:¥¥Program Files¥¥Tesseract-OCR"
    # if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    #     os.environ["PATH"] += os.pathsep + path_tesseract
    # コマンドライン引数の読み込み
    path_list = sys.argv
    read_file  = path_list[1]
    write_file = path_list[2]
    data = make_data(read_file)
    edit = battle_cut(data)
    capture(read_file,edit,write_file)

    return

# OCRで数字を読み取る関数
def get_num(frame):
    bgr2rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    to_PIL = Image.fromarray(bgr2rgb)
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool")
    
    tool = tools[0]
    lang = 'eng'

    text = tool.image_to_string(
    Image.fromarray(bgr2rgb),
    lang=lang,
    #builder=pyocr.builders.DigitBuilder()
    builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    
    if text.isdigit():
        text = int(text)
    else:
        text = '-'
    
    return text

# 切り取りに使用するデータの作成（タイムスタンプ30フレームごとで判定）
def make_data(read_name):
    # データを格納するための配列
    battle_data = []
    # 認識範囲
    xmin,xmax = 1145,1190
    ymin,ymax = 640,666
    
    
    read_file = cv2.VideoCapture(read_name)

    # フレーム数のカウント
    frame_cnt = 0
    frame_num = int(read_file.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = read_file.get(cv2.CAP_PROP_FPS)
    time_stamp = 0
   
    add_time = 1/fps
    
    # 真偽値
    tf = 0
    
    # errorの初期化
    error = 0
    
    for i in tqdm(range(frame_num)):
        ret, frame = read_file.read()
        # 初期化 1次元の[数字,フレーム数,真偽値]
        num = []
        if not ret:
            break
        frame = cv2.resize(frame,dsize=(1280,720))
        # 弾数が減っている部分を切り出している
        bullet_num = frame[ymin:ymax,xmin:xmax]

        detframe = cv2.bitwise_not(bullet_num)

        # 関数get_numを呼び出して数字をカウントしていく(30フレームおきに)
        if i%30 == 0:
            number = get_num(detframe)        
            # 誤差についての計算
            if frame_cnt != 0:
                # エラーの算出
                error = detframe.astype(int) - before_frame.astype(int)
                error = error.max()
            
        # 一次元配列に格納
        num.append(number)    # 数字
        num.append(frame_cnt)    # フレーム数
        num.append(tf)    # 真偽値
        num.append(error)
        num.append(time_stamp)

        # 二次元配列に格納
        battle_data.append(num)

        # フレーム数を増やす
        frame_cnt+=1
        time_stamp+=add_time
        before_frame = detframe

    read_file.release()
    
    return battle_data

# 射撃シーン判定アルゴリズム
def battle_cut(db):    # db=[num,frame_num,tf]
    # frame数,現在のフレームをカウントする変数
    frame_len = len(db)
    frame_cnt = 0
    battle_true = 1    # battleしていると判断したものはtfを1に変換する
    keep_num = 0    # 数字を保持しておくための変数
    rainbow_cnt = 150    # カットするためのフレーム数の定義７フレーム動いていないと撃っていないと判断する
    start_late = 15  # 打ち始めを考慮したフレーム数
    # battle判定
    while True:
        if frame_cnt >= frame_len:
            break
        keep_num = db[frame_cnt][0]        # 現在のフレームの時の弾数を格納しておく
        start_point = 0    # 打ち始めるポイント
        conti_cnt=0
        if db[frame_cnt][0] != "-" and db[frame_cnt][3] > 5:        # 数字を検知していないところはカット
            while True:    # 同じ数字が何回続いたかをカウントする
                conti_cnt+=1
                if frame_cnt+conti_cnt >=frame_len:
                    break
                if keep_num != db[frame_cnt+conti_cnt][0]:
                    break
            start_point = frame_cnt-start_late
            for i in range(rainbow_cnt+start_late):
                if frame_cnt+i >=frame_len:
                    break
                db[start_point+i][2] = int(1)
            frame_cnt+=conti_cnt
        else:
            frame_cnt+=1
    return db

# 動画を作成する関数
def capture(read_name,cut_data,write_name):
    # 映像の呼び出し
    clip = VideoFileClip(read_name) 
    # 音声の呼び出し
    audio = AudioFileClip(read_name)
    
    # 映像と音声の結び付け
    clip = clip.set_audio(audio)
    
    start_time = 0
    flag = 0
    stop_time =0
    cut_cnt = 0
    
    fin = clip.subclip(0,0.0000001)
    
    for i in cut_data:
        if i[2] == 1 and flag == 0:
            start_time = i[4]
            flag = 1
        if i[2] == 0 and flag == 1:
            stop_time = i[4]
            flag = 0
            """
            if cut_cnt == 0:
                fin = clip.subclip(start_time,stop_time)
                cut_cnt += 1
            else:
            """
            clip_tmp = clip.subclip(start_time,stop_time)
            audio_tmp = audio.subclip(start_time,stop_time)
            
            clip_tmp = clip_tmp.set_audio(audio_tmp)
            
            fin = concatenate_videoclips([fin,clip_tmp])         
    fin.write_videofile(write_name,
                                     codec='libx264',
                                     audio_codec='aac',
                                     temp_audiofile='temp-audio.m4a',
                                     remove_temp=True)
    
    return

main()