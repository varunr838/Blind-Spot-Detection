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
    front_img = cv2.imread("car_images/front.jpeg")
    back_img = cv2.imread("car_images/back.jpeg")
    left_img = cv2.imread("car_images/left.jpeg")
    right_img = cv2.imread("car_images/right.jpeg")

    # --- 2. DEFINE YOUR PERSPECTIVE POINTS (CRITICAL STEP!) ---
    # These are placeholder values! You MUST find the correct points for YOUR cameras.
    # The points should form a trapezoid on the ground in front of each camera.
    # Format: np.float32([[top_left], [top_right], [bottom_right], [bottom_left]])
    
    # Example points for the FRONT camera
    # You need to find these by looking at your front_img
    src_front = np.float32([(470, 377), (838, 387), (1158, 557), (10, 524)])

    # Example points for the BACK camera (coordinates will be different)
    src_back = np.float32([(215, 114), (1049, 114), (1126, 687), (122, 683)])

    # Example points for the LEFT camera
    src_left = np.float32([(360, 372), (991, 352), (1278, 708), (75, 704)])

    # Example points for the RIGHT camera
    src_right = np.float32([(335, 386), (956, 366), (1277, 715), (41, 713)])

    # --- 3. Apply the top-down warp to each image ---
    front_top_down = get_top_down_view(front_img, src_front)
    back_top_down = get_top_down_view(back_img, src_back)
    left_top_down = get_top_down_view(left_img, src_left)
    right_top_down = get_top_down_view(right_img, src_right)
    cv2.imwrite("right-top-down.jpeg",right_top_down)
    cv2.imwrite("front-top-down.jpeg",front_top_down)
    cv2.imwrite("back-top-down.jpeg",back_top_down)


    # --- 4. Combine the images into a single bird's-eye view ---
    # Define the size of the final output image and car area
#     output_width = 800  # left_w + right_w
#     output_height = 800 # front_h + back_h
#     car_area_width = 200
#     car_area_height = 300

#     # Create a black canvas
#     birds_eye_view = np.zeros((output_height, output_width, 3), dtype=np.uint8)

#     # Get dimensions of the warped images
#     front_h, front_w = front_top_down.shape[:2]
#     back_h, back_w = back_top_down.shape[:2]
#     left_h, left_w = left_top_down.shape[:2]
#     right_h, right_w = right_top_down.shape[:2]
    
#     # --- Place the warped images onto the canvas ---
#     # Note: These calculations assume warped images are 400x400 as defined in the function
#     x_offset = (output_width - car_area_width) // 2
#     y_offset = (output_height - car_area_height) // 2

#     # Place FRONT image
#     birds_eye_view[y_offset - front_h : y_offset, x_offset : x_offset + front_w] = front_top_down

#     # Place BACK image (it needs to be flipped 180 degrees)
#     back_flipped = cv2.rotate(back_top_down, cv2.ROTATE_180)
#     birds_eye_view[y_offset + car_area_height : y_offset + car_area_height + back_h, x_offset : x_offset + back_w] = back_flipped
    
#     # Place LEFT image (it needs to be rotated)
#     left_rotated = cv2.rotate(left_top_down, cv2.ROTATE_90_COUNTERCLOCKWISE)
#     birds_eye_view[y_offset : y_offset + left_h, x_offset - left_w : x_offset] = left_rotated

#     # Place RIGHT image (it needs to be rotated)
#     right_rotated = cv2.rotate(right_top_down, cv2.ROTATE_90_CLOCKWISE)
#     birds_eye_view[y_offset : y_offset + right_h, x_offset + car_area_width : x_offset + car_area_width + right_w] = right_rotated

#     # --- Optional: Add a car icon in the middle ---
#     car_icon = cv2.imread("car_icon.png") # Make sure you have this image
#     if car_icon is not None:
#         car_icon = cv2.resize(car_icon, (car_area_width, car_area_height))
#         birds_eye_view[y_offset:y_offset + car_area_height, x_offset:x_offset + car_area_width] = car_icon

#     # --- 5. Save and Display the Result ---
#     cv2.imwrite("birds_eye_view.png", birds_eye_view)
#     print("Bird's-eye view saved as 'birds_eye_view.png'")
    
    # cv2.imshow("Bird's Eye View", birds_eye_view)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()