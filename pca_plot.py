import cairocffi as cairo
import math
import numpy

WIDTH, HEIGHT = 600, 600

surface = cairo.ImageSurface( cairo.FORMAT_ARGB32, WIDTH, HEIGHT )
ctx = cairo.Context (surface)

#data
with open( 'projected_atest.npy', 'rb' ) as atest_file, open( 'projected_desctest.npy', 'rb') as desctest_file:
	atest_2d = numpy.load( atest_file )
	desctest_2d = numpy.load( desctest_file )

#background
ctx.rectangle( 0, 0, WIDTH, HEIGHT )
ctx.set_source_rgb( 0, 0, 0.3 )
ctx.fill()

ctx.set_source_rgb( 1, 1, 1 )
ctx.move_to( 300 - 70, 300 )
ctx.line_to( 300 + 70, 300 )
ctx.move_to( 300, 300 - 70 )
ctx.line_to( 300, 300 + 70 )
ctx.stroke()

# draw the 2 dimensional points that were projected down from 300 dimensions
ctx.set_source_rgb( 0.8, 0, 0 )
for data in atest_2d:
	ctx.arc( data[0] * 70 + 300, data[1] * 70 + 300, 2, 0, 2*math.pi)
	ctx.fill()
ctx.set_source_rgb( 0, 0.8, 0 )
for data in desctest_2d:
	ctx.arc( data[0] * 70 + 300, data[1] * 70 + 300, 2, 0, 2*math.pi)
	ctx.fill()

# output to PNG
surface.write_to_png( "plot.png" )
