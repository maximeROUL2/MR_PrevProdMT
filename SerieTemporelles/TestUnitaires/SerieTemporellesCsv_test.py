import unittest

import pandas
import numpy

from MR_PrevProdMT.SerieTemporelles.SerieTemporelles import SerieTemporelles

class TestSerieTemporellesCsv(unittest.TestCase):

    def setUp(self) -> None:
        ar = numpy.array([['01-02-2007', 1], ['01-03-2007', 2], ['01-04-2007', 3], ['01-05-2007', 4]
                          ['01-06-2007', 5], ['01-07-2007', 6], ['01-0Z-2007', 1], ['01-02-2007', 2]
                          ['01-02-2007', 3], ['01-02-2007', 4], ['01-02-2007', 5],['01-02-2007', 6]])
        df = pandas.DataFrame(ar, columns=['Date', 'Serie'])

        self.appel = SerieTemporelles(df, 'Date', 'Serie')

    def test_erreur_holt_winters(self):
        """Test de la fonction holt_winters"""
        test = self.appel.analyse_erreur_holt_winters(3)

        test.assertIn(test[0], [0, 1])
        test.assertIn(test[1], [0, 1])


if __name__ == '__main__':
    unittest.main()
