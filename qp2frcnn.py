import os
import pandas as pd
from shutil import copy


def build_datasets(srcroot, tgtroot, tagcsv, dsmap, classfile):

    # read data tag csv file
    df = pd.read_csv(tagcsv, header=None)

    for k, dsname in dsmap.items():
        tgtdir_img = os.path.join(tgtroot, dsname, 'images')
        tgtdir_ann = os.path.join(tgtroot, dsname, 'annotations')

        if not os.path.exists(tgtdir_img):
            os.makedirs(tgtdir_img)
        if not os.path.exists(tgtdir_ann):
            os.makedirs(tgtdir_ann)

        validrows = df[df[k].notna()]
        filenamelist = [os.path.join(srcroot, c, f) for c, f in zip(validrows[0], validrows[1])]

        # copy files
        for fname in filenamelist:
            copy(fname + '.jpg', tgtdir_img)
            copy(fname + '.anno', tgtdir_ann)

        # copy class file
        copy(classfile, os.path.join(tgtroot, dsname))

    print('file copy completed.')


if __name__ == '__main__':

    data_src_root = './sourcedata/export'
    data_tag_csv = './sourcedata/step2_DataTag.csv'
    classfile = './sourcedata/classes.json'

    data_tgt_root = './data_frcnn'

    dataset_map = {
        6: 'test75',
        7: 'train362',
        8: 'train320_16x20',
        9: 'train160_16x10',
        10: 'train160_8_20',
        11: 'train80_16x5',
        12: 'train80_8x10',
        13: 'train80_4x20',
        14: 'train40_16x2',
        15: 'train40_8x5',
        16: 'train40_4x10',
        17: 'train40_2x20',
    }

    # Arrange data according to the tag
    build_datasets(data_src_root, data_tgt_root, data_tag_csv, dataset_map, classfile)

