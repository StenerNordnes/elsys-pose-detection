import qrcode

def generateRandomString():
    import random
    import string
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


# Define the data you want to encode in the QR code
data = "HP9XSVGXQ5"

# Generate the QR code
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QR code
img = qr.make_image(fill="black", back_color="white")

# Save the image as a file
img.save("qrcode.png")