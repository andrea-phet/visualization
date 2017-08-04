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
WIDTH, HEIGHT = 900, 500
ITERATIONS = 2

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
    print('Un-normalizing wikipedia title.')
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
				x = x + 200
		x = left
		y = y + 20
		ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL )

#pycairo	
def draw_visualization(ctx, width, height, i, frame, have_vectors_data=False ):
	# draw a background rectangle
	ctx.rectangle( 0, 0, width, height )
	ctx.set_source_rgb( 1, 1, 1 )
	ctx.fill()

	# display question text
	ctx.set_font_size(14)
	ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
	ctx.move_to( 10, 20 )
	ctx.set_source_rgb( 0, 0, 0 )
	print(frame)
	wrapped_text( ctx, frame[0], 20, 20, 440 )

	# draw background rectangle for the plot
	ctx.rectangle( 500, 0, 400, 400 )
	ctx.set_source_rgb( 0, 0, 0.3 )
	ctx.fill()

	table = [ [ "Prediction", "Evidence" ] ]
	for i in range(1, len(frame)):
		table.append([ frame[i][0], str(frame[i][1]) ] )
		if ( have_vectors_data is not False ):
			point = frame[i][2]
			plot( ctx, 700, 200, 40, frame[i][0], point[ 0 ], point [ 1 ] )

	create_table( ctx, 10, 250, table )

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
	print('Done loading guesses_dev.')

# create visualizations from data and returns paths of the pictures
def visualize( guesses_data=None, cached_wikipedia=None, w2vmodel=None ):
	'''
	cached_wikipedia=CachedWikipedia(), w2vmodel=models.KeyedVectors.load_word2vec_format(\'../GoogleNews-vectors-negative300.bin\', binary=True)
	'''
	# guesses = load_pickle('files/qantatest.p')
	if ( guesses_data is None ):
		print('Loading guesses_expo.')
		guesses_data = load_guesses()
		print('Done loading guesses_dev.')
	# return guesses_data
	# return guesses_data.groupby( 'qnum' )
	# values = guesses_data.groupby( 'qnum' ).sum().groupby(['sentence','token']).sum().values
	values = guesses_data.values
	# groupped_guesses_data = guesses_data.groupby('qnum').mean().groupby( ['sentence', 'token' ] ).mean()
	# print(groupped_guesses_data)
	# return
	questions_lookup = load_pickle('../visualization/questions_lookup.pkl')
	# desctest_2d = reduce_to_2d( load_numpy('files/rnndesctest.npy') )
	file_names = []
	frames = []
	last_token = None
	frame = None
	for i in range (0, 30):
		value = values[i]
		answer = value[1]
		qnum = value[3]
		score = value[4]
		sentence = value[5]
		token = value[6]
		if token == last_token:
			frame.append( [ answer, score ] )
		else:
			frames.append( frame )
			question_text = questions_lookup[qnum]
			question_text_so_far = get_number_of_words( question_text[sentence], token )
			frame = [question_text_so_far]
			last_token = token
	frames.pop(0) # pop the first None frame from the list
	if ( cached_wikipedia is not None ):
		use_wikipedia = True
		not_in_vocab = []
		for frame in frames:

			# find word2vectors for each guess, and fit PCA model on them
			vectors=[]
			# print(frame)
			for i in range(1, len(frame)):
				# print(frame[i][0])
				answer = unnormalize_wikipedia_title(frame[i][0])
				wiki_page = cached_wikipedia[answer]
				wikipedia_words = getWords( wiki_page.content )
				wikipedia_word_vectors = []
				for word in wikipedia_words:
					# print(word)
					try:
						wikipedia_word_vector = w2vmodel.wv[word]
					except:
						not_in_vocab.append(word)
					# print(wikipedia_word_vector)
					wikipedia_word_vectors.append( wikipedia_word_vector )
				# print(wikipedia_word_vectors)
				vector = numpy.array(wikipedia_word_vectors).mean(axis=0)
				# print(i)
				vectors.append(vector)
			# TODO, get question average vector and origin around that
			# print(type(vectors), len(vectors), vectors[0])
			vectors2d = reduce_to_2d(numpy.array(vectors))
			print(vectors2d) #[[ 0.]]

			# add 2d vector to each guess info array
			for i in range(0, len(vectors2d)):
				frame[i+1].append(vectors2d[i])
		# print( 'Not in vocab: ' + str(not_in_vocab) )
	else:
		use_wikipedia = False
	for i in range( 0, ITERATIONS ):
		surface = cairo.ImageSurface( cairo.FORMAT_ARGB32, WIDTH, HEIGHT )
		ctx = cairo.Context(surface)
		draw_visualization( ctx, WIDTH, HEIGHT, i, frames[i], have_vectors_data=use_wikipedia )
		file_name = "../visualization/pictures/vis" + str(i) + ".png"
		surface.write_to_png( file_name )
		file_names.append( file_name )
	create_gif( '../visualization/vis.gif', file_names )
	print( 'Visualization complete.')

# get training data
def create_sentences(path_to_file):
	sentences = []
	with open( path_to_file ) as infile:
		for line in infile.readlines():
			line = line.strip( '\n' )
			line = line.strip(',.!?"-')
			words = line.split()
			sentences.append( words )
	return sentences


# experiment with word2vec
def word_vectors():
	'''
	computer
	programmer
	Shadowhunters
	Jace Wayland
	Clary Fray
	nerd
	Pho
	Jianghu
	'''

	# sentences = [
	# 	['computer', 'programmer'],
	# 	['Jace','Wayland','and','Clary','Fray','are','Shadowhunters'],
	# 	['I','am','a','nerd','and','I','like','Pho'],
	# 	['Jianghu','is','the','wuxia','world','of','citizens','heroes','and','evildoers']
	# ]
	# text_file = 'City of Bones.txt'
	# sentences = create_sentences(text_file)
	# print('Processed text file ' + text_file + ' into sentences and words')
	# model = models.Word2Vec( sentences, min_count=1 )
	# disk_file_name = 'wordsbyandrea.txt'
	# model.save(disk_file_name)
	# model = models.Word2Vec.load(disk_file_name)
	# print( 'Trained and loaded word2vec model into ' + disk_file_name )
	# print( 'Start loading google model' )
	# model = models.KeyedVectors.load_word2vec_format('../GoogleNews-vectors-negative300.bin', binary=True)  
	# print( 'Loaded google model' )
	words = [
		# 'Shadowhunter',
		# 'Shadowhunters',
		# 'warlock',
		# 'warlocks',
		# 'vampire',
		# 'vampires',
		# 'werewolf',
		# 'werewolves',
		# 'faerie',
		# 'faeries',
		# 'Jace',
		# 'Clary',
		# 'Isabelle',
		# 'Simon',
		# 'Alec',
		# 'Magnus',
		# 'Valentine',
		# 'Jocelyn',
		# 'Luke',
		'angel',
		'demon',
		'stele',
		'rune',
		'hair',
		'hands'
	]
	# vectors = []
	# for word in words:
	# 	word_vector = model.wv[word]
	# 	vectors.append( word_vector )
	# word_vectors = numpy.array( vectors )
	vectors_file_name = 'angle_demon_vectors.npy'
	# print( 'saving array into file ' + vectors_file_name )
	# save_numpy( vectors_file_name, word_vectors )
	# print( 'saved' )
	word_vectors = load_numpy( vectors_file_name )
	word_2d_vectors = reduce_to_2d( word_vectors )

	surface = cairo.ImageSurface( cairo.FORMAT_ARGB32, WIDTH, HEIGHT )
	ctx = cairo.Context(surface)

	# draw a background rectangle
	ctx.rectangle( 0, 0, WIDTH, HEIGHT )
	ctx.set_source_rgb( 1, 1, 1 )
	ctx.fill()

	# draw background rectangle for the plot
	ctx.rectangle( 400, 0, 500, 500 )
	ctx.set_source_rgb( 0, 0, 0.3 )
	ctx.fill()

	table = [ [ "Word", "2D Vector" ] ]
	
	for i in range( 0, len(words) ):
		point = word_2d_vectors[i]
		plot( ctx, 650, 250, 40, words[i], point[ 0 ], point [ 1 ], y_to_x_scale=1 )
		table.append( [ words[i], str(point[0])+', '+str(point[1]) ] )
	
	create_table( ctx, 10, 20, table )

	file_name = "word2vec.png"
	surface.write_to_png( file_name )
		
# executed
def main():
	print(visualize())
	# word_vectors()

# main()
