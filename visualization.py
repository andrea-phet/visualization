import cairocffi as cairo
import math
import pickle
import numpy
from sklearn.decomposition import PCA
import imageio
import textwrap

FRAMES_PER_SECOND = 1
WIDTH, HEIGHT = 600, 300
ITERATIONS = 30

# draw wrapped text
def wrapped_text( ctx, text, x, y, width ):
	(text_x, text_y, text_width, text_height, dx, dy) = ctx.text_extents( text  )
	if text_width <= width:
		ctx.move_to( x, y )
		ctx.show_text( text )
	else:
		ctx.move_to( x, y )
		character_width = text_width / len(text)
		number_of_characters = width // character_width
		lines = textwrap.wrap( text, width=number_of_characters )
		for line in lines:
			ctx.show_text( line )
			y += 20 #text_height + 2
			ctx.move_to( x, y )

# plot a guess
def plot( ctx, center_x, center_y, scale, text, point_x, point_y ):
    
	# map x,y range from (-1,-1),(1,1) to (400,200),(600,0)
	mapped_x = point_x * scale + center_x
	mapped_y = point_y * scale + center_y
	
    # gather information about the text to center it
	(x, y, width, height, dx, dy) = ctx.text_extents( text ) 
	ctx.move_to( mapped_x - width/2, mapped_y + height/2 )
	
	ctx.set_source_rgb( 1, 1, 0 )
	ctx.show_text( text )

# create table from two dimensional array
def create_table( ctx, left, top, array ):
	x = left
	y = top
	ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
	ctx.set_source_rgb( 0, 0, 0 )
	for row in array:
		for cell in row:
				ctx.move_to( x, y )
				ctx.show_text( cell )
				x = x + 200
		x = left
		y = y + 20
		ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL )

#pycairo	
def draw(ctx, width, height, i, guesses, desctest_2d ):
	# draw a background rectangle
	ctx.rectangle( 0, 0, width, height )
	ctx.set_source_rgb( 1, 1, 1 )
	ctx.fill()

	# display question text
	ctx.set_font_size(14)
	ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
	ctx.move_to( 10, 20 )
	ctx.set_source_rgb( 0, 0, 0 )
	wrapped_text( ctx, guesses[i][0], 20, 20, 360 )

	create_table( ctx, 10, 250, [ [ "Prediction", "Evidence" ], [ guesses[i][1], "-"] ] )

	# draw background rectangle for the plot
	ctx.rectangle( 400, 0, 200, 200 )
	ctx.set_source_rgb( 0, 0, 0.3 )
	ctx.fill()
	
	point = desctest_2d[i]
	plot( ctx, 500, 100, 20, guesses[i][1], point[ 0 ], point [ 1 ] )

# dimensions
def reduce_to_2d(nd_array):
	pca = PCA(n_components=2)
	pca.fit(nd_array)
	return pca.transform(nd_array)

# loading data
def load_pickle(path):
	with open( path, 'rb' ) as infile:
		loaded_pickle = pickle.load( infile )
	return loaded_pickle

def load_numpy(path):
	with open( path, 'rb' ) as infile:
		loaded_numpy = numpy.load( infile )
	return loaded_numpy

# create visualizations from data and returns paths of the pictures
def visualize( guesses, desctest_2d ):
	file_names = []
	for i in range( 0, ITERATIONS ):
		surface = cairo.ImageSurface( cairo.FORMAT_ARGB32, WIDTH, HEIGHT )
		ctx = cairo.Context(surface)
		draw( ctx, WIDTH, HEIGHT, i, guesses, desctest_2d )
		file_name = "pictures/vis" + str(i) + ".png"
		surface.write_to_png( file_name )
		file_names.append( file_name )
	return file_names

def create_gif( path_to_gif, file_names ):
	images = []
	for file_name in file_names:
		images.append(imageio.imread(file_name))
	imageio.mimsave( path_to_gif, images, fps=FRAMES_PER_SECOND)
	
# executed
def main():
	guesses = load_pickle('files/qantatest.p')
	desctest_2d = reduce_to_2d( load_numpy('files/rnndesctest.npy') )
	file_names = visualize( guesses, desctest_2d )
	create_gif( 'vis.gif', file_names )
	print( 'Visualization complete.')

main()
