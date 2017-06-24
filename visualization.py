import cairocffi as cairo
import math
import pickle

WIDTH, HEIGHT = 600, 300

surface = cairo.ImageSurface( cairo.FORMAT_ARGB32, WIDTH, HEIGHT )
ctx = cairo.Context (surface)

# my methods - idea: make an object that contains ctx as field and has these:

def strip_last_word( string ):
	words = string.split( ' ' )
	words.pop()
	return ' '.join( words )

def make_less( raw_text, currently_text, done, width ):
	if not raw_text:
		return done
	else:
		(text_x, text_y, text_width, text_height, dx, dy) = ctx.text_extents( currently_text  )
		if text_width <= width:
			remaining_text = raw_text.replace( currently_text, '' )
			remaining_text = remaining_text.lstrip()
			done.append( currently_text )
			return make_less( remaining_text, remaining_text, done, width )
		else:
			return make_less( raw_text, strip_last_word( currently_text ), done, width )

def wrapped_text( text, x, y, width ):
	(text_x, text_y, text_width, text_height, dx, dy) = ctx.text_extents( text  )
	if text_width <= width:
		ctx.move_to( x, y )
		ctx.show_text( text )
	else:
		ctx.move_to( x, y )
		lines = make_less( text, text, [], width )
		for line in lines:
			ctx.show_text( line )
			y += text_height + 2
			ctx.move_to( x, y )

#data
with open( 'files/qantatest.p', 'rb' ) as infile:
	guesses = pickle.load( infile )

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
wrapped_text( guesses[0][0], 10, 20, 400 )

### 2D plot of possible answers ###

# draw background rectangle for the plot
ctx.rectangle( 400, 0, 200, 200 )
ctx.set_source_rgb( 0, 0, 0.3 )
ctx.fill()

# draw the text
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

### table of guesses and evidence ###
ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_source_rgb( 0, 0, 0 )
ctx.move_to( 10, 200 )
ctx.show_text( "Prediction")
ctx.move_to( 210, 200 )
ctx.show_text( "Evidence")

ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL )
ctx.move_to( 10, 220 )
ctx.show_text( guesses[0][1] )


# output to PNG
surface.write_to_png( "vis.png" )
