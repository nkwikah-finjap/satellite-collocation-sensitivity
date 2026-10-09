import unittest
import numpy as np
import pandas as pd
from analysis import haversine_km,collocate,ROOT
class Tests(unittest.TestCase):
    def test_same_point(self):self.assertAlmostEqual(float(haversine_km(0,0,0,0)),0.)
    def test_one_degree_equator(self):self.assertAlmostEqual(float(haversine_km(0,1,0,0)),111.19508,places=3)
    def test_date_line(self):self.assertLess(float(haversine_km(0,-179.9,0,179.9)),23)
    def test_both_filters(self):
        f=pd.DataFrame({'latitude':[0,0,0],'longitude':[.1,3,.1],'time':['2020-01-01T10:30Z','2020-01-01T10:30Z','2020-01-01T15:30Z']})
        self.assertEqual(len(collocate(f,0,0,'2020-01-01T10:30Z',radius_km=50,time_hours=2)),1)
    def test_timezone_required(self):
        f=pd.DataFrame({'latitude':[0],'longitude':[0],'time':['2020-01-01T10:30Z']})
        with self.assertRaises(ValueError):collocate(f,0,0,'2020-01-01 10:30')
    def test_published_anchor_rows(self):
        d=pd.read_csv(ROOT/'data/published_radius_summary.csv')
        row=d[(d.gas=='CO')&(d.radius_km==50)].iloc[0]
        self.assertEqual(row.satellite_retrievals,4738);self.assertEqual(row.mean_difference,-6.62)
        self.assertEqual(len(d),23)
