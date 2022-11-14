import re
import os


def caption_clean(caption_direct):
    with open(caption_direct, 'r') as file:
        data = file.read().splitlines()

    data = list(filter(lambda a: a != '', data))  # Remove '' from data list

    data_str = ' '.join(data)

    data_str = re.sub(r"(([0-9]{2}:){2}[0-9]{2}.[0-9]{3} -->)", "\\n\\1",
                      data_str, 0, re.MULTILINE)

    # Lines below remove the 1st line in data_str
    data_str_list = data_str.splitlines()
    data_str = '\n'.join(data_str_list[1:])
    return data_str


def time_str_to_sec(time_str):  # time_str is something like "00:00:14.080"
    hour, min, second = time_str.split(':')
    time_in_sec = int(hour) * 3600 + int(min) * 60 + float(second)
    return time_in_sec


def caption_to_label(caption_str):
    caption_list = caption_str.splitlines()
    out_str_list = []

    for time_caption in caption_list:
        time_caption_list = re.split(r"(?<=[0-9]{3})", time_caption)

        for idx, string in enumerate(time_caption_list):  # Remove all the
            # leading and trailing spaces around the strings
            time_caption_list[idx] = string.strip()
            # Now strings inside time_caption_list are all cleaned up

        for string in time_caption_list:
            start_time_str = time_caption_list[0]
            end_time_str = time_caption_list[1].strip('--> ')
            label_str = time_caption_list[2]

            start_time_str = str(time_str_to_sec(start_time_str))
            end_time_str = str(time_str_to_sec(end_time_str))

            line_str = '\t'.join([start_time_str, end_time_str, label_str])

        out_str_list.append(line_str)

    out_str = '\n'.join(out_str_list)
    return out_str


def main():
    input_caption_file = r".\audio\2022_11_13 Exhibition Tour—In " \
                         r"America-\manual_caption_en-US.txt"
    input_file_direct = os.path.dirname(input_caption_file)
    input_file_name = os.path.basename(input_caption_file)

    caption_str = caption_clean(input_caption_file)  # Every raw caption can
    # be a bit different, so you need to double-check on our output file
    # before importing it into audicity
    out_str = caption_to_label(caption_str)

    output_file_direct = os.path.join(input_file_direct,
                                      'cleaned_' + input_file_name)
    with open(output_file_direct, 'w') as file:
        file.write(out_str)
    # Then you import this label file into audicity with the vocals.wav
    # opened. You can now adjust on the labels relatively easier inside
    # audicity

    return 0


if __name__ == '__main__':
    main()
