from packages import get_framebbox, get_path_list, get_nonframebbox, get_bboxs_inside_frame, plot_bounded_obj_num

if __name__ == "__main__":
    bounded_bboxs_num = []
    all_path = get_path_list.get_path_list()
    for path in all_path:
        # if "ARMS" not in path:
        #     continue
        frame_bboxs = get_framebbox.get_framebbox(path)
        nonframe_bboxs = get_nonframebbox.get_nonframebbox(path)
        for index in frame_bboxs.keys():
            # print(index)
            for frame_bbox in frame_bboxs[index]:
                # print(frame_bbox["id"])
                bouded_nonframe_bboxs = get_bboxs_inside_frame.get_bboxs_inside_frame(frame_bbox, nonframe_bboxs[index])
                bounded_bboxs_num.append(bouded_nonframe_bboxs.__len__())
                # print(bouded_nonframe_bboxs.__len__())
                if len(bouded_nonframe_bboxs) >= 10:
                    print(path)
                    print(index)
                    print(frame_bbox["id"])
                    print(bouded_nonframe_bboxs.__len__())
                    print(bouded_nonframe_bboxs)
                    print("=================================")
                    break
    # print(bounded_bboxs_num)
    plot_bounded_obj_num.plot_bounded_obj_num(bounded_bboxs_num, "コマ内のオブジェクト数")