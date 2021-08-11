import unittest
from unittest.mock import Mock

from rescan import scanner


class TestScanner(unittest.TestCase):
    """core test cases."""

    def test_mergeAreas_handle_holes(self):
        colorCode = 'BLACK'
        
        colorAreaA = Mock()
        colorAreaA.getBoundingRectangle.return_value = (0, -1, 10, -1)
        colorAreaA.colorCode = colorCode
        
        colorAreaB = Mock()
        colorAreaB.getBoundingRectangle.return_value = (10, -1, 10, -1)
        colorAreaB.colorCode = colorCode
        
        colorAreaC = Mock()
        colorAreaC.getBoundingRectangle.return_value = (20, -1, 10, -1)
        colorAreaC.colorCode = colorCode
        
        sut = scanner.Scanner()
        
        groups = sut.groupAreas([colorAreaA, colorAreaC, colorAreaB])
        
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].xMin, 0)
        self.assertEqual(groups[0].xMax, 30)
        
    def test_createStrips(self):
        colorCode = 'BLACK'
        
        colorAreaGroupA = Mock()
        colorAreaGroupA.compute_xPos.return_value = 1
        
        colorAreaGroupB = Mock()
        colorAreaGroupB.compute_xPos.return_value = 2
        
        colorAreaGroupC = Mock()
        colorAreaGroupC.compute_xPos.return_value = 3
        
        colorAreaGroupD = Mock()
        colorAreaGroupD.compute_xPos.return_value = 4
        
        colorAreaGroupE = Mock()
        colorAreaGroupE.compute_xPos.return_value = 0
        
        sut = scanner.Scanner()
        strips = sut.createStrips([colorAreaGroupA, colorAreaGroupC, colorAreaGroupB, colorAreaGroupD, colorAreaGroupE])
        
        self.assertEqual(len(strips), 5)
        self.assertEqual(strips[0].xPos, 0)
        self.assertEqual(strips[1].xPos, 1)
        self.assertEqual(strips[2].xPos, 2)
        self.assertEqual(strips[3].xPos, 3)
        self.assertEqual(strips[4].xPos, 4)

    def test_createStrips_raise(self):
        colorCode = 'BLACK'
        
        colorAreaGroupA = Mock()
        colorAreaGroupA.compute_xPos.return_value = 1
        
        colorAreaGroupB = Mock()
        colorAreaGroupB.compute_xPos.return_value = 1
        
        sut = scanner.Scanner()
        
        with self.assertRaises(ValueError):
            sut.createStrips([colorAreaGroupA, colorAreaGroupB])

if __name__ == '__main__':
    unittest.main()
