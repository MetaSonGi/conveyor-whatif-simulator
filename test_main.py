import unittest,json
from pathlib import Path
from main import *
class Tests(unittest.TestCase):
    def sample(self):return json.loads(Path(__file__).with_name('sample-input.json').read_text(encoding='utf-8'))

    def test_serial_queue(self):
        jobs=[{'id':'a','arrival_s':0},{'id':'b','arrival_s':0}]
        o=simulate(jobs,[{'id':'s','process_s':3,'servers':1}]);self.assertEqual(o['makespan_s'],6);self.assertEqual(o['average_lead_time_s'],4.5)
    def test_pause_resume_boundary(self):
        self.assertEqual(complete(0,3,[(1,4)]),6);self.assertEqual(complete(0,1,[(1,4)]),1)
        o=simulate([{'id':'a','arrival_s':2}],[{'id':'s','process_s':1,'servers':1,'downtime':[[1,4]]}]);self.assertEqual(o['timeline'][0]['start_s'],4)
    def test_parallel_and_empty(self):
        o=run(self.sample());self.assertGreater(o['makespan_saved_s'],0)
        self.assertEqual(simulate([],[] )['makespan_s'],0)
    def test_invalid(self):
        with self.assertRaises(ValueError):simulate([{'id':'a','arrival_s':0}],[{'id':'s','process_s':2,'servers':0}])
        with self.assertRaises(ValueError):simulate([], [{'id':'s','process_s':2,'servers':1,'downtime':[[1,4],[3,5]]}])

if __name__=="__main__":unittest.main()
