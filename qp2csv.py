import os
import json
import csv
from glob import glob


# def count_cells(dataroot, celltypes, csvout):
#     cellcount = {}
#
#     # explore data folder and analyze
#     cases = sorted(os.listdir(dataroot))
#
#     for c in cases:
#         casedir = os.path.join(dataroot, c)
#
#         if os.path.isdir(casedir):
#             imgpaths = sorted(glob(os.path.join(casedir, '*.jpg')))
#             annopaths = sorted(glob(os.path.join(casedir, '*.anno')))
#             assert len(imgpaths) == len(annopaths)
#
#             num_regions = len(imgpaths)
#             num_cells = [0 for _ in celltypes]
#
#             for i, ap in enumerate(annopaths):
#                 assert os.path.splitext(os.path.basename(ap))[0] == \
#                        os.path.splitext(os.path.basename(imgpaths[i]))[0]
#
#                 with open(ap, 'r') as annofile:
#                     anno = json.load(annofile)
#
#                     for j, cell in enumerate(celltypes):
#                         if cell in anno:
#                             num_cells[j] += len(anno[cell])
#
#             cellcount[c] = (num_regions, num_cells)
#
#     print('data structure analyzed.')
#
#     # write csv file
#     with open(csvout, 'w') as fp:
#         wr = csv.writer(fp)
#
#         for c, (nr, nc) in sorted(cellcount.items()):
#             wr.writerow([c, nr] + nc)
#
#     print('csv file created.')


def count_cells(dataroot, celltypes, csvout):
    casedict = {}

    # explore data folder and analyze
    cases = sorted(os.listdir(dataroot))

    for c in cases:
        casedir = os.path.join(dataroot, c)

        if os.path.isdir(casedir):
            imgpaths = sorted(glob(os.path.join(casedir, '*.jpg')))
            annopaths = sorted(glob(os.path.join(casedir, '*.anno')))
            assert len(imgpaths) == len(annopaths)

            regiondict = {}

            for imgp, annop in zip(imgpaths, annopaths):
                region = os.path.splitext(os.path.basename(imgp))[0]
                assert region == os.path.splitext(os.path.basename(annop))[0]

                with open(annop, 'r') as annofile:
                    anno = json.load(annofile)

                num_cells = [0 for _ in celltypes]
                for j, cell in enumerate(celltypes):
                    if cell in anno:
                        num_cells[j] += len(anno[cell])

                regiondict[region] = num_cells

            casedict[c] = regiondict

    print('data structure analyzed.')

    # write csv file
    with open(csvout, 'w') as fp:
        wr = csv.writer(fp)

        for c, rd in sorted(casedict.items()):
            for r, d in sorted(rd.items()):
                wr.writerow([c, r] + d)

    print('csv file created.')


if __name__ == '__main__':

    celltypes = ['Erythrocyte', 'Lymphocyte', 'Mononuclear cell', 'Neutrophil']
    dataroot = './sourcedata/export'
    csvoutput = './sourcedata/step1_datastat.csv'

    # Count cells and save as a .csv file
    count_cells(dataroot, celltypes, csvoutput)

