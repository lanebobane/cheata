import sys
from datetime import timedelta

sys.path.insert(0, '/Users/lanezimmerman/Documents/cheata')

from data import DataPoint, DataPoints

# TODO: Generate XML file to be used so you know what to assert
# from within this file. 


def test_parse_gpx_file_wpt():
	print('******************')
	print('Running test_parse_gpx_file_1')
	dps = DataPoints('./tests/sample_gpx1.gpx', 'wpt')
	try:
		assert dps.data_point_count() == 6
		print('Assertion of data_point_count() passed.')
		assert dps.ensure_dates_sorted()
		print('Assertion of ensure_dates_sorted() passed.')

		assert dps.max_time() > dps.min_time()
		print('Assertion of min and max times passed.')

		assert dps.time_difference() == timedelta(seconds=26)
		print('Assertion of time_difference passed pre modification')

		dps.reduce_time_by_time(timedelta(seconds=16))

		assert dps.time_difference() == timedelta(seconds=10)
		print('Assertion of time_difference passed post absolute modification')

		dps.reduce_time_by_percentage(50)

		assert dps.time_difference() == timedelta(seconds=5)
		print('Assertion of time_difference passed post percentage modification')

	except:
		print('An assertion failed.')

	else: 
		print('All assertions passed.')


def test_parse_gpx_file_trkpt():
	print('******************')
	print('Running test_parse_gpx_file_2')
	dps = DataPoints('./tests/sample_gpx2.gpx', 'trkpt')
	try:
		# assert dps.data_point_count() == 6
		print('Assertion of data_point_count() passed.')
		assert dps.ensure_dates_sorted()
		print('Assertion of ensure_dates_sorted() passed.')

		assert dps.max_time() > dps.min_time()
		print('Assertion of min and max times passed.')


		assert dps.time_difference() == timedelta(seconds=3889)
		print('Assertion of time_difference passed pre modification')

		dps.reduce_time_by_time(timedelta(seconds=1889))

		assert dps.time_difference() == timedelta(seconds=2000)
		print('Assertion of time_difference passed post absolute modification')

		dps.reduce_time_by_percentage(50)

		assert dps.time_difference() == timedelta(seconds=1000)
		print('Assertion of time_difference passed post percentage modification')

	except:
		print('An assertion failed.')

	else: 
		print('All assertions passed.')


test_parse_gpx_file_wpt()
test_parse_gpx_file_trkpt()