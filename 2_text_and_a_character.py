from packages import get_path_list, get_framebbox, get_textbbox,calc_stats,plot_bounded_obj_num,get_bboxs_inside_frame, get_facebbox, draw_bbox_and_show, classify_face_text_layout, plot_layout
#吹き出し2つとキャラ1人の場合の位置関係の調査
if __name__ == "__main__":
    framebboxs_num = 0
    count = 0
    bounded_text_bboxs_num = []
    bounded_face_bboxs_num = []
    face_text_layout = []
    all_path = get_path_list.get_path_list()
    for path in all_path:
        frame_bboxs = get_framebbox.get_framebbox(path)
        face_bboxs = get_facebbox.get_facebbox(path)
        text_bboxs = get_textbbox.get_textbbox(path)
        for index in frame_bboxs.keys():
            for frame_bbox in frame_bboxs[index]:
                framebboxs_num += 1
                bouded_text_bboxs = get_bboxs_inside_frame.get_bboxs_inside_frame(frame_bbox, text_bboxs[index])
                bounded_face_bboxs = get_bboxs_inside_frame.get_bboxs_inside_frame(frame_bbox, face_bboxs[index])
                # 吹き出し2つとキャラ1人の場合
                if len(bouded_text_bboxs) == 2:
                    if len(bounded_face_bboxs) == 1:
                        count += 1
                        # print(bouded_text_bboxs)
                        # print(bounded_face_bboxs)
                        # draw_bbox_and_show.draw_bbox_and_show(path, index, frame_bbox, bouded_text_bboxs)
                        # draw_bbox_and_show.draw_bbox_and_show(path, index, frame_bbox, bounded_face_bboxs)
                        # print(classify_face_text_layout.classify_face_text_layout(bounded_face_bboxs[0], bouded_text_bboxs))
                        face_text_layout.append(classify_face_text_layout.classify_face_text_layout(bounded_face_bboxs[0], bouded_text_bboxs))
    percent = count/framebboxs_num * 100
    print(f'吹き出し2つとキャラ1人の場合の全体に占める割合: {percent}%')
    plot_layout.plot_layout(face_text_layout,'コマ内キャラクタと吹き出しの位置関係', 'layout')