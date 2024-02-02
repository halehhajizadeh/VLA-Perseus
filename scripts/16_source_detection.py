import sys
sys.path.append('.')
from configs import path, nit, threedigits, thresh, blim
import numpy as np
import pandas as pd

imagename= threedigits + '-mosaic-fieldALL-Stokes'+str(Stoke)+'-2.5arc-'+str(nit)+'-'+str(thresh)+'-spwALL-pb'+str(pblim)+'-cyclenit500'

catalog_name= path +'/Images/'+ imagename + '.image.pybdsf.srl'

df = pd.read_csv(catalog_name, delim_whitespace=True)