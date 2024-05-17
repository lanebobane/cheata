import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta

# https://docs.python.org/3/library/xml.etree.elementtree.html

class DataPoint():

	def __init__(self, lat, lon, elevation, date, extensions):
		# {
		#     "date": "06/17/2016, 23:41:03",
		#     "ele": "3.4",
		#     "extensions": "",
		#     "lat": "37.778259000",
		#     "lon": "-122.391386000"
		# }
		self.lat = lat
		self.lon = lon
		self.elevation = elevation
		self.date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
		self.normalized_date = None
		self.extensions = extensions if \
			extensions != "\n      " else ''

	def __repr__(self):
		return json.dumps(
			{
				"lat": self.lat,
				"lon": self.lon,
				"ele": self.elevation,
				"date": self.date.strftime("%m/%d/%Y, %H:%M:%S"),
				"normalized_date": self.normalized_date,
				"extensions": self.extensions
			}
		, sort_keys=True, indent=4)


class DataPoints():

	def __init__(self, file_name, node_type):
		self.data_points = self._parse_gpx_file(file_name, node_type)
		self.normalize_dates()

	def _parse_gpx_file(self, file_name, node_type):
		# <wpt> vs <trkpt>
		tree = ET.parse(file_name)
		root = tree.getroot()
		data_points = []

		if node_type == 'wpt':
			for wpt in root:
				data_dict = {
					"lat": wpt.attrib['lat'],
					"lon": wpt.attrib['lon'],
					"ele": None, 
					"time": None, 
					"extensions": None
				}
				for child in wpt:
					key = child.tag.split('}')[1]
					data_dict[key] = child.text
				dp = DataPoint(
					data_dict['lat'],
					data_dict['lon'],
					data_dict['ele'],
					data_dict['time'],
					data_dict['extensions'],
					)
				data_points.append(dp)


		elif node_type == 'trkpt':
			for trkpt in root[1][2]:
				data_dict = {
					"lat": trkpt.attrib['lat'],
					"lon": trkpt.attrib['lon'],
					"ele": None, 
					"time": None, 
					"extensions": None
				}
				for child in trkpt:
					key = child.tag.split('}')[1]
					data_dict[key] = child.text
				dp = DataPoint(
					data_dict['lat'],
					data_dict['lon'],
					data_dict['ele'],
					data_dict['time'],
					data_dict['extensions'],
					)
				data_points.append(dp)

		else: 
			print('Invalid node type. Please choose either "wpt" or trkpt" ')

		return data_points

	def data_point_count(self):
		return len(self.data_points)

	def min_time(self):
		return self.data_points[0].date

	def max_time(self):
		return self.data_points[self.data_point_count()-1].date

	def time_difference(self): 
		return self.max_time() - self.min_time()

	def ensure_dates_sorted(self):
		previous = self.data_points[0]
		for data_point in self.data_points[1:]:
			if data_point.date < previous.date:
				return False
			else: 
				previous = data_point
		return True

	def normalize_dates(self):
		for dp in self.data_points:
			dp_diff = dp.date - self.min_time()
			factor = dp_diff/self.time_difference()
			dp.normalized_date = factor

	def reduce_time_by_percentage(self, amount):
		if amount >= 100:
			raise Exception('You cannot reduce the file by 100% or more.')

		# ignore fractional seconds in current time_difference().
		self.reduce_time_by_time((amount/100)*self.time_difference())


	def reduce_time_by_time(self, delta):
		if self.time_difference() < delta:
			raise Exception('You cannot reduce the file by more time than its total elapsed time.')

		for dp in self.data_points:
			dp.date = dp.date - (dp.normalized_date * delta)



