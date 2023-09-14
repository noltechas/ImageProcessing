import cv2

def detect_body_parts(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours
    contours = [c for c in contours if cv2.contourArea(c) > 100]

    # Sort contours by area in descending order
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Assuming the largest contour is the torso
    torso = contours[0]
    cv2.drawContours(image, [torso], -1, (0, 255, 0), 2)

    # The head is likely to be a circular contour near the top
    for c in contours:
        (x, y), radius = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))
        if y < image.shape[0] * 0.25 and radius > 20:  # heuristic for top 25% of the image and reasonable radius
            cv2.circle(image, center, int(radius), (255, 0, 0), 2)
            break

    # Further processing for limbs, hands, and feet can be added using similar heuristics

    return image
