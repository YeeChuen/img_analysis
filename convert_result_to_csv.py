if __name__ == "__main__":
    file = "./Image_analysis_result.txt"

    with open(file, "r") as f:
        contents = f.readlines()

    count = 0
    indexes = []
    for i in range(len(contents)):
        if "./" in contents[i] and "control: " not in contents[i]:
            count += 1
            indexes.append(i)

    # print(len(indexes))

    image_analysis = []

    for i in range(len(indexes) - 1):
        image_analysis.append(contents[indexes[i] : indexes[i + 1]])

    image_analysis.append(contents[indexes[len(indexes) - 1] :])

    # print(image_analysis[0])

    for i in range(len(image_analysis)):
        image_analysis[i] = [x for x in image_analysis[i] if x != "\n"]

        for j in range(len(image_analysis[i])):
            image_analysis[i][j] = image_analysis[i][j].replace("\n", "")

    for analysis in image_analysis:
        # print(analysis)
        if len(analysis) != 29:
            raise ValueError("incorrect number of analysis in", analysis, len(analysis))

    with open("analysis_2.csv", "w") as f:
        for analysis in image_analysis:
            f.write("/".join(analysis[0].split("/")[-2:]) + ",")
            f.write("/".join(analysis[28].split("/")[-2:]) + ",") # <-- control image

            # print(analysis[1]) # <-- ignore
            
            # red
            f.write(analysis[2].split(": ")[-1] + ",") # <-- max
            f.write(analysis[3].split(": ")[-1] + ",") # <-- mean
            f.write(analysis[4].split(": ")[-1] + ",") # <-- median

            rgb = eval(analysis[5].split(": ")[-1])
            # f.write(f"\"rgb({rgb[0]},{rgb[1]},{rgb[2]})\"" + ",") # <-- RGB intensity
            f.write(f"{rgb[0]},{rgb[1]},{rgb[2]},") # <-- RGB intensity

            rgb_percent = eval(analysis[6].split(": ")[-1])
            f.write(f"{rgb_percent[0]}%,{rgb_percent[1]}%,{rgb_percent[2]}%,") # <-- RGB intensity

            f.write(analysis[7].split(": ")[-1] + ",") # <-- color percent
            f.write(analysis[8].split(": ")[-1] + ",") # <-- color pixels
            f.write(analysis[9].split(": ")[-1] + ",") # <-- total pixels

            
            # green
            f.write(analysis[11].split(": ")[-1] + ",") # <-- max
            f.write(analysis[12].split(": ")[-1] + ",") # <-- mean
            f.write(analysis[13].split(": ")[-1] + ",") # <-- median
            rgb = eval(analysis[14].split(": ")[-1])
            # f.write(f"\"rgb({rgb[0]},{rgb[1]},{rgb[2]})\"" + ",") # <-- RGB intensity
            f.write(f"{rgb[0]},{rgb[1]},{rgb[2]}" + ",") # <-- RGB intensity
            rgb_percent = eval(analysis[15].split(": ")[-1])
            # f.write(f"\"rgb({rgb_percent[0]}%,{rgb_percent[1]}%,{rgb_percent[2]}%)\"" + ",") # <-- RGB intensity
            f.write(f"{rgb_percent[0]}%,{rgb_percent[1]}%,{rgb_percent[2]}%" + ",") # <-- RGB intensity
            f.write(analysis[16].split(": ")[-1] + ",") # <-- color percent
            f.write(analysis[17].split(": ")[-1] + ",") # <-- color pixels
            f.write(analysis[18].split(": ")[-1] + ",") # <-- total pixels

            
            # yellow
            f.write(analysis[20].split(": ")[-1] + ",") # <-- max
            f.write(analysis[21].split(": ")[-1] + ",") # <-- mean
            f.write(analysis[22].split(": ")[-1] + ",") # <-- median
            rgb = eval(analysis[23].split(": ")[-1])
            # f.write(f"\"rgb({rgb[0]},{rgb[1]},{rgb[2]})\"" + ",") # <-- RGB intensity
            f.write(f"{rgb[0]},{rgb[1]},{rgb[2]}" + ",") # <-- RGB intensity
            rgb_percent = eval(analysis[24].split(": ")[-1])
            # f.write(f"\"rgb({rgb_percent[0]}%,{rgb_percent[1]}%,{rgb_percent[2]}%)\"" + ",") # <-- RGB intensity
            f.write(f"{rgb_percent[0]}%,{rgb_percent[1]}%,{rgb_percent[2]}" + ",") # <-- RGB intensity
            f.write(analysis[25].split(": ")[-1] + ",") # <-- color percent
            f.write(analysis[26].split(": ")[-1] + ",") # <-- color pixels
            f.write(analysis[27].split(": ")[-1] + ",") # <-- total pixels

            f.write("\n")
