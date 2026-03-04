import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize

# --------------------------------------------------
# 1) Load image1 and convert to grayscale
# --------------------------------------------------
img1 = cv2.imread("pres_good.jpg")
if img1 is None:
    raise FileNotFoundError("image1.jpg not found.")

img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

# --------------------------------------------------
# 2) Prewitt edge detection
# --------------------------------------------------
kernelx = np.array([[1, 0, -1],
                    [1, 0, -1],
                    [1, 0, -1]], dtype=np.float32)

kernely = np.array([[ 1,  1,  1],
                    [ 0,  0,  0],
                    [-1, -1, -1]], dtype=np.float32)

gx = cv2.filter2D(gray1, cv2.CV_32F, kernelx)
gy = cv2.filter2D(gray1, cv2.CV_32F, kernely)

grad_mag = np.sqrt(gx**2 + gy**2)

# Binary threshold (like MATLAB edge auto-threshold)
_, BW = cv2.threshold(
    grad_mag.astype(np.uint8),
    0, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# --------------------------------------------------
# Thinning step (approximates MATLAB edge thinning)
# --------------------------------------------------
BW_bool = BW > 0
thinned = skeletonize(BW_bool)
img = thinned.astype(np.uint8)   # final binary image (0/1)

# --------------------------------------------------
# 3) Sliding window code (converted from MATLAB)
# --------------------------------------------------
rows, cols = img.shape

outRows = (rows - 7) // 2 + 1
outCols = (cols - 7) // 2 + 1

outputImg = np.zeros((outRows * 3, outCols * 3), dtype=np.uint8)

for r in range(0, rows - 6, 2):
    for c in range(0, cols - 6, 2):

        window = img[r:r+7, c:c+7]

        if np.sum(window) >= 20:

            outR = (r // 2) * 3
            outC = (c // 2) * 3

            outputImg[outR:outR+3, outC:outC+3] = 1

# Resize result
scale_factor = 480 / 711
new_size = (
    int(outputImg.shape[1] * scale_factor),
    int(outputImg.shape[0] * scale_factor)
)

outputImg_resized = cv2.resize(
    outputImg,
    new_size,
    interpolation=cv2.INTER_NEAREST
)

# Match image1 size
outputImg_resized = cv2.resize(
    outputImg_resized,
    (img1.shape[1], img1.shape[0]),
    interpolation=cv2.INTER_NEAREST
)

# --------------------------------------------------
# 4) Load image2
# --------------------------------------------------
img2 = cv2.imread("pres_dent_zones.jpg")
if img2 is None:
    raise FileNotFoundError("image2.jpg not found.")

img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

b = img2[:, :, 0]
g = img2[:, :, 1]
r = img2[:, :, 2]

red_mask = (r > 200) & (g < 50) & (b < 50)

# --------------------------------------------------
# 5) Highlight pixels
# --------------------------------------------------
highlight_img = img1_rgb.copy()

condition = (outputImg_resized == 1) & red_mask
highlight_img[condition] = [255, 0, 0]

# --------------------------------------------------
# 6) Display results
# --------------------------------------------------
plt.figure(figsize=(21, 6))

plt.subplot(1, 4, 1)
plt.imshow(img1_rgb)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 4, 2)
plt.imshow(img * 255, cmap="gray")
plt.title("Prewitt + Thinning")
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