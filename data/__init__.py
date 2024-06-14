import xml.etree.ElementTree as ET
import json
import random
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
		self.date = datetime.strptime(date, OUTPUT_TIME_FORMAT)
		self.normalized_date = None
		self.extensions = extensions if \
			extensions != "\n      " else ''

	def __repr__(self):
		return json.dumps(
			{
				"lat": self.lat,
				"lon": self.lon,
				"ele": self.elevation,
				"date": self.date.strftime(PARSE_TIME_FORMAT),
				"normalized_date": self.normalized_date,
				"extensions": self.extensions
			}
		, sort_keys=True, indent=4)


WPT = 'wpt'
TRKPT = 'trkpt'
TRK = 'trk'
NAME = 'name'
TYPE = 'type'
TRKSEG = 'trkseg'
ELE = 'ele'
TIME = 'time'
PARSE_TIME_FORMAT = "%m/%d/%Y, %H:%M:%S"
OUTPUT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
METADATA = 'metadata'
JITTER = .000001

class DataPoints():

	def __init__(self, file_name, node_type):
		self.data_points = self._parse_gpx_file(file_name, node_type)
		self.file_name = file_name
		self.node_type = node_type
		self.normalize_dates()

	def _parse_gpx_file(self, file_name, node_type):
		# <wpt> vs <trkpt>
		tree = ET.parse(file_name)
		root = tree.getroot()
		data_points = []

		if node_type == 'wpt':
			for wpt in root:
				data_dict = {
					"lat": float(wpt.attrib['lat']) + random.randrange(-5,5,1)*JITTER,
					"lon": float(wpt.attrib['lon']) + random.randrange(-5,5,1)*JITTER,
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

		self.reduce_time_by_time((amount/100)*self.time_difference())


	def reduce_time_by_time(self, delta):
		if self.time_difference() < delta:
			raise Exception('You cannot reduce the file by more time than its total elapsed time.')

		for dp in self.data_points:
			dp.date = dp.date - (dp.normalized_date * delta)


WPT_GPX_ATTRIBS = {
		"version":"1.1",
	  	"creator":"Runkeeper - http://www.runkeeper.com",
	  	"xmlns":"http://www.topografix.com/GPX/1/1",
	  	"xmlns:gpxtpx":"http://www.garmin.com/xmlschemas/TrackPointExtension/v1",
	  	"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
	  	"xsi:schemaLocation":"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd",
	}

TPKPT_GPX_ATTRIBS = {
	"version":"1.1",
    "creator":"StravaGPX",
    "xmlns":"http://www.topografix.com/GPX/1/1",
    "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
    "xsi:schemaLocation":"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd",
}

class XMLBuilder():

	def __init__(self, data_points: DataPoints):
		self.data_points = data_points
		self.xml_element = self._build_xml_element()

	def __repr__(self):
		return ET.tostring(self.xml_element).decode('utf-8')

	
	"""
	a = ET.Element('a')
	b = ET.SubElement(a, 'b')
	c = ET.SubElement(a, 'c')
	d = ET.SubElement(c, 'd')
	ET.dump(a)
	<a><b /><c><d /></c></a>


	class xml.etree.ElementTree.Element(tag, attrib={}, **extra)¶

	"""
	def _build_xml_element(self):
		# xml_attribs = {'version': '1.0', 'encoding': 'UTF-8'}
		# xml_root = ET.Element('xml', xml_attribs)

		# gpx_element = ET.SubElement(xml_root, 'gpx', self._find_gpx_attribs_by_node_type())
		gpx_element = ET.Element('gpx', self._find_gpx_attribs_by_node_type())

		if self.data_points.node_type == WPT:
			# todo: maybe rename the first data_points? 
			for dp in self.data_points.data_points:
				attribs = {"lat": dp.lat, "lon": dp.lon}
				wpt_element = ET.SubElement(gpx_element, WPT, attribs)
				ele = ET.SubElement(wpt_element, ELE)
				ele.text = str(dp.elevation)
				time = ET.SubElement(wpt_element, TIME)
				time.text = dp.date.strftime(OUTPUT_TIME_FORMAT)

		if self.data_points.node_type == TRKPT:
			
			# 2. Add Trk element with name, type and trkseg elements
			# 3. Add trkpt elements to the trkseg element
			metadata_element = ET.SubElement(gpx_element, METADATA)
			meta_time_element = ET.SubElement(metadata_element, TIME)
			meta_time_element.text = self.data_points.data_points[0].date.strftime(OUTPUT_TIME_FORMAT)

			trk_element = ET.SubElement(gpx_element, TRK)
			#TODO: Get these values from the initial file.
			name_element = ET.SubElement(trk_element, NAME)
			name_element.text = "PLACEHOLDER NAME"
			type_element = ET.SubElement(trk_element, TYPE)
			type_element.text = "PLACEHOLDER TYPE"

			trkseg_element = ET.SubElement(trk_element, TRKSEG)

			for dp in self.data_points.data_points:
				attribs = {"lat": dp.lat, "lon": dp.lon}
				trkpt_element = ET.SubElement(trkseg_element, TRKPT, attribs)

				ele_element = ET.SubElement(trkpt_element, ELE)
				ele_element.text = dp.elevation

				time_element = ET.SubElement(trkpt_element, TIME)
				time_element.text = dp.date.strftime(OUTPUT_TIME_FORMAT)

		# return xml_root
		return gpx_element


	def _find_gpx_attribs_by_node_type(self):
		if self.data_points.node_type == WPT:
			return WPT_GPX_ATTRIBS
		elif self.data_points.node_type == TRKPT:
			return TPKPT_GPX_ATTRIBS

	def write_file(self):
		tree = ET.ElementTree(self.xml_element)
		file_name = f'output_files/GPX_{datetime.now().strftime(OUTPUT_TIME_FORMAT)}.gpx' 
		tree.write(file_name, encoding='utf-8', xml_declaration=True)
		return file_name