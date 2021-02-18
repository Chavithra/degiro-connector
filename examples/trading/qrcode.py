from pyzbar.pyzbar import decode
from PIL import Image

"""
    This is an example on how to extract the text from a QRCode image.
    You will need to install the library : pyzbar
"""

data = decode(Image.open('YOUR_QRCODE.png'))[0].data
print('This is the content of your QRCode : ', data)
