import os
import cv2


celltypes = {'Erythrocyte': 0,
             'Lymphocyte': 1,
             'Mononuclear cell': 2,
             'Neutrophil': 3}

# BGR order
color_map = {
    0: (0, 0, 255),     # Erythrocyte
    1: (0, 255, 0),     # Lymphocyte
    2: (255, 0, 0),     # Mononuclear
    3: (0, 180, 180)    # Neutrophil
}


def show_labeled_img(listfile, idxs, dir_prefix='', thresh=0.02, print_score=True, save_dir=None):
    with open(listfile, 'r') as fp:
        lines = fp.readlines()

    if idxs is None:
        idxs = range(len(lines))

    for idx in idxs:
        line = lines[idx]
        data = line.split()

        imgfile = dir_prefix + data[0]
        img = cv2.imread(imgfile)

        for j in range(1, len(data)):
            boxinfo = data[j].split(',')
            pts = [int(v) for v in boxinfo[0:4]]
            color = color_map[int(boxinfo[4])]

            if len(boxinfo) >= 6:
                score = float(boxinfo[5])
                if score < thresh:
                    continue
                if print_score:
                    cv2.putText(img, '%.1f' % (score*100), (pts[0], pts[1]-2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1)

            cv2.rectangle(img, (pts[0], pts[1]), (pts[2], pts[3]), color)

        img = cv2.resize(img, dsize=(1088, 1088), interpolation=cv2.INTER_LINEAR)

        if save_dir is not None:
            if not os.path.isdir(save_dir):
                os.mkdir(save_dir)

            outfile = os.path.basename(imgfile)
            name, ext = os.path.splitext(outfile)
            outfile = name + '_out' + ext
            outfile = os.path.join(save_dir, outfile)

            cv2.imwrite(outfile, img)
            print('image saved:', outfile)

        else:
            cv2.imshow('image', img)
            cv2.waitKey()

    cv2.destroyAllWindows()


if __name__ == '__main__':

    # check result
    # datafile = 'kerasYOLO/data_yolo/test.txt'
    # datafile = 'kerasYOLO/result/abs_320_16x20_yolo3_mbnl_7295/result/detection_result.txt'
    datafile = 'kerasYOLO/result/362_23_y3_darkspp_b8_8706/result75/detection_result.txt'

    showrange = None

    # savedir = None
    # savedir = 'kerasYOLO/data_yolo/test_labeled'
    savedir = 'kerasYOLO/result/362_23_y3_darkspp_b8_8706/result75/detection_result'

    show_labeled_img(datafile, showrange, dir_prefix='./kerasYOLO/', thresh=0.5, print_score=False, save_dir=savedir)
