# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 08:46:04 2024

@author: pickering
"""


import pyopticaltable as pt
import matplotlib.pyplot as plt
msize = 0.4
table = pt.OpticalTable(20,10, size_factor=10, show_edge=True, show_grid=False, show_labels=False)
#table = pt.OpticalTable(20,10, size_factor=10, show_edge=True, show_grid=True, show_labels=True)
probebeam = pt.LaserBeam(colour='red')
wlbeam = pt.LaserBeam(colour='gold')
wlprobe = pt.LaserBeam(colour='gold', style=':')
pumpbeam = pt.LaserBeam(colour='blue')
ramanbeam = pt.LaserBeam(colour='skyblue')
topaspumpbeam = pt.LaserBeam(colour='red')
nopapumpbeam = pt.LaserBeam(colour='red')
probepath, wlpath, wlprobepath, pumppath, ramanpath = [], [], [], [], []
topaspumppath, nopapumppath  = [], []

col = 'green'
spitfire = table.box_source(-8, 4, 4, 2, output_side='right', angle=0, label='Spitfire\nDriving Laser', label_pos='centre')
BS1 = table.mirror(-5,4, msize, -45)
BS2 = table.mirror(-5,2, msize, 45)
M1 = table.mirror(-9,2, msize, 45)
M2 = table.mirror(-9,-4, msize, -45)
topas = table.box_source(-7,-4,2,1.5, 0, label='TOPAS', output_side='right', label_pos='centre')
topaspt = table.point_source(-8,-4)

#probe path
M3 = table.mirror(-3, 2, msize, -45, colour=col)
M4 = table.mirror(-3, 1, msize, 45, colour=col)
M5 = table.mirror(-6, 1, msize, 45, colour=col)
M6 = table.mirror(-6, 0, msize, -45, colour=col)
delay1 = table.box(-6.5, 0.5, 2, 2,0, label='Delay\nStage', label_pos = 'left', labelpad=1.75,standalone=True, linestyle=':')

CM1 = table.concave_mirror(-1, 0, msize, -70, lens_factor=0.4, colour=col)
sapphire = table.box(-3,-0.5,0.25,0.5, 35, standalone=True, colour=col)
CM2 = table.concave_mirror(-5, -1, msize, 110, lens_factor=0.4, colour=col)
M7 = table.mirror(-2, -1, msize, -45, colour=col)
M8 = table.mirror(-2, -2, msize, -45, colour=col)

#pump path
chop1 = table.box(-4, -4, 0.5, 1, 0, label='Chopper', standalone=True, labelpad=1, colour=col, textcolour=col)
M9 = table.mirror(0, -4, msize, 45, colour=col)
M10 = table.mirror(0, -3, msize, 45, colour=col)
L2 = table.convex_lens(1,-2.8,msize,105, colour=col)
dump1 = table.point_source(7, -1.6)

#raman path
NOPA = table.box_source(-1.5, 4, 2.5, 1.5, 0, label='ps-NOPA', output_side='right', label_pos='centre')
nopapt = table.point_source(-2.75, 4)
chop2 = table.box(1, 4, 0.5, 1, 0, label='Chopper', standalone=True, labelpad=0.75, colour=col, textcolour=col)
M11 = table.mirror(6, 4, msize, -45, colour=col)
M12 = table.mirror(6, 3, msize, 45, colour=col)
M13 = table.mirror(1, 3, msize, 45, colour=col)
M14 = table.mirror(1, -1, msize, -60, colour=col)
L3 = table.convex_lens(2, -1.3, msize, 70, colour=col)
delay2 = table.box(6.5, 3.5, 3, 2,0, label='Delay\nStage', label_pos = 'right', labelpad=2.5,standalone=True, linestyle=':')
dump2 = table.point_source(7, -2.4)


sample = table.box(6, -2, 0.25, 1, 0, label='Sample', standalone=True, labelpad=1)
detector = table.box(8, -2, 2, 1.5,0,  label='Spectroscopic\n Detector', standalone=True, labelpad=1.5, colour=col, textcolour=col)


probepath.extend([spitfire, BS1, BS2, M3, M4, M5, M6, CM1, CM2, M7, M8])
wlpath.extend([M8, detector])
wlprobepath.extend([sapphire, CM2, M7, M8])
topaspumppath.extend([BS2, M1, M2, topaspt])
pumppath.extend([topas, M9, M10, sample, dump1])
nopapumppath.extend([BS1, nopapt])
ramanpath.extend([NOPA, M11, M12, M13, M14, sample, dump2])

ramanbeam.draw(table, ramanpath)
nopapumpbeam.draw(table, nopapumppath)
topaspumpbeam.draw(table, topaspumppath)
pumpbeam.draw(table, pumppath)
probebeam.draw(table, probepath)
wlprobe.draw(table, wlprobepath)
wlbeam.draw(table, wlpath)
