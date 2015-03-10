import unittest
from instance_monitor import make_stats

class TestMakeStatFunc(unittest.TestCase):
    """
    contains test methods
    """
    def test_noemptyslotforeachinstance(self):
        # no empty slot for each instance, expected zero for each instance in the EMPTY line
        output_lines = []
        fr =   ["80,M1,5,1,1,1,1,0",
                "81,M2,7,1,0,1,1,1,1,1",
                "82,M3,7,1,0,0,0,0,0,1"]
        make_stats(fr, lambda x : output_lines.append(x))

        self.assertEqual(output_lines[0][0].strip(), "EMPTY: M1=0; M2=0; M3=0;")
        self.assertEqual(output_lines[0][1].strip(), "FULL: M1=0; M2=0; M3=0;")
        self.assertEqual(output_lines[0][2].strip(), "MOST FILLED: M1=1,1; M2=1,1; M3=1,5;")

    def test_onlyemptyslotforeachinstance(self):
        # no empty slot for each instance, expected zero for each instance in the EMPTY line
        output_lines = []
        fr =   ["80,M1,5,0,0,0,0,0",
                "81,M2,7,0,0,0,0,0,0,0",
                "82,M3,7,0,0,0,0,0,0,0"]
        make_stats(fr, lambda x : output_lines.append(x))

        self.assertEqual(output_lines[0][0].strip(), "EMPTY: M1=1; M2=1; M3=1;")
        self.assertEqual(output_lines[0][1].strip(), "FULL: M1=0; M2=0; M3=0;")
        self.assertEqual(output_lines[0][2].strip(), "MOST FILLED: M1=1,5; M2=1,7; M3=1,7;")

    def test_onlyfullslotforeachinstance(self):
        # no empty slot for each instance, expected zero for each instance in the EMPTY line
        output_lines = []
        fr =   ["80,M1,5,1,1,1,1,1",
                "81,M2,7,1,1,1,1,1,1,1",
                "82,M3,7,1,1,1,1,1,1,1"]
        make_stats(fr, lambda x : output_lines.append(x))

        self.assertEqual(output_lines[0][0].strip(), "EMPTY: M1=0; M2=0; M3=0;")
        self.assertEqual(output_lines[0][1].strip(), "FULL: M1=1; M2=1; M3=1;")
        self.assertEqual(output_lines[0][2].strip(), "MOST FILLED: M1=0,-1; M2=0,-1; M3=0,-1;")

    def test_instanceM2notpresent(self):
        output_lines = []
        fr =   ["80,M1,5,1,1,1,1,1",
                "82,M3,7,1,1,1,1,1,1,1"]
        make_stats(fr, lambda x : output_lines.append(x))

        self.assertEqual(output_lines[0][0].strip(), "EMPTY: M1=0; M2=0; M3=0;")
        self.assertEqual(output_lines[0][1].strip(), "FULL: M1=1; M2=0; M3=1;")
        self.assertEqual(output_lines[0][2].strip(), "MOST FILLED: M1=0,-1; M2=0,-1; M3=0,-1;")

    @unittest.expectedFailure
    def test_numberslotsbroken(self):
        output_lines = []
        fr =   ["80,M1,10,1,1,1,1,0",
                "81,M2,7,1,0,1,1,1,1,1",
                "82,M3,7,1,0,0,0,0,0,1"]
        make_stats(fr, lambda x : output_lines.append(x))

    @unittest.expectedFailure
    def test_instancenumbernotrecognized(self):
        output_lines = []
        fr =   ["80,M1,5,1,1,1,1,0",
                "81,M10,7,1,0,1,1,1,1,1",
                "82,M3,7,1,0,0,0,0,0,1"]
        make_stats(fr, lambda x : output_lines.append(x))


    def test_emptyinput(self):
        output_lines = []
        fr =   []
        make_stats(fr, lambda x : output_lines.append(x))
        self.assertEqual(output_lines[0][0].strip(), "EMPTY: M1=0; M2=0; M3=0;")
        self.assertEqual(output_lines[0][1].strip(), "FULL: M1=1; M2=0; M3=1;")
        self.assertEqual(output_lines[0][2].strip(), "MOST FILLED: M1=0,-1; M2=0,-1; M3=0,-1;")

    

suite = unittest.TestLoader().loadTestsFromTestCase(TestMakeStatFunc)
unittest.TextTestRunner(verbosity=2).run(suite)