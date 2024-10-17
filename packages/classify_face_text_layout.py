def classify_face_text_layout(face_bbox, text_bboxs):
    face_xmin = face_bbox["xmin"]
    face_ymin = face_bbox["ymin"]
    face_xmax = face_bbox["xmax"]
    face_ymax = face_bbox["ymax"]
    
    text1_xmin = int(text_bboxs[0]["xmin"])
    text1_ymin = int(text_bboxs[0]["ymin"])
    text1_xmax = int(text_bboxs[0]["xmax"])
    text1_ymax = int(text_bboxs[0]["ymax"])
    
    text2_xmin = int(text_bboxs[1]["xmin"])
    text2_ymin = int(text_bboxs[1]["ymin"])
    text2_xmax = int(text_bboxs[1]["xmax"])
    text2_ymax = int(text_bboxs[1]["ymax"])
    
    face_center_x = (int(face_xmin) + int(face_xmax)) / 2
    face_center_y = (int(face_ymin) + int(face_ymax)) / 2
    text1_center_x = (text1_xmin + text1_xmax) / 2
    text1_center_y = (text1_ymin + text1_ymax) / 2
    text2_center_x = (text2_xmin + text2_xmax) / 2
    text2_center_y = (text2_ymin + text2_ymax) / 2
    
    # テキストがキャラクターの左右どちらにあるか判定
    text_left = min(text1_center_x, text2_center_x) < face_center_x
    text_right = max(text1_center_x, text2_center_x) > face_center_x

    # 位置関係の判定
    if text_left and text_right:
        return "tct"
    elif text_left:
        return "ttc"
    elif text_right:
        return "ctt"
    else:
        return "不明な配置"