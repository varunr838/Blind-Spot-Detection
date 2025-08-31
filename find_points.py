import cv2
import argparse

# Global variables to store points
points = []

def mouse_callback(event, x, y, flags, param):
    """
    Mouse callback function to capture clicks.
    Appends the (x, y) coordinates to the global 'points' list on left-click.
    """
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        # Append the clicked point
        points.append((x, y))
        
        # Draw a circle on the image to show where we clicked
        cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
        
        print(f"Point {len(points)} added: ({x}, {y})")

        # If we have 4 points, print the final array and instructions
        if len(points) == 4:
            print("\n--- 4 points selected ---")
            print("Copy the NumPy array below into your main script:\n")
            # Format the output as a NumPy array for easy copy-pasting
            print(f"np.float32({points})")
            print("\nPress any key to close the image.")

# --- Main execution ---
# Set up argument parser to accept image path from command line
parser = argparse.ArgumentParser(description="Click to find 4 source points for perspective transform.")
parser.add_argument("-i", "--image", required=True, help="Path to the calibration image")
args = vars(parser.parse_args())

# Load the image
image_path = args["image"]
image = cv2.imread(image_path)
clone = image.copy() # Keep a clean copy of the original image

# Create a window and set the mouse callback function
cv2.namedWindow("Click to select points")
cv2.setMouseCallback("Click to select points", mouse_callback)

print("Please click on the 4 corners of the calibration object in order:")
print("1. Top-left")
print("2. Top-right")
print("3. Bottom-right")
print("4. Bottom-left")
print("\nClose the window when you are done.")

# Keep the window open until a key is pressed
while True:
    cv2.imshow("Click to select points", image)
    key = cv2.waitKey(1) & 0xFF
    # If we have 4 points, wait for any key press to exit
    if len(points) == 4:
        if cv2.waitKey(0):
            break
    # Allow resetting if 'r' is pressed
    elif key == ord("r"):
        image = clone.copy()
        points = []

cv2.destroyAllWindows()