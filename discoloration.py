import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1) Load the image
image = cv2.imread("pres_good.jpg")

if image is None:
    raise FileNotFoundError("image.jpg not found in the current directory.")

# Convert BGR (OpenCV default) to RGB for displaying
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 2) Create blue color mask (HSV space)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_blue = np.array([90,50,50])
upper_blue = np.array([140,255,255])

mask = cv2.inRange(hsv, lower_blue, upper_blue)

# 3) Extract only blue pixels
blue_only = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)

# 4) Compute percentage of blue pixels
total_pixels = image.shape[0] * image.shape[1]
blue_pixels = np.count_nonzero(mask)
percentage_blue = (blue_pixels / total_pixels) * 100

# 5) Create overlay image with pure blue pixels
overlay_image = image_rgb.copy()

# Set detected blue pixels to pure blue [0, 0, 255] in RGB
overlay_image[mask > 0] = [0, 0, 255]

# 6) Display results
plt.figure(figsize=(21, 6))

plt.subplot(1, 4, 1)
plt.imshow(image_rgb)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 4, 2)
plt.imshow(blue_only)
plt.title("Blue Pixels Extracted")
plt.axis("off")

plt.subplot(1, 4, 3)
plt.imshow(mask, cmap="gray")
plt.title(f"Blue Pixel Mask -- {percentage_blue:.2f}% Blue")
plt.axis("off")

plt.subplot(1, 4, 4)
plt.imshow(overlay_image)
plt.title("Blue Pixels Highlighted (Pure Blue)")
plt.axis("off")

plt.tight_layout()
plt.show()

print(f"Percentage of blue pixels: {percentage_blue:.2f}%")