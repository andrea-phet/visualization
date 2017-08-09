
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
		