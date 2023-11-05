import unittest
from utils.timeFormatHandler import *


class TestTimeFormatHandler(unittest.TestCase) :


    def test_localizeAndISOtime(self):

        date = "2023-10-30" # This is the format that you need to input into localizeANDISOtime.

        expected = 1698638400

        actual  = localizeAndISOtime(date)

        self.assertEqual(actual,expected)

    
    def test_localizeAndISOtimeHMS(self):

        date = "2023-10-30T00:00:00-04:00" # This is the format that you need to input into localizeAndISOtimeHMS.

        expected = 1698638400

        actual = localizeAndISOtimeHMS(date)
        
        self.assertEqual(actual,expected)

   
    def test_localizeAndISOtimeHM(self):

        date = "2023-10-30T00:00" # This is the format that you need to input into localizeAndISOtimeHM.

        expected = 1698638400

        actual = localizeAndISOtimeHM(date)
        
        self.assertEqual(actual,expected)

    
    def test_localizeTimeFromOANDA(self):

        date = "2023-10-30T00:00:00.000000000Z" # This is the format that you need to input into localizeTimeFromOANDA.

        expected = 1698638400

        actual = localizeTimeFromOANDA(date)

        self.assertEqual(actual,expected)
        




if __name__ == "__main__":
    unittest.main()


