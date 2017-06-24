import cairocffi as cairo

WIDTH, HEIGHT = 600, 300

surface = cairo.ImageSurface( cairo.FORMAT_ARGB32, WIDTH, HEIGHT )
ctx = cairo.Context (surface)

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

### 2D plot of possible answers ###

# draw background rectangle for the plot
ctx.rectangle( 400, 0, 200, 200 )
ctx.set_source_rgb( 0, 0, 0.3 )
ctx.fill()

# draw the text
ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(14)
ctx.set_source_rgb( 1, 1, 0 )
for point in points_2d:

	# map x,y range from (-1,-1),(1,1) to (400,200),(600,0)
	center_x = point[ 1 ] * 100 + 500
	center_y = point[ 2 ] * 100 + 100
	
    # gather information about the text to center it
	(x, y, width, height, dx, dy) = ctx.text_extents( point[ 0 ]  ) 
	ctx.move_to( center_x - width/2, center_y + height/2 )

	ctx.show_text( point[ 0 ] )

	# # help see center
	# ctx.arc( center_x, center_y, 3, 0, 2 * math.pi )
	# ctx.fill()

# output to PNG
surface.write_to_png( "sample_plot.png" )
