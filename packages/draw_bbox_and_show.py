import cv2
import numpy as np

def draw_bbox_and_show(path, index, frame, bboxes):
    index = str(index).zfill(3)
    title = path.split("/")[-1].split(".")[0]
    # 画像のパスを生成
    img_path = f"./../Manga109_released_2023_12_07/images/{title}/{index}.jpg"
    img = cv2.imread(img_path)
    if img is None:
        print("画像が読み込めませんでした")
        return
    frame_xmin = int(frame["xmin"])
    frame_ymin = int(frame["ymin"])
    frame_xmax = int(frame["xmax"])
    frame_ymax = int(frame["ymax"])
    cv2.rectangle(img, (frame_xmin, frame_ymin), (frame_xmax, frame_ymax), (0, 255, 0), 2)

    for bbox in bboxes:
        xmin = int(bbox["xmin"])
        ymin = int(bbox["ymin"])
        xmax = int(bbox["xmax"])
        ymax = int(bbox["ymax"])
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
        
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



# if __name__ == "__main__":
#     path = "./../../Manga109_released_2023_12_07/annotations/YumeiroCooking.xml"
#     index = 78
#     frame = {'type': 'frame', 'id': '000818ee', 'xmin': '36', 'ymin': '2', 'xmax': '740', 'ymax': '817'}
#     bboxes = [{'type': 'face', 'id': '000818d6', 'xmin': '554', 'ymin': '112', 'xmax': '612', 'ymax': '163'}, {'type': 'text', 'id': '000818d7', 'xmin': '462', 'ymin': '257', 'xmax': '518', 'ymax': '343'}, {'type': 'face', 'id': '000818da', 'xmin': '611', 'ymin': '195', 'xmax': '648', 'ymax': '246'}, {'type': 'text', 'id': '000818db', 'xmin': '640', 'ymin': '404', 'xmax': '702', 'ymax': '502'}, {'type': 'face', 'id': '000818dc', 'xmin': '350', 'ymin': '78', 'xmax': '381', 'ymax': '103'}, {'type': 'text', 'id': '000818ec', 'xmin': '194', 'ymin': '32', 'xmax': '221', 'ymax': '126'}, {'type': 'face', 'id': '000818f0', 'xmin': '64', 'ymin': '367', 'xmax': '210', 'ymax': '490'}, {'type': 'text', 'id': '000818f3', 'xmin': '682', 'ymin': '98', 'xmax': '717', 'ymax': '163'}, {'type': 'text', 'id': '000818f4', 'xmin': '384', 'ymin': '245', 'xmax': '417', 'ymax': '349'}, {'type': 'text', 'id': '00081901', 'xmin': '355', 'ymin': '652', 'xmax': '394', 'ymax': '769'}, {'type': 'face', 'id': '00081902', 'xmin': '507', 'ymin': '586', 'xmax': '689', 'ymax': '813'}, {'type': 'face', 'id': '00081903', 'xmin': '304', 'ymin': '60', 'xmax': '331', 'ymax': '81'}, {'type': 'face', 'id': '0008190a', 'xmin': '242', 'ymin': '74', 'xmax': '263', 'ymax': '92'}]
#     draw_bbox_and_show(path, index, frame, bboxes)