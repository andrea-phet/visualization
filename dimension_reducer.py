import numpy
from sklearn.decomposition import PCA

with open( 'files/rnnatest.npy', 'rb' ) as infile:
	atest = numpy.load( infile )

pca = PCA(n_components=2)

pca.fit(atest)

projected_down_atest = pca.transform(atest)

with open( 'projected_atest.npy', 'wb' ) as outfile:
	numpy.save( outfile, projected_down_atest )

with open( 'files/rnndesctest.npy', 'rb' ) as infile:
	desctest = numpy.load( infile )

pca.fit(desctest)

projected_down_desctest = pca.transform(desctest)

with open( 'projected_desctest.npy', 'wb' ) as outfile:
	numpy.save( outfile, projected_down_desctest )
