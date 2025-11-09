import os.path
from xml.dom import minidom

#### ONLY ONE OBJECT PER IMAGE IS ASSUMED ####

out_dir = './data/labels/train'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

file = minidom.parse('annotations.xml')
images = file.getElementsByTagName('image')

for image in images:
    width = int(float(image.getAttribute('width')))
    height = int(float(image.getAttribute('height')))
    name = image.getAttribute('name')

    elem = image.getElementsByTagName('points')
    bbox = image.getElementsByTagName('box')[0]
    xtl = float(bbox.getAttribute('xtl'))
    ytl = float(bbox.getAttribute('ytl'))
    xbr = float(bbox.getAttribute('xbr'))
    ybr = float(bbox.getAttribute('ybr'))

    w = xbr - xtl
    h = ybr - ytl

    with open(os.path.join(out_dir, name[:-4] + 'txt'), 'w') as label_file:
        for e in elem:
            # class cx cy w h
            cx = (xtl + w / 2.0) / width
            cy = (ytl + h / 2.0) / height
            bw = w / width
            bh = h / height
            parts = ['0', f'{cx}', f'{cy}', f'{bw}', f'{bh}']

            # parse points "x1,y1;x2,y2;..."
            pts_attr = e.getAttribute('points')
            pts_raw = pts_attr.split(';') if pts_attr else []
            points_ = []
            for p in pts_raw:
                p1, p2 = p.split(',')
                points_.append([float(p1), float(p2)])

            # bierzemy dokładnie 4 punkty (TL,TR,BR,BL)
            points_ = points_[:4]

            # dodajemy (x,y,v=2) dla każdego punktu
            for p in points_:
                x_n = p[0] / width
                y_n = p[1] / height
                parts += [f'{x_n}', f'{y_n}', '2']

            # zapis jednej linii (powinno być 17 wartości)
            label_file.write(' '.join(parts) + '\n')
