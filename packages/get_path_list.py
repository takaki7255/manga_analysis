import os

def get_path_list() -> list:
    manga109_path = "./../Manga109_released_2023_12_07/annotations/"
    file_list = os.listdir(manga109_path)
    path_list = []
    for file in file_list:
        if file.endswith(".xml"):
            path = os.path.join(manga109_path, file)
            path_list.append(path)
    path_list.sort()
    return path_list