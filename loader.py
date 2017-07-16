import pickle
import numpy
import pandas

# loading data
def load_pickle(path):
	with open( path, 'rb' ) as infile:
		loaded_pickle = pickle.load( infile )
	return loaded_pickle

def load_numpy(path):
	with open( path, 'rb' ) as infile:
		loaded_numpy = numpy.load( infile )
	return loaded_numpy

def load_pandas(path):
	with open( path, 'rb' ) as infile:
		loaded_pandas = pandas.read_pickle(infile)
	return loaded_pandas