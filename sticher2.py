import cv2
import numpy as np

def get_top_down_view(image, src_points):
    """
    Applies a top-down perspective transform to an image.
    
    Args:
        image: The input image from a single camera.
        src_points: A NumPy array of 4 points in the source image.
                    These points should form a trapezoid on the ground.
    
    Returns:
        The warped image, which is a top-down view.
    """
    # Define the width and height of the output top-down image
    # These can be tuned to your preference
    width, height = 400, 400

    # Define the 4 destination points for the top-down view (a rectangle)
    # The order must correspond to the order of src_points
    dst_points = np.float32([
        [0, 0],         # Top-left
        [width, 0],     # Top-right
        [width, height],# Bottom-right
        [0, height]     # Bottom-left
    ])

    # Calculate the perspective transform matrix M
    M = cv2.getPerspectiveTransform(src_points, dst_points)
    
    # Apply the perspective warp to get the top-down view
    warped_image = cv2.warpPerspective(image, M, (width, height))
    
    return warped_image

# --- Main Execution ---
if __name__ == "__main__":
    # --- 1. Load your four images ---
    front_img = cv2.imread("car_images/front_view.jpg")
    back_img = cv2.imread("car_images/back_view.jpg")
    left_img = cv2.imread("car_images/left_view.jpg")
    right_img = cv2.imread("car_images/right_view.jpg")

    # --- 2. DEFINE YOUR PERSPECTIVE POINTS (CRITICAL STEP!) ---
    # These are placeholder values! You MUST find the correct points for YOUR cameras.
    # The points should form a trapezoid on the ground in front of each camera.
    # Format: np.float32([[top_left], [top_right], [bottom_right], [bottom_left]])
    
    # Example points for the FRONT camera
    # You need to find these by looking at your front_img
    src_front = np.float32([(9, 309), (1264, 343), (1132, 705), (231, 708)])

    # Example points for the BACK camera (coordinates will be different)
    src_back = np.float32([(34, 346), (1242, 320), (1045, 709), (261, 708)])

    # Example points for the LEFT camera
    src_left = np.float32([(11, 359), (1258, 333), (1080, 709), (297, 713)])

    # Example points for the RIGHT camera
    src_right = np.float32([(36, 360), (1201, 339), (1113, 712), (265, 715)])

    # --- 3. Apply the top-down warp to each image ---
    front_top_down = get_top_down_view(front_img, src_front)
    back_top_down = get_top_down_view(back_img, src_back)
    left_top_down = get_top_down_view(left_img, src_left)
    right_top_down = get_top_down_view(right_img, src_right)
    cv2.imwrite("right-top-down.jpeg",right_top_down)
    cv2.imwrite("front-top-down.jpeg",front_top_down)
    cv2.imwrite("back-top-down.jpeg",back_top_down)


# --- 4. Combine the images into a single bird's-eye view ---
def create_vertical_gradient_mask(height, width):
    """Creates a mask with a vertical gradient (white at top, black at bottom)."""
    mask = np.zeros((height, width, 3), dtype=np.float32)
    # Create a linear gradient from 1.0 to 0.0
    gradient = np.linspace(1, 0, height, dtype=np.float32)
    # Apply the gradient to all columns and color channels
    mask[:, :, 0] = gradient[:, np.newaxis]
    mask[:, :, 1] = gradient[:, np.newaxis]
    mask[:, :, 2] = gradient[:, np.newaxis]
    return mask

# --- 4. Combine the images into a single bird's-eye view ---
# Get dimensions of the warped images (assuming they are all 400x400)
h, w = front_top_down.shape[:2]

# Define the car area size
car_area_width = 200
car_area_height = 300

# Calculate the output size dynamically
output_width = w + car_area_width + w
output_height = h + car_area_height + h

# --- NEW: Create the gradient masks ---
# This mask fades from top (1.0) to bottom (0.0). We'll reuse it for all views.
mask = create_vertical_gradient_mask(h, w)

# --- Apply masks to the top-down views ---
# We convert to float for multiplication and back to uint8 for display
front_masked = cv2.multiply(front_top_down.astype(np.float32), mask).astype(np.uint8)
back_masked = cv2.multiply(back_top_down.astype(np.float32), mask).astype(np.uint8)
left_masked = cv2.multiply(left_top_down.astype(np.float32), mask).astype(np.uint8)
right_masked = cv2.multiply(right_top_down.astype(np.float32), mask).astype(np.uint8)


# --- Create the canvas and place the images using addition for blending ---
birds_eye_view = np.zeros((output_height, output_width, 3), dtype=np.uint8)
x_offset = w
y_offset = h

# --- Place FRONT image ---
front_resized = cv2.resize(front_masked, (car_area_width, h))
# Use cv2.add() to blend instead of direct assignment
birds_eye_view[0:h, x_offset:x_offset + car_area_width] = cv2.add(
    birds_eye_view[0:h, x_offset:x_offset + car_area_width], front_resized)

# --- Place BACK image ---
back_flipped = cv2.rotate(back_masked, cv2.ROTATE_180)
back_resized = cv2.resize(back_flipped, (car_area_width, h))
birds_eye_view[y_offset + car_area_height : y_offset + car_area_height + h, x_offset : x_offset + car_area_width] = cv2.add(
    birds_eye_view[y_offset + car_area_height : y_offset + car_area_height + h, x_offset : x_offset + car_area_width], back_resized)

# --- Place LEFT image ---
# The vertical gradient becomes horizontal after rotation
left_rotated = cv2.rotate(left_masked, cv2.ROTATE_90_COUNTERCLOCKWISE)
left_resized = cv2.resize(left_rotated, (w, car_area_height))
birds_eye_view[y_offset : y_offset + car_area_height, 0:w] = cv2.add(
    birds_eye_view[y_offset : y_offset + car_area_height, 0:w], left_resized)

# --- Place RIGHT image ---
# The vertical gradient becomes horizontal after rotation
right_rotated = cv2.rotate(right_masked, cv2.ROTATE_90_CLOCKWISE)
right_resized = cv2.resize(right_rotated, (w, car_area_height))
birds_eye_view[y_offset:y_offset + car_area_height, x_offset + car_area_width : x_offset + car_area_width + w] = cv2.add(
    birds_eye_view[y_offset:y_offset + car_area_height, x_offset + car_area_width : x_offset + car_area_width + w], right_resized)

# --- Optional: Add a car icon in the middle ---
# You can uncomment this now if you have a 'car_icon.png'
# car_icon = cv2.imread("car_icon.png")
# if car_icon is not None:
#     car_icon = cv2.resize(car_icon, (car_area_width, car_area_height))
#     birds_eye_view[y_offset:y_offset + car_area_height, x_offset:x_offset + car_area_width] = car_icon

# --- 5. Save and Display the Result ---
cv2.imwrite("birds_eye_view.png", birds_eye_view)
print("Bird's-eye view saved as 'birds_eye_view.png'")

cv2.imshow("Bird's Eye View", birds_eye_view)
cv2.waitKey(0)
cv2.destroyAllWindows()