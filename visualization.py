import cairocffi as cairo
import math
import pickle
import numpy
from sklearn.decomposition import PCA
import imageio
import textwrap
import pandas
from gensim import models
import re

# For paths, the home is qb.

FRAMES_PER_SECOND = 1
WIDTH, HEIGHT = 1050, 600
DATA_ROWS = 40
PLOT_SIDE_LENGTH = 600

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

# strings
def get_number_of_words( sentence, number_of_words ):
	words = sentence.split(' ')
	return ' '.join(words[:number_of_words])

def getWords(text):
	return re.compile('\w+').findall(text)

def unnormalize_wikipedia_title(title):
    """
    Normalize wikipedia title coming from raw dumps. This removes non-ascii characters by converting them to their
    nearest equivalent and replaces spaces with underscores
    :param title: raw wikipedia title
    :return: normalized title
    """
    return title.replace('_', ' ')

# plot a guess
def plot( ctx, center_x, center_y, scale, text, point_x, point_y, y_to_x_scale=1 ):
	
	scale_x = scale
	scale_y = scale * y_to_x_scale

	# map x,y range from (-1,-1),(1,1) to (400,200),(600,0)
	mapped_x = point_x * scale_x + center_x
	mapped_y = point_y * scale_y + center_y
	
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
				x = x + 310
		x = left
		y = y + 20
		ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL )

#pycairo	
def draw_visualization(ctx, width, height, frame, have_vectors_data=False ):
	# draw a background rectangle
	ctx.rectangle( 0, 0, width, height )
	ctx.set_source_rgb( 1, 1, 1 )
	ctx.fill()

	# display question text
	ctx.set_font_size(14)
	ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
	ctx.move_to( 10, 20 )
	ctx.set_source_rgb( 0, 0, 0 )
	wrapped_text( ctx, frame[0], 20, 20, 440 )

	# draw background rectangle for the plot
	ctx.rectangle( WIDTH - PLOT_SIDE_LENGTH, 0, PLOT_SIDE_LENGTH, PLOT_SIDE_LENGTH )
	ctx.set_source_rgb( 0, 0, 0.3 )
	ctx.fill()

	table = [ [ "Prediction", "Evidence" ] ]
	for i in range(1, len(frame)):
		table.append([ frame[i][0], str(frame[i][1]) ] )
		if ( have_vectors_data is not False ):
			point = frame[i][2]
			plot( ctx, WIDTH - PLOT_SIDE_LENGTH / 2, PLOT_SIDE_LENGTH / 2, 400, frame[i][0], point[ 0 ], point [ 1 ], y_to_x_scale=1 )

	create_table( ctx, 10, 250, table )

# dimensions
def reduce_to_2d(nd_array):
	pca = PCA(n_components=2)
	try:
		pca.fit(nd_array)
	except:
		print( 'ERROR with pca.fit')
		# print( nd_array )
		return
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

def save_numpy( path, output ):
	with open( path, 'wb' ) as outfile:
		numpy.save( outfile, output )

def load_pandas(path):
	with open( path, 'rb' ) as infile:
		loaded_pandas = pandas.read_pickle(infile)
	return loaded_pandas

# animate pictures
def create_gif( path_to_gif, file_names ):
	images = []
	for file_name in file_names:
		images.append(imageio.imread(file_name))
	imageio.mimsave( path_to_gif, images, fps=FRAMES_PER_SECOND)

# loading data, hopefully just once
def load_guesses():
	print('Loading guesses_expo.')
	return load_pandas('../guesser_guesses/guesses_dev.pickle')

# create visualizations from data and returns paths of the pictures
def visualize( guesses_data=None, cached_wikipedia=None, w2vmodel=None, questions_lookup=None, rows=DATA_ROWS ):
	'''
	cached_wikipedia=CachedWikipedia(), w2vmodel=models.KeyedVectors.load_word2vec_format(\'../GoogleNews-vectors-negative300.bin\', binary=True)
	'''
	# guesses = load_pickle('files/qantatest.p')
	if ( guesses_data is None ):
		print('Loading guesses_expo.')
		guesses_data = load_guesses()
		print('Done loading guesses_dev.')
	values = guesses_data.values
	if ( questions_lookup is None ):
		print('Loading old questions database.')
		questions_lookup = load_pickle('../visualization/questions_lookup.pkl')
		print('Done loading questions.')
	file_names = []
	frames = []
	last_token = None
	frame = None

	# save data into frames
	for i in range (0, rows, 1):
		value = values[i]
		answer = value[1]
		qnum = value[3]
		score = value[4]
		sentence = value[5]
		token = value[6]
		if token == last_token:
			# print([ answer, score ])
			frame.append( [ answer, round( score, 4 ) ] )
		else:
			# print('frame')
			frames.append( frame )
			question_text = questions_lookup[qnum].text
			question_text_so_far = ''
			for m in range(0,sentence):
				question_text_so_far += question_text[m] + ' '
			question_text_so_far += get_number_of_words( question_text[sentence], token )
			frame = [question_text_so_far]
			last_token = token
	frames.pop(0) # pop the first None frame from the list

	# get word vectors for each frame
	if ( cached_wikipedia is not None ):
		use_wikipedia = True
		not_in_vocab = []
		for frame in frames:

			# find word2vectors for each guess, and fit PCA model on them
			vectors=[]
			for j in range(1, len(frame)):
				answer = unnormalize_wikipedia_title(frame[j][0])

				# fix some titles so wikipedia model can find the page
				if ( answer == 'Orange'):
					answer = 'Orange (color)'
				if ( answer == 'Java (programming language)'):
					answer = 'Java'
				wiki_page = cached_wikipedia[answer]
				wikipedia_words = getWords( wiki_page.content )
				wikipedia_word_vectors = []
				for word in wikipedia_words:
					try:
						wikipedia_word_vector = w2vmodel.wv[word]
					except:
						not_in_vocab.append(word)
					wikipedia_word_vectors.append( wikipedia_word_vector )
				vector = numpy.array(wikipedia_word_vectors).mean(axis=0)
				if ( not numpy.isnan(vector).any()): # only add word_vector if it exists
					vectors.append(vector)
				else:
					print('nan vector ' + answer)

			# shift vectors to center around top guess
			top_guess = numpy.copy( vectors[0] )

			# add a strut to force the mean to be the top guess
			strut = []
			for x in range( 0, len(top_guess) ):
				sum_column = 0
				for vector in vectors:
					sum_column += vector[x]
				strut.append( top_guess[x] * ( len(vectors) + 1 ) - sum_column )
			# strut = numpy.subtract( numpy.multiply( top_guess, len(vectors ) ), numpy.sum( vectors[1:] ) )
			vectors.append( strut )
			vectors2d = reduce_to_2d(numpy.array(vectors))
			vectors2d = vectors2d[:-1].copy() # remove strut
			# print( vectors2d )

			# add 2d vector to each guess info array
			for k in range(0, len(vectors2d)):
				frame[k+1].append(vectors2d[k])
		# print( 'Not in vocab: ' + str(not_in_vocab) )
	else:
		use_wikipedia = False

	# draw each frame
	for i in range( 0, len(frames) ):
		surface = cairo.ImageSurface( cairo.FORMAT_ARGB32, WIDTH, HEIGHT )
		ctx = cairo.Context(surface)
		draw_visualization( ctx, WIDTH, HEIGHT, frames[i], have_vectors_data=use_wikipedia )
		file_name = "../visualization/pictures/vis" + str(i) + ".png"
		surface.write_to_png( file_name )
		file_names.append( file_name )
	create_gif( '../visualization/vis.gif', file_names )
	print( 'Visualization complete.')

# executed
def main():
	print(visualize())
	# word_vectors()

# main()
