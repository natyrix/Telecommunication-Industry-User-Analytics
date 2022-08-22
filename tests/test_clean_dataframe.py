import unittest
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join("../Telecommunication-Industry-User-Analytics/")))

from scripts import clean_dataframe

df = pd.read_csv("./tests/sample_data.csv")

class TestCleaTelco(unittest.TestCase):
    
    def setUp(self):
        self.clean_telco = clean_dataframe.CleanTelco()
    
    def test_convert_to_datetime(self):
        self.assertEqual(self.clean_telco.convert_to_datetime(df, 'Start')['Start'].dtype, "datetime64[ns]")
    
    def test_convert_to_integer(self):
        self.assertEqual(self.clean_telco.convert_to_integer(df, 'Bearer Id')['Bearer Id'].dtype, "int64")

    def test_convert_to_string(self):
        self.assertEqual(self.clean_telco.convert_to_string(df, 'Last Location Name')['Last Location Name'].dtype, 'string')








if __name__ == "__main__":
    unittest.main()