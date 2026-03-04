import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import frangi
from skimage import util

# 1) Load image1.jpg
img1 = cv2.imread("pres_scratch.jpg")
if img1 is None:
    raise FileNotFoundError("image1.jpg not found in current directory.")

# Convert to RGB for display later
img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

# 2) Convert image1 to grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

# 3) Apply Frangi filter
vesselness = frangi(gray1, sigmas=np.arange(1, 5, 1), black_ridges=True)

# 4) Convert float image (0–1) to 8-bit (0–255)
vesselness_img = util.img_as_ubyte(vesselness)

# 5) Load image2.jpg
img2 = cv2.imread("pres_scratch_keepout.jpg")
if img2 is None:
    raise FileNotFoundError("image2.jpg not found in current directory.")

img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

# 6) Pick out red pixels from image2
# Since OpenCV loads in BGR format:
# Red ≈ [255,0,0] in RGB → [0,0,255] in BGR
blue_channel = img2[:, :, 0]
green_channel = img2[:, :, 1]
red_channel = img2[:, :, 2]

# Create mask for strong red pixels
red_mask = (
    (red_channel > 200) &
    (green_channel < 50) &
    (blue_channel < 50)
)

# 7) Compare the two images
# Condition:
# - Frangi pixel value > 20
# - Pixel location is red in image2

highlight_img = img1_rgb.copy()

condition = (vesselness_img > 20) & red_mask

# Highlight those pixels in red on image1
highlight_img[condition] = [255, 0, 0]  # RGB red

# 8) Show results
plt.figure(figsize=(21, 6))

plt.subplot(1, 4, 1)
plt.imshow(img1_rgb)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 4, 2)
plt.imshow(vesselness_img, cmap="gray")
plt.title("Image After Frangi Filter")
plt.axis("off")

plt.subplot(1, 4, 3)
plt.imshow(img2_rgb)
plt.title("Part Scan Zone")
plt.axis("off")

plt.subplot(1, 4, 4)
plt.imshow(highlight_img)
plt.title("Highlighted Defects")
plt.axis("off")

plt.tight_layout()
plt.show()
