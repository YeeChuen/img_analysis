from io import BytesIO
from PIL import Image
import base64
import numpy as np
import math


def color_analysis_2(image_base64, percentage=10):
    # image_base64 = reduce_image_size(image_base64, int(percentage))

    img = Image.open(
        BytesIO(
            base64.b64decode(image_base64.split(",")[len(image_base64.split(",")) - 1])
        )
    )
    img = img.convert("RGB")

    image_array = np.array(img)

    # print("RGB array")
    # print(image_array)

    rgb_ypt = [[] for _ in range(6)]
    total = 0

    for row in image_array:
        for pixel in row:
            total += 1 
            # RGB (0, 1, 2)
            for i in range(3):
                if pixel[i] > 0: 
                    # rgb_ypt[i][0] += 1 # number of pixels
                    rgb_ypt[i].append(pixel[i]) # all intensity of that color

            # YPT (3, 4, 5)
            if pixel[0] > 0 and pixel[1] > 0: 
                # rgb_ypt[3][0] += 1 # R + G = Y
                rgb_ypt[3].append((pixel[0] + pixel[1]) / 2)

            if pixel[0] > 0 and pixel[2] > 0: 
                # rgb_ypt[4][0] += 1 # R + B = P
                rgb_ypt[4].append((pixel[0] + pixel[2]) / 2)

            if pixel[1] > 0 and pixel[2] > 0: 
                # rgb_ypt[5][0] += 1 # G + B = T
                rgb_ypt[5].append((pixel[1] + pixel[2]) / 2)

    color = ["Red   ", "Green ", "Blue  ", "Yellow", "Purple", "Teal  "]

    """ 
        min_intensity,
        max_intensity,
        round(mean_intensity / total, 2),
        total_intensity,
        percentage_intensity,
        round(num / total * 100, 2),
        num,
        total, 

        analysis = []
    """

    for i in range(len(rgb_ypt)):
        data = rgb_ypt[i]
        # print(f"Number of pixels {color[i]}", data[0])
        print(f"Pixels {color[i]}:", len(data))
        print(f"Sum    {color[i]}:", sum(data))

        rgb_ypt[i].sort()

    print(total)

    pass


def image_path_to_base64(image_path):

    upload_image = Image.open(image_path)
    buffered = BytesIO()
    upload_image.save(buffered, format="JPEG")
    upload_image_base64 = base64.b64encode(buffered.getvalue()).decode("ascii")

    return upload_image_base64


if __name__ == "__main__":
    image_path = "./Blank.jpg"

    analysis_object = color_analysis_2(image_path_to_base64(image_path))
