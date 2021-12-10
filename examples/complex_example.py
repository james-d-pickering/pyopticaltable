import matplotlib.pyplot as plt
import pyopticaltable as pyopt

plt.close('all')
mirrorsize = 0.25
table = pyopt.OpticalTable(30, 10, size_factor=10, show_edge=True, show_grid=False)

visbeam = pyopt.LaserBeam(colour='green')
vispath = []

visbeam_dumped = pyopt.LaserBeam(colour='green')
visdump_path = []

irbeam = pyopt.LaserBeam(colour='red')
irpath = []

sfbeam = pyopt.LaserBeam(colour='blue')
sfpath = []

irbeam_overlapped = pyopt.LaserBeam(colour='red', style=(0, (5, 8)))
irbeam_overlappedpath = []

SHBC = table.box_source(-12,-4, 4, 2, 0, colour='k', output_side='right',label='SHBC', textcolour='green',
                 labelpad=0)
vispath.append(SHBC)

visM1 = table.mirror(14,-4,mirrorsize,45)
vispath.append(visM1)
visM2 = table.mirror(14, 4,mirrorsize,-45)
vispath.append(visM2)
visM3 = table.mirror(13, 4,mirrorsize,45)
vispath.append(visM3)
visM4 = table.mirror(13,-1,mirrorsize,45)
vispath.append(visM4)
visM5 = table.mirror(12,-1,mirrorsize,-45)
vispath.append(visM5)
visM6 = table.mirror(12,4,mirrorsize,-45)
vispath.append(visM6)
visM7 = table.mirror(11,4,mirrorsize,45)
vispath.append(visM7)
visL1 = table.concave_lens(11, 1, mirrorsize, 0)
vispath.append(visL1)
visL2 = table.convex_lens(11, 0.5, mirrorsize, 180)
vispath.append(visL2)
visM8 = table.mirror(11,-3,mirrorsize,45)
vispath.append(visM8)
visHWP1 = table.transmissive_plate(10, -3, mirrorsize, 90, label='HWP', label_pos='bottom', labelpad=0.6)
vispath.append(visHWP1)
visCube = table.beamsplitter_cube(9, -3, mirrorsize, 0, 'R')
vispath.append(visCube)
visdump_path.append(visCube)
visHWP2 = table.transmissive_plate(8, -3, mirrorsize, 90, label='HWP', label_pos='bottom', labelpad=0.6)
vispath.append(visHWP2)
visdump = table.beam_dump(9, -2, mirrorsize, 0)
visdump_path.append(visdump)
visperiscope = table.beamsplitter_cube(-6, -3, mirrorsize, 0, 'R', label='Periscope', label_pos='bottom', labelpad=0.6)
vispath.append(visperiscope)
visM9 = table.mirror(-6, 0, mirrorsize, 30)
vispath.append(visM9)

Geplate = table.mirror(-4,-2, mirrorsize*1.5, -20, label='Ge Plate', label_pos='bottom', labelpad=0.4)
vispath.append(Geplate)

CM1 = table.concave_mirror(6, -2, mirrorsize, 250, lens_factor=0.5)

vispath.append(CM1)
CM2 = table.concave_mirror(4.25, -1.4, mirrorsize, 70, lens_factor=0.5)
vispath.append(CM2)


lyra = table.box_source(-13, 0, 3, 2, 0, colour='k', output_side='right', label='Lyra', textcolour='red',
                        labelpad=0)
irpath.append(lyra)
irM1 = table.mirror(-7, 0, mirrorsize, -65)
irpath.append(irM1)
irM2 = table.mirror(-10, -2, mirrorsize, -15)
irpath.append(irM2)
irM3 = table.mirror(-11, 2, mirrorsize, 45)
irpath.append(irM3)
irHWP = table.transmissive_plate(-9, 2, mirrorsize, 90, label='HWP', label_pos='top', labelpad=0.6)
irpath.append(irHWP)
irpol = table.transmissive_plate(-7, 2, mirrorsize, 90, label='Polariser', label_pos='top', labelpad=0.6)
irpath.append(irpol)
irM4 = table.mirror(-5, 2, mirrorsize, -45)
irpath.append(irM4)
irM5 = table.mirror(-5, -2, mirrorsize, -45)
irpath.append(irM5)
irpath.append(Geplate)
irbeam_overlappedpath.append(Geplate)
irbeam_overlappedpath.append(CM1)
irbeam_overlappedpath.append(CM2)

aerosols = table.generic_circle(5, -1.65, 0.2)
sfpath.append(aerosols)
sflens1 = table.concave_lens(5.28, -1.19, mirrorsize, 329.0, label='Collection Lens', label_pos='right', 
                             labelpad=1.7,fontsize=7)

sfFilter1 = table.transmissive_plate(5.66, -0.56, mirrorsize, 328, label='515nm Filter', label_pos='right', 
                                   labelpad=1.7, fontsize=7)


sfM1 = table.mirror(6, 0, mirrorsize, -60)
sfpath.append(sfM1)
sfM2 = table.mirror(3, 0, mirrorsize, -45)
sfpath.append(sfM2)

sfHWP = table.transmissive_plate(3, 1, mirrorsize, 0, label='HWP', label_pos='left', labelpad=1)

sfM3 = table.mirror(3, 2, mirrorsize, 45)

sfCube = table.beamsplitter_cube(4, 2, mirrorsize, 0, 'L', label='Polariser', label_pos='top', labelpad=0.6)
sfFilter2 = table.transmissive_plate(5, 2, mirrorsize, 90, label='515nm\n Filter', label_pos='bottom', labelpad=0.75)
sflens2 = table.concave_lens(6, 2, mirrorsize, 90, label='Lens', label_pos='top', labelpad=0.6)
sfpath.append(sfM3)

spectrograph = table.box_source(8, 2, 3, 2, 0, output_side='left', label='Detection', labelpad=0, textcolour='k')
camera = table.box(8.75, 4, 1, 2, 0, standalone=True)
sfpath.append(spectrograph)


visbeam.draw(table, vispath)
visbeam_dumped.draw(table, visdump_path)
irbeam.draw(table, irpath)
irbeam_overlapped.draw(table, irbeam_overlappedpath)
sfbeam.draw(table, sfpath)


