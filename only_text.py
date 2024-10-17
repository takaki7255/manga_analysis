from packages import get_framebbox, get_path_list, get_textbbox, get_bboxs_inside_frame, plot_bounded_obj_num, calc_stats

if __name__ == "__main__":
    bounded_text_bboxs_num = []
    all_path = get_path_list.get_path_list()
    for path in all_path:
        frame_bboxs = get_framebbox.get_framebbox(path)
        text_bboxs = get_textbbox.get_textbbox(path)
        for index in frame_bboxs.keys():
            for frame_bbox in frame_bboxs[index]:
                bouded_text_bboxs = get_bboxs_inside_frame.get_bboxs_inside_frame(frame_bbox, text_bboxs[index])
                bounded_text_bboxs_num.append(bouded_text_bboxs.__len__())
                
                # if len(bouded_text_bboxs) == 0:
                #     print(path)
                #     print(index)
                #     print(frame_bbox)
                #     print(bouded_text_bboxs.__len__())
                #     print(bouded_text_bboxs)
                #     print("=================================")
                #     # draw_bbox_and_show.draw_bbox_and_show(path, index, frame_bbox, nonframe_bboxs[index])
    calc_stats.calc_stats(bounded_text_bboxs_num, "bounded_text_num")
    plot_bounded_obj_num.plot_bounded_obj_num(bounded_text_bboxs_num, "コマ内のテキスト数","bounded_text_num")