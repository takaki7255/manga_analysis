def get_bboxs_inside_frame(frame_bbox, obj_bboxs, iou_threshold=0.5):
    frame_xmin = int(frame_bbox["xmin"])
    frame_ymin = int(frame_bbox["ymin"])
    frame_xmax = int(frame_bbox["xmax"])
    frame_ymax = int(frame_bbox["ymax"])

    bouded_obj_bboxs = []
    for obj_bbox in obj_bboxs:
        obj_xmin = int(obj_bbox["xmin"])
        obj_ymin = int(obj_bbox["ymin"])
        obj_xmax = int(obj_bbox["xmax"])
        obj_ymax = int(obj_bbox["ymax"])

        overlap_xmin = max(frame_xmin, obj_xmin)
        overlap_ymin = max(frame_ymin, obj_ymin)
        overlap_xmax = min(frame_xmax, obj_xmax)
        overlap_ymax = min(frame_ymax, obj_ymax)

        overlap_area = max(0, overlap_xmax - overlap_xmin) * max(0, overlap_ymax - overlap_ymin)
        obj_area = (obj_xmax - obj_xmin) * (obj_ymax - obj_ymin)
        iou = overlap_area / obj_area
        if iou >= iou_threshold:
            bouded_obj_bboxs.append(obj_bbox)
    return bouded_obj_bboxs