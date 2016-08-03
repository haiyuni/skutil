from __future__ import print_function, division
import h2o
import warnings
import numpy as np
from h2o.frame import H2OFrame
from skutil.h2o.select import *
from sklearn.datasets import load_iris
import pandas as pd


iris = load_iris()
F = pd.DataFrame.from_records(data=iris.data, columns=iris.feature_names)


# if we can't start an h2o instance, let's just pass all these tests
try:
	h2o.init(ip='localhost', port=54321)
	X = H2OFrame.from_python(F, column_names=F.columns.tolist())
except Exception as e:
	warnings.warn('could not successfully start H2O instance', UserWarning)
	X = None


def catch_warning_assert_thrown(fun, kwargs):
	with warnings.catch_warnings(record=True) as w:
		warnings.simplefilter("always")

		ret = fun(**kwargs)
		assert len(w) > 0 if not X else True, 'expected warning to be thrown'
		return ret



def test_h2o_multicollinearity():
	# one way or another, we can initialize it
	filterer = catch_warning_assert_thrown(H2OMulticollinearityFilterer, {'threshold':0.6})
	assert filterer.min_version == '3.8.3'
	assert not filterer.max_version

	if X:
		x = filterer.fit_transform(X)
	else:
		pass


def test_h2o_nzv():
	filterer = catch_warning_assert_thrown(H2ONearZeroVarianceFilterer, {'threshold':1e-8})
	assert filterer.min_version == '3.8.3'
	assert not filterer.max_version

	# let's add a zero var feature to F
	f = F.copy()
	f['zerovar'] = np.zeros(F.shape[0])

	try:
		Y = H2OFrame.from_python(f, column_names=f.columns)
	except Exception as e:
		Y = None

	if Y:
		y = filterer.fit_transform(y)
		assert len(y.drop) == 1
	else:
		pass

