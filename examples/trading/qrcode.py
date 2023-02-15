import cv2

"""
    You will need to install the following library  :
        - opencv-python
    
    For instance by doing `pip install opencv-python`.
"""

img_path = "YOUR_QRCODE.png"
img = cv2.imread(img_path)
detect = cv2.QRCodeDetector()
data, points, straight_qrcode = detect.detectAndDecode(img)
print("This is the content of your QRCode : ", data, type(data))
