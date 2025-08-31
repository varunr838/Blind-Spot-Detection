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
    width, height = 1280, 720

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
    img1 = cv2.imread("car_images/img1.jpg")
    img2 = cv2.imread("car_images/img2.jpg")

    # --- 2. DEFINE YOUR PERSPECTIVE POINTS (CRITICAL STEP!) ---
    # These are placeholder values! You MUST find the correct points for YOUR cameras.
    # The points should form a trapezoid on the ground in front of each camera.
    # Format: np.float32([[top_left], [top_right], [bottom_right], [bottom_left]])
    
    src_img1 = np.float32([(399, 457), (802, 467), (920, 717), (163, 717)])

    src_img2 = np.float32([(490, 579), (790, 581), (831, 691), (458, 692)])

    # --- 3. Apply the top-down warp to each image ---
    img1_top_down = get_top_down_view(img1, src_img1)
    img2_top_down = get_top_down_view(img2, src_img2)

    # --- 4. Combine the images into a single bird's-eye view ---
#     img1_rotated = cv2.rotate(img1_top_down, cv2.ROTATE_90_COUNTERCLOCKWISE)
#     img2_rotated = cv2.rotate(img2_top_down, cv2.ROTATE_90_CLOCKWISE)
    # Horizontally stack the two images together
    cv2.imwrite("img1_top_down.png",img1_top_down)
    birds_eye_view = np.hstack((img1_top_down, img2_top_down))

    # --- 5. Save and Display the Result ---
    cv2.imwrite("birds_eye_view.png", birds_eye_view)
    print("Bird's-eye view saved as 'birds_eye_view.png'")
    
    # cv2.imshow("Bird's Eye View", birds_eye_view)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()