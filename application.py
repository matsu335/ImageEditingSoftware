import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter.messagebox as messagebox
import os

# JSON形式を使うか。まだPNG形式で圧縮し書き込み、及びPNG形式で圧縮したJSONファイルの読み出ししか実装しておらず。また、圧縮形式も独自の形。
USE_JSON = True
if USE_JSON == True:
    import json
    from json_command import encode_image_to_base64, compress_base64_data, load_image_from_json

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
margin_w = 30
margin_h = 30

scale = 1.0

image_width = 0
image_height = 0

now_img = None
now_filepath = None
mode = 0

x_high, x_low = image_width, 0
y_high, y_low = image_height, 0
# グローバル変数としてIDを保存するリストを定義
trim_ids = []

resize_yoko = 0
resize_tate = 0

def select_button(button):
    """ボタンを選択した状態にする"""
    # すべてのボタンの色をデフォルトに戻す
    for btn in buttons:
        btn.config(bg="white", fg="black", relief="raised")

    # クリックされたボタンだけ色を変更
    if button != None:
        button.config(bg="blue", fg="white", relief="sunken")

    button_availability()

def button_availability():
    if mode == 0:
        for button in buttons_trim:
            button.config(state="disabled")
        for button in buttons_resize:
            button.config(state="disabled")
        for button in buttons_rotate:
            button.config(state="disabled")
        for entry in entries_trim:
            entry.delete(0, tk.END)
            entry.config(state="disabled")
        for entry in entries_resize:
            entry.delete(0, tk.END)
            entry.config(state="disabled")
    if mode == 1:
        for button in buttons_trim:
            button.config(state="normal")
        for button in buttons_resize:
            button.config(state="disabled")
        for button in buttons_rotate:
            button.config(state="disabled")
        values = [0, image_width, 0, image_height]
        for entry, value in zip(entries_trim, values):
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, str(value))
        for entry in entries_resize:
            entry.delete(0, tk.END)
            entry.config(state="disabled")
    if mode == 2:
        for button in buttons_trim:
            button.config(state="disabled")
        for button in buttons_resize:
            button.config(state="normal")
        for button in buttons_rotate:
            button.config(state="disabled")
        for entry in entries_trim:
            entry.delete(0, tk.END)
            entry.config(state="disabled")
        values = [image_width, image_height]
        for entry, value in zip(entries_resize, values):
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, str(value))
    if mode == 3:
        for button in buttons_trim:
            button.config(state="disabled")
        for button in buttons_resize:
            button.config(state="disabled")
        for button in buttons_rotate:
            button.config(state="normal")
        for entry in entries_trim:
            entry.delete(0, tk.END)
            entry.config(state="disabled")
        for entry in entries_resize:
            entry.delete(0, tk.END)
            entry.config(state="disabled")

def open_image(file_path):
    """画像を開いて表示する"""
    global image_width, image_height, x_high, y_high, now_filepath, resize_yoko, resize_tate
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
        try:
            img = Image.open(file_path)
            image_width, image_height = img.size
            x_high, y_high = image_width, image_height
            resize_yoko, resize_tate = image_width, image_height
            show_image(img)
            for button in buttons:
                button.config(state="normal")
            status_label.config(text="画像を読み込みました", fg="green")
            now_filepath = file_path
            save_label.config(text="")
        except Exception as e:
            status_label.config(text=f"エラー: {str(e)}", fg="red")
    elif file_path.lower().endswith(('.json')):
        if USE_JSON==True:
            try:
                img = load_image_from_json(file_path)
                image_width, image_height = img.size
                x_high, y_high = image_width, image_height
                resize_yoko, resize_tate = image_width, image_height
                show_image(img)
                for button in buttons:
                    button.config(state="normal")
                status_label.config(text="画像を読み込みました", fg="green")
                now_filepath = file_path
                save_label.config(text="")
            except Exception as e:
                status_label.config(text=f"エラー: {str(e)}", fg="red")
        else:
            status_label.config(text="JSONファイル対応はOFFです", fg="red")
    else:
        status_label.config(text="PNG,JPEGまたはPDFファイルのみ対応しています", fg="red")

def show_image(img):
    """画像をLabelに表示"""
    global now_img
    shownImg = resize_shownimage(img)
    img_tk = ImageTk.PhotoImage(shownImg)
    # 画像をCanvasに表示
    canvas.delete("all")  # 既存の画像を削除
    canvas.create_image(margin_w, margin_h, anchor="nw", image=img_tk)
    canvas.image = img_tk
    now_img = img
    show_image_size()
    
def show_image_size():
    x, y = now_img.size
    width_label.config(text=f"{x}")
    height_label.config(text=f"{y}")

def resize_shownimage(img):
    global image_width, image_height, x_high, y_high, scale
    image_width, image_height = img.size
    x_high, y_high = image_width, image_height
    if CANVAS_WIDTH > image_width and CANVAS_HEIGHT > image_height:
        scale = 1.0
        return img
    elif CANVAS_HEIGHT/CANVAS_WIDTH > image_height/image_width:
        scale = CANVAS_WIDTH / image_width
    else:
        scale = CANVAS_HEIGHT / image_height
    # 新しい画像サイズ
    new_width = int(scale * image_width)
    new_height = int(scale * image_height)
    # 画像をリサイズ
    img = img.resize((new_width, new_height))

    return img

def read_image():
    """ファイルダイアログで画像を選択"""
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.pdf;*.json")])
    if file_path:
        open_image(file_path)

def on_drop(event):
    """ドラッグ＆ドロップで画像を開く"""
    file_path = event.data.strip('{}')  # {} が付く場合があるので削除
    if os.path.isfile(file_path):
        open_image(file_path)
    else:
        status_label.config(text="有効なファイルではありません", fg="red")

def trimming_mode():
    global mode
    mode = 1
    select_button(btn_trimming)
    show_image(now_img)
    draw_rectangle()

def draw_rectangle():
    """点線の矩形を描画し、端に座標を表示"""
    global trim_ids
    # 既存の線とテキストを削除する
    for trim_id in trim_ids:
        canvas.delete(trim_id)

    # 矩形の描画
    trim_ids = []
    trim_ids.append(canvas.create_line(margin_w+x_low*scale, margin_h, margin_w+x_low*scale, margin_h+y_high*scale, fill="red", dash=(5, 5), width=2))
    trim_ids.append(canvas.create_line(margin_w+x_high*scale, margin_h, margin_w+x_high*scale, margin_h+y_high*scale, fill="red", dash=(5, 5), width=2))
    trim_ids.append(canvas.create_line(margin_w, margin_h+y_low*scale, margin_w+x_high*scale, margin_h+y_low*scale, fill="red", dash=(5, 5), width=2))
    trim_ids.append(canvas.create_line(margin_w, margin_h+y_high*scale, margin_w+x_high*scale, margin_h+y_high*scale, fill="red", dash=(5, 5), width=2))
    trim_ids.append(canvas.create_rectangle(margin_w+x_low*scale, margin_h+y_low*scale, margin_w+x_high*scale, margin_h+y_high*scale, outline="red", width=2, fill=None))

    # 座標の大きい方の値を表示
    trim_ids.append(canvas.create_text(margin_w+x_low*scale, margin_h, text=f"{x_low}", font=("Arial", 10), fill="blue", anchor="s"))
    trim_ids.append(canvas.create_text(margin_w+x_high*scale, margin_h, text=f"{x_high}", font=("Arial", 10), fill="blue", anchor="s"))
    trim_ids.append(canvas.create_text(margin_w, margin_h+y_low*scale, text=f"{y_low}", font=("Arial", 10), fill="blue", anchor="e"))
    trim_ids.append(canvas.create_text(margin_w, margin_h+y_high*scale, text=f"{y_high}", font=("Arial", 10), fill="blue", anchor="e"))
    # coords = [
    #     (x_low, 0, max(x_low, 0)), 
    #     (x_high, 0, max(x_high, 0)), 
    #     (0, y_low, max(0, y_low)), 
    #     (0, y_high, max(0, y_high))
    # ]
    
    # for x, y, max_value in coords:
    #     canvas.create_text(x*scale, y*scale, text=f"{max_value}", font=("Arial", 10), fill="blue", anchor="nw")

def on_change_xl(*args):
    global x_low
    try:
        x_low = int(entry_xl.get())  # 入力された値を取得
        x_low = max(0, x_low)  # 範囲制限: 0以上
        x_low = min(x_low, x_high)  # 範囲制限: x_high以下
        draw_rectangle()
    except ValueError:
        x_low = 0  # 数字以外が入力された場合は0に戻す

def on_change_xh(*args):
    global x_high
    try:
        x_high = int(entry_xh.get())  # 入力された値を取得
        x_high = max(x_low, x_high)  # 範囲制限: x_low以上
        x_high = min(x_high, image_width)  # 範囲制限: image_width以下
        draw_rectangle()
    except ValueError:
        x_high = image_width  # 数字以外が入力された場合は最大値に戻す

def on_change_yl(*args):
    global y_low
    try:
        y_low = int(entry_yl.get())  # 入力された値を取得
        y_low = max(0, y_low)  # 範囲制限: 0以上
        y_low = min(y_low, y_high)  # 範囲制限: y_high以下
        draw_rectangle()
    except ValueError:
        y_low = 0  # 数字以外が入力された場合は0に戻す

def on_change_yh(*args):
    global y_high
    try:
        y_high = int(entry_yh.get())  # 入力された値を取得
        y_high = max(y_low, y_high)  # 範囲制限: y_low以上
        y_high = min(y_high, image_height)  # 範囲制限: image_height以下
        draw_rectangle()
    except ValueError:
        y_high = image_height  # 数字以外が入力された場合は最大値に戻す

def run_trim():
    global now_img, x_low, x_high, y_low, y_high, mode
    now_img = now_img.crop((x_low, y_low, x_high, y_high))
    show_image(now_img)
    x_low, y_low = 0, 0
    x_high, y_high = now_img.size
    mode = 0
    select_button(None)

def resize_mode():
    global mode
    mode = 2
    select_button(btn_resize)
    show_image(now_img)

def on_change_yoko(*args):
    global resize_yoko
    try:
        resize_yoko = int(entry_yoko.get())  # 入力された値を取得
        resize_yoko = max(1, resize_yoko)  # 範囲制限
    except ValueError:
        resize_yoko = image_width  # 数字以外が入力された場合は最大値に戻す

def on_change_tate(*args):
    global resize_tate
    try:
        resize_tate = int(entry_tate.get())  # 入力された値を取得
        resize_tate = max(1, resize_tate)  # 範囲制限
    except ValueError:
        resize_tate = image_height  # 数字以外が入力された場合は最大値に戻す

def run_resize():
    global now_img, mode, resize_yoko, resize_tate
    now_img = now_img.resize((resize_yoko, resize_tate))
    show_image(now_img)
    resize_yoko, resize_tate = now_img.size
    mode = 0
    select_button(None)

def rotate_mode():
    global mode
    mode = 3
    select_button(btn_rotate)
    show_image(now_img)

def on_rotateButton_click(button_name):
    global now_img
    if button_name == "L90°":
        rotated_img = now_img.rotate(90, expand=True)
    elif button_name == "R90°":
        rotated_img = now_img.rotate(-90, expand=True)
    elif button_name == "Hfrip":
        rotated_img = now_img.transpose(Image.FLIP_LEFT_RIGHT)
    elif button_name == "Vfrip":
        rotated_img = now_img.transpose(Image.FLIP_TOP_BOTTOM)
    show_image(rotated_img)

def save_as():
    # ファイルダイアログを開いて保存先とファイル名を指定
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[
        ("PNG", "*.png"),
        ("JPEG", "*.jpg"),
        ("JPEG", "*.jpeg"),
        ("PDF", "*.pdf"),
        ("JSON", "*.json"),
        ("All files", "*.*")
    ])
    
    if file_path:
        # 現在の画像 (now_img) を指定された形式で保存
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
            now_img.save(file_path)  # 画像を保存
            save_label.config(text=f"画像が保存されました: {file_path}", fg="green")
        elif USE_JSON==True and file_path.lower().endswith('.json'):
            # 画像をBase64に変換
            base64_data = encode_image_to_base64(now_img)
            # Base64データを圧縮
            compressed_data = compress_base64_data(base64_data)
            # JSONデータに保存
            data = {
                'imageData': compressed_data
            }
            # JSONファイルに書き込む
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file)
            
            save_label.config(text=f"画像がJSON形式で保存されました: {file_path}", fg="green")
        else:
            save_label.config(text="サポートされていない形式です。", fg="red")

def save_over():
    """現在開いているファイルに上書き保存"""
    global now_img, now_filepath

    if now_filepath:  # now_filepath が指定されている場合
        # 上書き保存確認のメッセージボックスを表示
        result = messagebox.askyesno("上書き確認", f"本当に上書き保存しますか？ {now_filepath}")
        
        if result:  # ユーザーが「はい」を選択した場合
            try:
                # 拡張子を取得し、適切な形式で保存
                if now_filepath.lower().endswith('.png'):
                    now_img.save(now_filepath, format='PNG')
                elif now_filepath.lower().endswith('.jpeg') or now_filepath.lower().endswith('.jpg'):
                    now_img.save(now_filepath, format='JPEG')
                elif now_filepath.lower().endswith('.pdf'):
                    now_img.save(now_filepath, format='PDF')
                elif now_filepath.lower().endswith('.json'):
                    # 画像をBase64に変換
                    base64_data = encode_image_to_base64(now_img)
                    # Base64データを圧縮
                    compressed_data = compress_base64_data(base64_data)
                    # JSONデータに保存
                    data = {
                        'imageData': compressed_data
                    }
                    # JSONファイルに書き込む
                    with open(now_filepath, 'w') as json_file:
                        json.dump(data, json_file)
                else:
                    save_label.config(text="対応していないファイル形式です", fg="red")
                    return

                save_label.config(text=f"上書き保存しました: {now_filepath}", fg="green")
            except Exception as e:
                save_label.config(text=f"エラー: {str(e)}", fg="red")
        else:
            save_label.config(text="上書き保存をキャンセルしました", fg="blue")  # キャンセルした場合
    else:
        save_label.config(text="ファイルが開かれていません", fg="red")


# メインウィンドウ (TkinterDnDを適用)
root = TkinterDnD.Tk()
root.title("画像編集ソフト by Me")
root.geometry("1200x640")

# 左側フレーム（ボタン配置）
left_frame = tk.Frame(root, width=200)
left_frame.grid(row=0, column=0, sticky="ns")
left_frame.grid_propagate(False)

readfile_frame = tk.Frame(left_frame, bd=3, relief="ridge")
readfile_frame.pack(side="top", fill="x")
trimming_frame = tk.Frame(left_frame, bd=3, relief="ridge")
trimming_frame.pack(side="top", fill="x")
resize_frame = tk.Frame(left_frame, bd=3, relief="ridge")
resize_frame.pack(side="top", fill="x")
rotate_frame = tk.Frame(left_frame, bd=3, relief="ridge")
rotate_frame.pack(side="top", fill="x")

btn_readfile = tk.Button(readfile_frame, text="画像を開く", command=read_image, bg="white")
btn_readfile.pack(pady=10, padx=10, fill="x")

# ドラッグ＆ドロップ用のラベル
drag_label = tk.Label(readfile_frame, text="ここにPNG/JPEG/PDFをドロップ", bg="lightgray", fg="black", font=("Arial", 12))
drag_label.config(height=5)
drag_label.pack(fill="x", padx=10, pady=10)

# ステータスラベル
status_label = tk.Label(readfile_frame, text="", fg="blue", font=("Arial", 10))
status_label.pack(pady=5)

# ドラッグ＆ドロップの設定
drag_label.drop_target_register(DND_FILES)
drag_label.dnd_bind("<<Drop>>", on_drop)

btn_trimming = tk.Button(trimming_frame, text="切り抜き", command=trimming_mode, bg="white")
btn_trimming.pack(pady=10, padx=10, fill="x")

# StringVarを使用して数値を追跡
entry_xl_var = tk.StringVar()
entry_xh_var = tk.StringVar()
entry_yl_var = tk.StringVar()
entry_yh_var = tk.StringVar()

# 配置変える。デフォルトで最初の画像サイズが入力されてるように。
# Entryウィジェットの設定
entry_x_frame = tk.Frame(trimming_frame)
entry_x_frame.pack(side="top", fill="x")
entry_xh = tk.Entry(entry_x_frame, textvariable=entry_xh_var, width=10)
entry_xh.pack(padx=10, pady=3, side="right", anchor="e")
entry_xh_var.trace("w", on_change_xh)
entry_xl = tk.Entry(entry_x_frame, textvariable=entry_xl_var, width=10)
entry_xl.pack(padx=10, pady=3, side="right", anchor="e")
entry_xl_var.trace("w", on_change_xl)
entry_yl = tk.Entry(trimming_frame, textvariable=entry_yl_var, width=10)
entry_yl.pack(pady=10, anchor="nw")
entry_yl_var.trace("w", on_change_yl)
entry_yh = tk.Entry(trimming_frame, textvariable=entry_yh_var, width=10)
entry_yh.pack(pady=10, anchor="nw")
entry_yh_var.trace("w", on_change_yh)
button_run_trim = tk.Button(trimming_frame, text="確定", command=run_trim)
button_run_trim.pack(padx=5, pady=5,side="right", anchor="e")

# リサイズ関係のボタンを配置
btn_resize = tk.Button(resize_frame, text="サイズ変更", command=resize_mode, bg="white")
btn_resize.pack(pady=10, padx=10, fill="x")

entry_yoko_var = tk.StringVar()
entry_tate_var = tk.StringVar()

yoko_label = tk.Label(resize_frame, text="横:", fg="black", font=("Arial", 10))
yoko_label.pack(side="left", padx=2, pady=5)
entry_yoko = tk.Entry(resize_frame, textvariable=entry_yoko_var, width=10)
entry_yoko.pack(padx=2, pady=5, side="left")
entry_yoko_var.trace("w", on_change_yoko)
tate_label = tk.Label(resize_frame, text="縦:", fg="black", font=("Arial", 10))
tate_label.pack(side="left", padx=2, pady=5)
entry_tate = tk.Entry(resize_frame, textvariable=entry_tate_var, width=10)
entry_tate.pack(padx=2, pady=5, side="left")
entry_tate_var.trace("w", on_change_tate)
button_run_resize = tk.Button(resize_frame, text="確定", command=run_resize)
button_run_resize.pack(padx=5, pady=5,side="right", anchor="e")

btn_rotate = tk.Button(rotate_frame, text="回転・反転", command=rotate_mode, bg="white")
btn_rotate.pack(pady=10, padx=10, fill="x")

# 回転・反転ボタンを配置
button_left90 = tk.Button(rotate_frame, text="L90°", command=lambda: on_rotateButton_click("L90°"))
button_left90.pack(side="left", anchor="nw", padx=5, pady=5)

button_right_90 = tk.Button(rotate_frame, text="R90°", command=lambda: on_rotateButton_click("R90°"))
button_right_90.pack(side="left", anchor="nw", padx=5, pady=5)

button_Hfrip = tk.Button(rotate_frame, text="Hfrip", command=lambda: on_rotateButton_click("Hfrip"))
button_Hfrip.pack(side="left", anchor="nw", padx=5, pady=5)

button_Vfrip = tk.Button(rotate_frame, text="Vfrip", command=lambda: on_rotateButton_click("Vfrip"))
button_Vfrip.pack(side="left", anchor="nw", padx=5, pady=5)

# 右側フレーム（画像表示）
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, sticky="nsew")

# 画像表示用のCanvas
canvas = tk.Canvas(right_frame, width=CANVAS_WIDTH+margin_w, height=CANVAS_HEIGHT+margin_h, bg="white")
canvas.pack(pady=10)

size_frame = tk.Frame(right_frame)
size_frame.pack(anchor="e", padx=50)
height_label = tk.Label(size_frame, text="0", fg="black", font=("Arial", 8))
height_label.pack(side="right")
malti_label = tk.Label(size_frame, text="×", fg="black", font=("Arial", 8))
malti_label.pack(side="right")
width_label = tk.Label(size_frame, text="0", fg="black", font=("Arial", 8))
width_label.pack(side="right")


# 保存ボタン
button_saveas = tk.Button(right_frame, text="指定保存(save as ...)", command=save_as)
button_saveas.pack(side="right", anchor="se", padx=15, pady=20)
button_saveover = tk.Button(right_frame, text="上書き保存(save over)", command=save_over)
button_saveover.pack(side="right", anchor="se", padx=15, pady=20)
# データ保存状況表示
save_label = tk.Label(right_frame, text="", fg="blue", font=("Arial", 10))
save_label.pack(side="right", anchor="se", padx=15, pady=20)

# レスポンシブ設定
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# ボタンリスト
buttons = [btn_trimming, btn_resize, btn_rotate, button_saveas, button_saveover]
buttons_trim = [button_run_trim]
entries_trim = [entry_xl, entry_xh, entry_yl, entry_yh]
buttons_resize = [button_run_resize]
entries_resize = [entry_yoko, entry_tate]
buttons_rotate = [button_left90, button_right_90, button_Hfrip, button_Vfrip]

# すべてのボタンを無効にする
for button in buttons:
    button.config(state="disabled")
for button in buttons_trim:
    button.config(state="disabled")
for entry in entries_trim:
    entry.config(state="disabled")
for button in buttons_resize:
    button.config(state="disabled")
for entry in entries_resize:
    entry.config(state="disabled")
for button in buttons_rotate:
    button.config(state="disabled")

root.mainloop()
