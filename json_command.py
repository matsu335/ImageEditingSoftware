import base64
from PIL import Image
from io import BytesIO
import zlib
import json

def encode_image_to_base64(img: Image.Image) -> str:
    buffered = BytesIO()
    img.save(buffered, format="PNG")  # PNG形式で保存
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode('utf-8')  # Base64文字列に変換

def compress_base64_data(base64_data: str) -> str:
    # Base64データをバイナリ形式にデコード
    img_bytes = base64.b64decode(base64_data)
    
    # zlibで圧縮
    compressed_data = zlib.compress(img_bytes)
    
    # 圧縮したデータを再度Base64エンコードして格納
    return base64.b64encode(compressed_data).decode('utf-8')

def save_image_to_json(image: Image.Image, file_path: str):
    # 画像をBase64に変換
    base64_data = encode_image_to_base64(image)
    
    # Base64データを圧縮
    compressed_data = compress_base64_data(base64_data)
    
    # JSONデータに保存
    data = {
        'imageData': compressed_data
    }
    
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

def load_image_from_json(file_path: str) -> Image.Image:
    # JSONからデータを読み込む
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    
    # 圧縮されたBase64データを取得
    compressed_data = data['imageData']
    
    # 圧縮データをデコード
    compressed_bytes = base64.b64decode(compressed_data)
    
    # zlibで復元
    img_bytes = zlib.decompress(compressed_bytes)
    
    # バイナリデータを画像として読み込む
    img = Image.open(BytesIO(img_bytes))
    return img


