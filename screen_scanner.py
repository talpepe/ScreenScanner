import cv2
import numpy as np
from mss import mss
import time

class ScreenScanner:
    def __init__(self, templates, mon, window_size=10, tolerance=0.30):
        self.processed_templates = []
        print("IN INIT AHAHA")
        for temp in templates:
            template = cv2.imread(temp.get_image_path())
            print("IN INIT loop AHAHA")
            if template is None:
                raise ValueError(f"Could not load template at {template}")
            template = cv2.Canny(template, 50, 150)
            cv2.imshow('', template)
            h, w = template.shape[:2]
            self.processed_templates.append((template, h, w))

        self.mon = mon
        self.window_size = window_size
        self.tolerance = tolerance
        self.running_average_arr = [0.0] * window_size
        self.sct = mss()

    def start_scanning(self):
        while True:
            last_time = time.time()
            img = self.sct.grab(self.mon)
            img = np.array(img)
            edged = cv2.Canny(img, 50, 150)

            found = None
            max_vals = []

            for template, h, w in self.processed_templates:
                result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
                _, maxVal, _, maxLoc = cv2.minMaxLoc(result)
                max_vals.append(maxVal)

                if maxVal > self.tolerance:
                    startX, startY = int(maxLoc[0]), int(maxLoc[1])
                    endX, endY = int((maxLoc[0] + w)), int((maxLoc[1] + h))
                    cv2.rectangle(img, (startX, startY), (endX, endY), (180, 105, 255), 2)


            print('The loop took: {0}'.format(time.time() - last_time))
            print(f"Max Vals: {max_vals}")

            cv2.imshow('test', np.array(img))

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

# Example usage:
# templates = ["template1.png", "template2.png"]
# mon = {"top": 0, "left": 0, "width": 800, "height": 600}
# scanner = ScreenScanner(templates, mon)
# scanner.start_scanning()


# Example usage:
# if __name__ == "__main__":
#     scanner = ScreenScanner(template_path="./images/fass4.png", mon={"top": 0, "left": 2500, "width": 900, "height": 300})
#     scanner.start_scanning()
