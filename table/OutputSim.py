from table.Output import Output
import numpy as np
import cv2


class OutputSim(Output):
    def __init__(self, rows=12, columns=12):
        super().__init__(rows=rows, columns=columns)

    def show(self):
        # Copy pixel_matrix into OpenCV-compatible image
        img = np.zeros((12, 12, 3), dtype=np.uint8)
        for r in range(12):
            for c in range(12):
                # Color order is different in opencv
                img[r, c, 2] = self.pixel_matrix[c][r][0]
                img[r, c, 1] = self.pixel_matrix[c][r][1]
                img[r, c, 0] = self.pixel_matrix[c][r][2]

        # Resize for better visibility
        img_resize = cv2.resize(img, (480, 480), interpolation=cv2.INTER_NEAREST)
        cv2.imshow('table', img_resize)
        cv2.waitKey(25)