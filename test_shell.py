from data import DataPoints, TRKPT, WPT, XMLBuilder
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta

dps2 = DataPoints('./tests/sample_gpx2.gpx', 'trkpt')
dps1 = DataPoints('./tests/sample_gpx1.gpx', 'wpt')

xml2 = XMLBuilder(dps2)
xml1 = XMLBuilder(dps1)