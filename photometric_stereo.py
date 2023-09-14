import cv2
import numpy as np

def photometric_stereo(images, light_directions):
    """
    Compute the normals of the surface using photometric stereo.

    Parameters:
    - images: List of images taken under different lighting conditions.
    - light_directions: Corresponding light directions for each image.

    Returns:
    - normals: The computed normals for the surface.
    """
    # Convert images to grayscale
    grayscale_images = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in images]

    # Stack grayscale images to form I matrix
    I = np.stack(grayscale_images, axis=-1)
    h, w, num_images = I.shape
    I = I.reshape(h * w, num_images)

    # Convert light directions to a matrix
    light_directions = np.array(light_directions)

    # Compute G matrix (Least squares solution)
    G = np.linalg.lstsq(light_directions, I.T, rcond=None)[0].T
    albedo = np.linalg.norm(G, axis=-1)

    epsilon = 1e-10  # A small constant to avoid division by zero
    albedo += epsilon

    normals = G / albedo[..., np.newaxis]

    # Set any NaN values in normals to a default value (e.g., [0, 0, 0])
    normals[np.isnan(normals)] = 0

    # Reshape the normals to the original image shape
    normals = normals.reshape(h, w, 3)

    return normals

def load_images_and_light_directions():
    """
    Load images and their corresponding light directions.
    Placeholder for now.

    Returns:
    - images: List of grayscale images.
    - light_directions: Corresponding light directions for each image.
    """
    # Placeholder: Load your images and light directions here
    images = []
    light_directions = []

    return images, light_directions

def test_photometric_stereo():
    """
    Test the photometric stereo implementation.
    """
    images, light_directions = load_images_and_light_directions()
    normals = photometric_stereo(images, light_directions)

    # Display the normals (for visualization purposes, you might want to map the normals to RGB space)
    cv2.imshow('Normals', normals)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Run the test
# test_photometric_stereo()