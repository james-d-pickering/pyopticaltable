import pyopticaltable as pyopt

table = pyopt.OpticalTable(20, 10, size_factor=10, show_edge=True, show_grid=True)

beam = pyopt.LaserBeam(colour='green')
beampath = []

laser = table.box_source(-5, 0, 4, 2, 0, colour='k', output_side='right',label='Laser', textcolour='green',
                 labelpad=0)

beampath.append(laser)

mirrorsize = 0.5
mirror1 = table.mirror(0,0,mirrorsize,45)
beampath.append(mirror1)

mirror2 = table.mirror(0,3,mirrorsize,45)
beampath.append(mirror2)

mirror3 = table.mirror(5,3,mirrorsize,-45)
beampath.append(mirror3)

mirror4 = table.mirror(5,0,mirrorsize,-45)
beampath.append(mirror4)

L1 = table.convex_lens(6, 0, mirrorsize, 90)
beampath.append(L1)

L2 = table.concave_lens(7, 0, mirrorsize, 270)
beampath.append(L2)

dump = table.beam_dump(8, 0, 0.1, 0, fillcolour='k')
beampath.append(dump)

beam.draw(table, beampath)
