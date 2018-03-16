import pytest
from nordb.nordic.nordicMain import NordicMain
from datetime import datetime
class TestCreateNordicMain(object):
    def testCreateEmptyNordicMain(self):
        nordic_header_main = NordicMain()        
        assert type(nordic_header_main) == NordicMain

    def testFillWithCorrectValues(self):
        nordic_header_main = NordicMain()

        nordic_header_main.origin_time = datetime.strptime("20120101 010101.123400", "%Y%m%d %H%M%S.%f")
        nordic_header_main.location_model = "A"
        nordic_header_main.distance_indicator = "L"
        nordic_header_main.event_desc_id = "Q"
        nordic_header_main.epicenter_latitude = 60.0
        nordic_header_main.epicenter_longitude = 29.0
        nordic_header_main.depth = 10.0
        nordic_header_main.depth_control = "F"
        nordic_header_main.locating_indicator = "S"
        nordic_header_main.epicenter_reporting_agency = "HEL"
        nordic_header_main.stations_used = 20
        nordic_header_main.rms_time_residuals = 10.0
        nordic_header_main.magnitude_1 = 2.1
        nordic_header_main.type_of_magnitude_1 = "M"
        nordic_header_main.magnitude_reporting_agency_1 = "HEL"
        nordic_header_main.magnitude_2 = 2.1
        nordic_header_main.type_of_magnitude_2 = "M"
        nordic_header_main.magnitude_reporting_agency_2 = "HEL"
        nordic_header_main.magnitude_3 = 2.1
        nordic_header_main.type_of_magnitude_3 = "M"
        nordic_header_main.magnitude_reporting_agency_3 = "HEL"
       
