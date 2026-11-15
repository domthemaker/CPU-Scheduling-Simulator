import unittest
from algorithms import schedule

SAMPLE = [('P1', 0, 6), ('P2', 1, 4), ('P3', 2, 2), ('P4', 3, 5)]


class SchedulingTests(unittest.TestCase):
    def test_sample_averages(self):
        expected = {
            'FCFS': (9.75, 5.50, 5.50),
            'SJF': (9.25, 5.00, 5.00),
            'SRTF': (8.50, 4.25, 2.25),
            'Round Robin': (12.00, 7.75, 2.75),
        }
        for name, averages in expected.items():
            with self.subTest(algorithm=name):
                self.assertEqual(schedule(SAMPLE, name, 3)[2], averages)

    def test_idle_time(self):
        for name in ('FCFS', 'SJF', 'SRTF', 'Round Robin'):
            with self.subTest(algorithm=name):
                segments, rows, averages = schedule([('P1', 3, 2)], name, 2)
                self.assertEqual(segments, [('IDLE', 0, 3), ('P1', 3, 5)])
                self.assertEqual(rows[0][3:], (5, 2, 0, 0))


if __name__ == '__main__':
    unittest.main()

