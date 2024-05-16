import sys

sys.path.insert(0, '/Users/lanezimmerman/Documents/cheata')

from data import DataPoint, DataPoints

# TODO: Generate XML file to be used so you know what to assert
# from within this file. 


def test_parse_gpx_file_1():
	dps = DataPoints('./tests/sample_gpx1.gpx')
	try:
		assert dps.data_point_count() == 6
		print('Assertion of data_point_count() passed.')
		assert dps.ensure_dates_sorted()
		print('Assertion of ensure_dates_sorted() passed.')

		assert dps.max_time() > dps.min_time()
		print('Assertion of min and max times passed.')

	except:
		print('Assertion of data_point_count() failed.')

	print(dps.data_points)

def test_parse_gpx_file_2():
	dps = DataPoints('./tests/sample_gpx2.gpx')
	try:
		# assert dps.data_point_count() == 6
		print('Assertion of data_point_count() passed.')
		assert dps.ensure_dates_sorted()
		print('Assertion of ensure_dates_sorted() passed.')

		assert dps.max_time() > dps.min_time()
		print('Assertion of min and max times passed.')

	except:
		print('Assertions of data_point_count() failed.')

	print(dps.data_points)

test_parse_gpx_file_1()
test_parse_gpx_file_2()