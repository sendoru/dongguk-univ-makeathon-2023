import base64
import cv2
import numpy as np

def encode_image_to_jpg_base64(img: np.ndarray):
    flag, img_encoded = cv2.imencode('.jpg', img)
    return base64.b64encode(img_encoded).decode('utf-8')

def decode_image_from_jpg_base64(img_encoded: str):
    img_encoded_bytes = base64.b64decode(img_encoded)
    img_encoded_ndarray = np.fromstring(img_encoded_bytes, dtype=np.byte)
    img_decoded = cv2.imdecode(img_encoded_ndarray, flags=cv2.IMREAD_ANYCOLOR)
    # img_decoded = cv2.cvtColor(img_decoded, cv2.COLOR_BGR2RGB)
    return img_decoded

def filter_single_channel(img: np.ndarray, channel: str):
    ch_str_to_int = {'R' : 0, 'G' : 1, 'B' : 2}
    if not channel in ch_str_to_int.keys():
        raise ValueError(f"'channel' should be one of 'R', 'G', 'B' but received {channel}")
    if len(img.shape) != 3 or img.shape[2] != 3:
        raise ValueError(f"Expected shape of img to be (*, *, 3) but it is {img.shape}")
    return img[:,:,ch_str_to_int[channel]]

def get_gradient_magnitude(img: np.ndarray):
    # 가우시안 필터 적용
    blurred = cv2.GaussianBlur(img, (5, 5), 0)

    # Sobel 필터를 사용하여 그래디언트 계산
    gradient_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)

    # 그래디언트 크기 계산
    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)

    # 그래디언트 방향 계산 (라디안)
    gradient_direction = np.arctan2(gradient_y, gradient_x)

    # 그래디언트 크기와 방향을 0~255로 스케일 조정 (선택 사항)
    gradient_magnitude = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    return gradient_magnitude
