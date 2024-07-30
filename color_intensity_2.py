from io import BytesIO
from PIL import Image
import base64
import numpy as np
import math


def color_analysis(image_base64, percentage=10):
    # image_base64 = reduce_image_size(image_base64, int(percentage))

    img = Image.open(
        BytesIO(
            base64.b64decode(image_base64.split(",")[len(image_base64.split(",")) - 1])
        )
    )
    img = img.convert("RGB")
    red_g, green_g, blue_g = img.split()

    red = get_combined_intensity_n_pixels(red_g, None, None, id="red")
    green = get_combined_intensity_n_pixels(None, green_g, None, id="green")
    blue = get_combined_intensity_n_pixels(None, None, blue_g, id="blue")

    red_stats = get_color_intensity_n_pixels(red, 1)
    green_stats = get_color_intensity_n_pixels(green, 1)
    blue_stats = get_color_intensity_n_pixels(blue, 1)

    yellow = get_combined_intensity_n_pixels(red_g, green_g, None, id="yellow")
    purple = get_combined_intensity_n_pixels(red_g, None, blue_g, id="purple")
    teal = get_combined_intensity_n_pixels(None, green_g, blue_g, id="teal")

    yellow_stats = get_color_intensity_n_pixels(yellow, 2)
    purple_stats = get_color_intensity_n_pixels(purple, 2)
    teal_stats = get_color_intensity_n_pixels(teal, 2)

    # red.save("red.jpg")
    # green.save("green.jpg")
    # blue.save("blue.jpg")
    # yellow.save("yellow.jpg")
    # purple.save("purple.jpg")
    # teal.save("teal.jpg")

    add_base64_to_list(red_stats, red)
    add_base64_to_list(green_stats, green)
    add_base64_to_list(blue_stats, blue)
    add_base64_to_list(yellow_stats, yellow)
    add_base64_to_list(purple_stats, purple)
    add_base64_to_list(teal_stats, teal)

    analysis_object = {}
    analysis_object["red"] = stats_to_dict(red_stats)
    analysis_object["green"] = stats_to_dict(green_stats)
    analysis_object["blue"] = stats_to_dict(blue_stats)
    analysis_object["yellow"] = stats_to_dict(yellow_stats)
    analysis_object["purple"] = stats_to_dict(purple_stats)
    analysis_object["teal"] = stats_to_dict(teal_stats)

    return analysis_object


def stats_to_dict(stats):
    stats_dict = {}
    stats_dict["min"] = str(stats[0])
    stats_dict["max"] = str(stats[1])
    stats_dict["mean"] = str(stats[2])
    stats_dict["rgbIntensity"] = stats[3]
    stats_dict["rgbPercentIntensity"] = stats[4]
    stats_dict["percentage"] = str(stats[5])
    stats_dict["colorPixels"] = str(stats[6])
    stats_dict["totalPixels"] = str(stats[7])
    stats_dict["median"] = str(stats[8])
    stats_dict["base64"] = stats[9]

    return stats_dict


def get_color_intensity_n_pixels(image_ori, channel):
    image_array = np.array(image_ori)

    num = 0
    total = 0
    total_intensity = [0, 0, 0]

    min_intensity = 255
    max_intensity = 0
    mean_intensity = 0

    # for median
    intensity_list = []

    for row in image_array:
        for x in row:
            channel_sum = np.sum(x, dtype=np.int32)
            if channel_sum > 0:
                num += 1

            min_intensity = min(min_intensity, channel_sum / channel)
            max_intensity = max(max_intensity, channel_sum / channel)
            mean_intensity += channel_sum / channel

            # median
            intensity_list.append(channel_sum / channel)

            total += 1
            total_intensity[0] += x[0]
            total_intensity[1] += x[1]
            total_intensity[2] += x[2]

    intensity_sum = sum(total_intensity)
    percentage_intensity = [
        round(total_intensity[0] / intensity_sum * 100, 2),
        round(total_intensity[1] / intensity_sum * 100, 2),
        round(total_intensity[2] / intensity_sum * 100, 2),
    ]

    return [
        min_intensity,
        max_intensity,
        round(mean_intensity / total, 2), # mean
        total_intensity, # rgb(total intensity, total intensity, total intensity)
        percentage_intensity, # rgb(%,%,%)
        round(num / total * 100, 2), # the percentage of the color pixels over 
        num, # number of pixels of this color
        total, # the total pixels
        np.median(intensity_list), # median
    ]


def get_combined_intensity_n_pixels(r, g, b, only_combined=True, id=0):
    if r and g and b:
        raise ValueError("Not allow all channels.")

    temp_img = r or g or b
    width, height = temp_img.size
    empty_channel = np.zeros((height, width), dtype=np.uint8)
    empty_channel_img = Image.fromarray(empty_channel)

    if only_combined:
        grey_combined = get_combined_strict(r, g, b, id)
    else:
        combined_img = Image.merge(
            "RGB",
            (r or empty_channel_img, g or empty_channel_img, b or empty_channel_img),
        )
        grey_combined = combined_img.convert("L")

    return grey_combined


def get_combined_strict(r, g, b, id=0):  # only 2 channel
    temp_img = r or g or b
    width, height = temp_img.size

    channels = [r, g, b]
    empty_channel = np.zeros((height, width), dtype=np.uint8)
    num_none = 0
    array_channels = []
    for elem in channels:
        if elem == None:
            num_none += 1
            array_channels.append(empty_channel)
        else:
            array_channels.append(np.array(elem))

    for i in range(len(empty_channel)):
        for j in range(len(empty_channel[i])):
            triplet = [
                array_channels[0][i][j],
                array_channels[1][i][j],
                array_channels[2][i][j],
            ]
            zeros = triplet.count(0)

            if zeros >= 1 + num_none:
                array_channels[0][i][j] = 0
                array_channels[1][i][j] = 0
                array_channels[2][i][j] = 0

    combined_img = Image.merge(
        "RGB",
        (
            Image.fromarray(array_channels[0]),
            Image.fromarray(array_channels[1]),
            Image.fromarray(array_channels[2]),
        ),
    )
    return combined_img


def add_base64_to_list(list, image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("ascii")

    list.append("data:image/jpg;base64," + image_base64)


def print_color_stats(color, stats):
    print(f"{color} stats:")
    print(f"    intensity (min): ", stats["min"])
    print(f"    intensity (max): ", stats["max"])
    print(f"    intensity (mean): ", stats["mean"])
    print(f"    total intensity: ", stats["rgbIntensity"])
    print(f"    total intensity %: ", stats["rgbPercentIntensity"])
    print(f"    color percent: ", str(stats["percentage"]) + "%")
    print(f"    color pixel: ", stats["colorPixels"])
    print(f"    total pixel: ", stats["totalPixels"])


def image_path_to_base64(image_path):

    upload_image = Image.open(image_path)
    buffered = BytesIO()
    upload_image.save(buffered, format="JPEG")
    upload_image_base64 = base64.b64encode(buffered.getvalue()).decode("ascii")

    return upload_image_base64



if __name__ == "__main__":
    image_path = "./jay_test_pic.jpg"

    analysis_object = color_analysis(image_path_to_base64(image_path))


    print_color_stats("red", analysis_object["red"])
    print_color_stats("green", analysis_object["green"])
    print_color_stats("blue", analysis_object["blue"])
    print_color_stats("yellow", analysis_object["yellow"])
    print_color_stats("purple", analysis_object["purple"])
    print_color_stats("teal", analysis_object["teal"])
