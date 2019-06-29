# coding: UTF-8

"""
--説明--
25分 or 5分を計測することができるタイマー
25min : 25分を計測開始する
5min  : 5分を計測開始する
Reset : タイマーをリセットする (ポップアップで停止するかを確認する)

タイマー終了はポップアップでお知らせする

※sleepでの時間計測なので、正確な時間計測ではない
"""

import tkinter as tk
import threading as th
import time
from tkinter import messagebox

stop_flg = False
thread = None

def countdown(min): # カウントダウンを実行する関数
    global stop_flg
    global thread
    global cnt_time

    print(stop_flg)

    reset_flg = 0 # resetを押されたのフラグ

    if not stop_flg:
        for i in range(0, min):
            if stop_flg == 1: # Resetボタンが押されて割り込みが発生した場合
                thread = None
                reset_flg = 1
                print("Reset timer")
                break
            
            # 表示する値を計算
            cnt_down_time     = min - i # 設定値からどれだけ時間たったか
            cnt_down_time_min = int(cnt_down_time / 60) # 分の値を計算
            cnt_down_time_sec = cnt_down_time - cnt_down_time_min * 60 # 秒の値を計算
            print(cnt_down_time, cnt_down_time_min, cnt_down_time_sec) # debug
            cnt_time.set(str(cnt_down_time_min) + ":" + str(cnt_down_time_sec)) # labelに分:秒の表示形式で渡す

            time.sleep(1) # 1秒待ち

        print("finish") # debug
        cnt_time.set("finish") # 終了したことをLabelに表示
        thread = None # 実行されているThreadがなくなるので、Noneを代入

        # 終了したことをポップアップで知らせる
        if reset_flg == 0: # resetを押されてないときのみ、表示させる
            tk.messagebox.showinfo("終了しました", str(int(min / 60)) + "分が経過しました")

def start_count_down(min): # カウントダウンを開始する関数
    global stop_flg
    global thread

    print(stop_flg, thread) # debug

    if not thread:
        stop_flg = False # カウントダウンを行うので、停止フラグをFalseにする
        thread = th.Thread(target = countdown, args = (min, )) # threadでcountdown関数を実行 実行時間は引数で受け取る
        thread.start()

def pushed_25min(button):
    print("Start 25min")

    min = 25 * 60 # 設定する時間

    start_count_down(min) # どのくらいの時間countdownを実行するか指定してスタートさせる

def pushed_5min(button):
    print("Start 5min")

    min = 5 * 60 # 設定する時間

    start_count_down(min) # どのくらいの時間countdownを実行するか指定してスタートさせる

def pushed_Reset(button):
    print("Reset Timer")

    global stop_flg
    global thread

    print(stop_flg, thread) # debug

    if thread: # もしthreadを実行中であれば、停止フラグをたてて、実行を停止させる
        ret = messagebox.askyesno("確認", "タイマーをResetしますか？")
        if ret == True:
            cnt_time.set("reset timer") # resetしたことを表示させる
            stop_flg = True

if __name__ == "__main__":
    root = tk.Tk()

    root.title("ptimer")

    topFrame = tk.Frame(root)
    topFrame.pack(fill="x")

    # 測定した時間を格納する
    global cnt_time
    cnt_time = tk.StringVar()
    cnt_time.set("start ptimer")

    # 計測時間を表示する
    label_time = tk.Label(topFrame, textvariable=cnt_time)
    label_time.pack(fill="x", padx=20, side="top")

    button_25min = tk.Button(topFrame, text="25min", command = lambda:pushed_25min(button_25min))
    button_25min.pack(fill="x", padx=20, side="left") # ボタンを表示して並べるために必要

    button_5min = tk.Button(topFrame, text="5min", command = lambda:pushed_5min(button_5min))
    button_5min.pack(fill="x", padx=20, side="left") # ボタンを表示して並べるために必要

    button_rst = tk.Button(topFrame, text="Reset", command = lambda:pushed_Reset(button_rst))
    button_rst.pack(fill="x", padx=20, side="left") # ボタンを表示して並べるために必要

    root.attributes("-topmost", True) # 常に最前面に表示
    root.mainloop()

    stop_flg = True
    thread.join()