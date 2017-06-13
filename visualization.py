import cairo
import math

WIDTH, HEIGHT = 600, 300

surface = cairo.ImageSurface( cairo.FORMAT_ARGB32, WIDTH, HEIGHT )
ctx = cairo.Context (surface)

# input
question_text = "This city's mass transit system's director, Paul Wiedefeld, undertook SafeTrack to restore reliability of the"
guesses = [
   [ "Washington Metro", 34, "stations designed by Harry Weese", "undertook SafeTrack", 0.001, 0.002, 0.300 ],
   [ "Baltimore", 31, "Paul Wiedefeld", "This city's mass transit", 0.002, 0.004, 0.600 ],
   [ "Pokemon", 1, "This city's", "restore reliability", 0.601, 0.602, 0.900 ]
]

#data
points_2d = [
   [ "Washington Metro", 0.001, 0.002 ],
   [ "Baltimore", -0.5, 0.2,],
   [ "Pokemon", 0.601, -0.900 ]
]

# draw a background rectangle
ctx.rectangle( 0, 0, WIDTH, HEIGHT )
ctx.set_source_rgb( 1, 1, 1 )
ctx.fill()

# set font
ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(14)

# display question text
ctx.move_to( 10, 20 )
ctx.set_source_rgb( 0, 0, 0 )
ctx.show_text( question_text )

### 2D plot of possible answers ###

# draw background rectangle for the plot
ctx.rectangle( 400, 20, 200, 200 )
ctx.set_source_rgb( 0, 0, 0.3 )
ctx.fill()

# draw the text
ctx.set_source_rgb( 1, 1, 0 )
for point in points_2d:

	# map x,y range from (-1,-1),(1,1) to (400,220),(600,20)
	center_x = point[ 1 ] * 100 + 500
	center_y = point[ 2 ] * 100 + 120
	
    # gather information about the text to center it
	(x, y, width, height, dx, dy) = ctx.text_extents( point[ 0 ]  ) 
	ctx.move_to( center_x - width/2, center_y + height/2 )

	ctx.show_text( point[ 0 ] )

	# # help see center
	# ctx.arc( center_x, center_y, 3, 0, 2 * math.pi )
	# ctx.fill()

# output to PNG
surface.write_to_png( "vis.png" )
