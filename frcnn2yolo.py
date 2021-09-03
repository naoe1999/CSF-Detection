import os
import cv2
import json
from glob import glob


def convert_ds(imgdir, anndir, tgtdir, cellcode, imsize):
    # list image & annotation
    imgfiles = sorted(glob(os.path.join(imgdir, '*.jpg')))
    annfiles = sorted(glob(os.path.join(anndir, '*.anno')))
    assert len(imgfiles) == len(annfiles)

    # make target dir
    if not os.path.exists(tgtdir):
        os.makedirs(tgtdir)

    new_annotation = {}  # {filename: [xmin,ymin,xmax,ymax,clsid], ...}

    for imgf, annf in zip(imgfiles, annfiles):

        # load image
        img = cv2.imread(imgf)

        # resize image
        h, w = img.shape[0:2]
        hrate = imsize[1] / h
        wrate = imsize[0] / w
        imgr = cv2.resize(img, imsize)

        # load annotation
        with open(annf, 'r') as fp:
            anno = json.load(fp)

        # apply resize factor to annotation
        imgr_anns = []
        for clsstr, boxes in anno.items():
            for box in boxes:
                xmin = round(box[0] * wrate)
                ymin = round(box[1] * hrate)
                xmax = round(box[2] * wrate)
                ymax = round(box[3] * hrate)
                imgr_anns.append([xmin, ymin, xmax, ymax, cellcode[clsstr]])

        # new image file path
        imgrf = os.path.join(tgtdir, os.path.basename(imgf))

        # save resized image to destination dir
        cv2.imwrite(imgrf, imgr)

        # store modified annotations to dictionary
        new_annotation[imgrf] = imgr_anns

    # write list as YOLO annotation file
    new_anno_file = tgtdir + '.txt'
    with open(new_anno_file, 'w') as fp:
        for imgfile, anns in new_annotation.items():
            anno_line = " ".join([",".join([str(el) for el in ann]) for ann in anns])
            anno_line = imgfile + " " + anno_line + "\n"
            fp.write(anno_line)

    print(new_anno_file + ' saved.')


def convert_datasets(srcroot, tgtroot, cellcode, imsize):

    dsdirs = [ds for ds in sorted(os.listdir(srcroot)) if os.path.isdir(os.path.join(srcroot, ds))]

    imgdirs = [os.path.join(srcroot, ds, 'images') for ds in dsdirs]
    anndirs = [os.path.join(srcroot, ds, 'annotations') for ds in dsdirs]
    tgtdirs = [os.path.join(tgtroot, ds) for ds in dsdirs]

    for imgdir, anndir, tgtdir in zip(imgdirs, anndirs, tgtdirs):
        convert_ds(imgdir, anndir, tgtdir, cellcode, imsize)

    print('done.')


if __name__ == '__main__':

    cell_code = {'Erythrocyte': 0,
                 'Lymphocyte': 1,
                 'Mononuclear cell': 2,
                 'Neutrophil': 3}

    img_size = (544, 544)  # width, height


    ##### convert all datasets

    data_src_root = './FRCNN/data_frcnn'
    data_tgt_root = './data_yolo'

    convert_datasets(data_src_root, data_tgt_root, cell_code, img_size)


    ##### convert one dataset

    # img_dir = './data_frcnn/train362/images'
    # ann_dir = './data_frcnn/train362/annotations'
    # tgt_dir = './data_yolo/train362'
    #
    # convert_ds(img_dir, ann_dir, tgt_dir, cell_code, img_size)

