import os
from color_intensity_2 import image_path_to_base64, color_analysis

from tqdm import tqdm


def get_all_image(folder_path):
    done = False
    paths = [folder_path]
    images = []

    while not done:
        path = paths.pop()

        images += [f"{path}/{x}" for x in os.listdir(path)]

        for image in images:
            if (
                image[-4:] != ".tif"
                and image[-4:] != ".png"
                and image[-4:] != ".jpg"
                and image[-4:] != ".jpeg"
                and not os.path.isfile(image)
            ):
                paths.append(image)

        if not paths:
            done = True

        for path in paths:
            if path in images:
                images.remove(path)

    return images


def write_to_result(str):
    with open("Image_analysis_result.txt", "a") as f:
        f.write(str)


def write_stats_to_result(color, stats):
    with open("Image_analysis_result.txt", "a") as f:
        f.write(f"{color} stats:")
        f.write(f"    intensity (min): " + str(stats["min"]) + "\n")
        f.write(f"    intensity (max): " + str(stats["max"]) + "\n")
        f.write(f"    intensity (mean): " + str(stats["mean"]) + "\n")
        f.write(f"    intensity (median): " + str(stats["median"]) + "\n")
        f.write(f"    total intensity: " + str(stats["rgbIntensity"]) + "\n")
        f.write(f"    total intensity %: " + str(stats["rgbPercentIntensity"]) + "\n")
        f.write(f"    color percent: " + str(stats["percentage"]) + "%" + "\n")
        f.write(f"    color pixel: " + str(stats["colorPixels"]) + "\n")
        f.write(f"    total pixel: " + str(stats["totalPixels"]) + "\n" + "\n")


def normalize(analysis, control_analysis):
    normalized = {}
    # min, max, mean, median, percentage. colorPixels, totalPixels is not normalize
    normalized["min"] = analysis["min"]
    normalized["max"] = analysis["max"]
    normalized["mean"] = analysis["mean"]
    normalized["median"] = analysis["median"]
    normalized["percentage"] = analysis["percentage"]
    normalized["colorPixels"] = analysis["colorPixels"]
    normalized["totalPixels"] = analysis["totalPixels"]

    # only normalize intensity number
    # rgbIntensity and rgbPercentIntensity
    # [0, 898128, 0]
    normalized["rgbIntensity"] = [
        analysis["rgbIntensity"][0] - control_analysis["rgbIntensity"][0],
        analysis["rgbIntensity"][1] - control_analysis["rgbIntensity"][1],
        analysis["rgbIntensity"][2] - control_analysis["rgbIntensity"][2],
    ]
    normalized["rgbPercentIntensity"] = [
        analysis["rgbPercentIntensity"][0] - control_analysis["rgbPercentIntensity"][0],
        analysis["rgbPercentIntensity"][1] - control_analysis["rgbPercentIntensity"][1],
        analysis["rgbPercentIntensity"][2] - control_analysis["rgbPercentIntensity"][2],
    ]
    # normalized["rgbPercentIntensity"] = [0, 0, 0]
    # print(control_analysis["rgbIntensity"])
    # control_analysis["rgbPercentIntensity"]

    return normalized


if __name__ == "__main__":
    image_path = "./image_analysis"

    # images = [f"{image_path}/{x}" for x in os.listdir(image_path)]

    # paths = []

    # for image in images:
    #     if image[-4:] != ".tif":
    #         paths.append(image)

    # for i in range(len(paths)):
    #     path = paths[i]
    #     images.remove(path)

    #     new_images = [f"{path}/{x}" for x in os.listdir(path)]

    #     images += new_images

    #     new_paths = []
    #     for new_image in new_images:
    #         if image[-4:] != ".tif":
    #             new_paths.append(image)

    # print(images)

    image_files = get_all_image(image_path)
    print(len(image_files))

    with open("Image_analysis_result.txt", "w") as f:
        f.write("")

    control_images = [img for img in image_files if "control" in img]
    # print(control_images)

    for image in tqdm(image_files):
        image_base64 = image_path_to_base64(image)
        write_to_result(image + "\n")
        analysis_object = color_analysis(image_base64, percentage=100)

        for control_img in control_images:
            control_base_64 = image_path_to_base64(control_img)
            control = color_analysis(control_base_64, percentage=100)

            write_stats_to_result(
                "red", normalize(analysis_object["red"], control["red"])
            )
            write_stats_to_result(
                "green", normalize(analysis_object["green"], control["green"])
            )
            write_stats_to_result(
                "yellow", normalize(analysis_object["yellow"], control["yellow"])
            )
            # write_stats_to_result("green", analysis_object["green"])
            # write_stats_to_result("yellow", analysis_object["yellow"])

            write_to_result(f"control: {control_img}" + "\n" + "\n")
