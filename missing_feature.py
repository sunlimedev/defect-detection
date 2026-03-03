import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1) Load the image
image = cv2.imread("pres_missing_feature.jpg")

if image is None:
    raise FileNotFoundError("image.jpg not found in the current directory.")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 2) Binarization (Otsu thresholding)
_, binarized = cv2.threshold(gray, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 3) Create white 5x5 mask
kernel = np.ones((5, 5), dtype=np.uint8)

# 4) Erode the binarized image
# OpenCV expects values 0–255, so temporarily scale
binarized_255 = (binarized * 255).astype(np.uint8)
eroded = cv2.erode(binarized_255, kernel, iterations=1)

# Convert back to 0/1
eroded_binary = (eroded > 0).astype(np.uint8)

# 5) Highlight pixel (240,240)
highlight_image = cv2.cvtColor(eroded_binary * 255, cv2.COLOR_GRAY2BGR)

rows = [ 91, 226, 361, 364, 367]
cols = [138, 136, 134, 236, 338]
pixel_values = []

row = 367
col = 338

for i in range(len(rows)):
    highlight_image[rows[i], cols[i]] = [0, 0, 255]  # red in BGR
    pixel_values.append(eroded_binary[rows[i], cols[i]])

# Output pixel value to console
for i in range(len(pixel_values)):
    if pixel_values[i] is not None:
        print(f"Pixel value at ({rows[i]},{cols[i]}): {pixel_values[i]}")

if any(pixel_values):
    print("Part has missing feature and is therefore defective.")
else:
    print("Part has no missing feature and may be good.")

# Convert original for display
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
highlight_rgb = cv2.cvtColor(highlight_image, cv2.COLOR_BGR2RGB)

# Display results
plt.figure(figsize=(15, 5))

plt.subplot(1, 4, 1)
plt.imshow(image_rgb)
plt.title("\nOriginal Image")
plt.axis("off")

plt.subplot(1, 4, 2)
plt.imshow(binarized, cmap="gray")
plt.title("\nBinarized Image")
plt.axis("off")

plt.subplot(1, 4, 3)
plt.imshow(eroded_binary, cmap="gray")
plt.title("\nEroded Binarized Image")
plt.axis("off")

plt.subplot(1, 4, 4)
plt.imshow(highlight_rgb)
plt.title("\nSelect Locations Highlighted")
plt.axis("off")

plt.tight_layout()
plt.show()