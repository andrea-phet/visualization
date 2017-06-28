import cairocffi as cairo
import math
import pickle

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
			y += 20 #text_height + 2
			ctx.move_to( x, y )

#data
with open( 'files/qantatest.p', 'rb' ) as infile:
	guesses = pickle.load( infile )

WIDTH, HEIGHT = 600, 300
for i in range( 0, 30 ):

	surface = cairo.ImageSurface( cairo.FORMAT_ARGB32, WIDTH, HEIGHT )
	ctx = cairo.Context (surface)

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
	wrapped_text( guesses[i][0], 10, 20, 380 )

	### 2D plot of possible answers ###

	# draw background rectangle for the plot
	ctx.rectangle( 400, 0, 200, 200 )
	ctx.set_source_rgb( 0, 0, 0.3 )
	ctx.fill()

	### table of guesses and evidence ###
	ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
	ctx.set_source_rgb( 0, 0, 0 )
	ctx.move_to( 10, 250 )
	ctx.show_text( "Prediction")
	ctx.move_to( 210, 250 )
	ctx.show_text( "Evidence")

	ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL )
	ctx.move_to( 10, 270 )

	ctx.show_text( guesses[i][1] )

	# output to PNG
	surface.write_to_png( "pictures/vis" + str(i) + ".png" )
