import os
import unittest
import numpy as np
from neuron import h
from neuronpp.cells.cell import Cell

class TestCellAddSectionDefault(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cell = Cell(name="cell")
        cls.soma = cls.cell.add_sec("soma", add_leak=True)
        
    def test_add_soma_L_default(self):
        self.assertEqual(self.soma.hoc.L, 100.)

    def test_add_soma_diam_default(self):
        self.assertEqual(self.soma.hoc.diam, 500.)

    def test_add_soma_cm_default(self):
        self.assertEqual(self.soma.hoc.cm, 1.)
        
    def test_add_soma_ra_default(self):
        self.assertEqual(self.soma.hoc.Ra, 35.4)

    def test_add_soma_g_pas_default(self):
        self.assertEqual(self.soma.hoc.g_pas, 0.001)

    def test_add_soma_e_pas_default(self):
        self.assertEqual(self.soma.hoc.e_pas, -70.0)


class TestCellAddSectionLeak(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cell1 = Cell(name="cell1")
        cls.soma1 = cell1.add_sec("soma", add_leak=True)
        cell2 = Cell(name="cell2")
        cls.soma2 = cell2.add_sec("soma", g_leak=0.002)
        cell3 = Cell(name="cell3")
        cls.soma3 = cell3.add_sec("soma", rm=1/0.003)
        cell4 = Cell(name="cell4")
        cls.soma4 = cell4.add_sec("soma", E_leak=-80)
        #no leak but add leak
        cls.cell5 = Cell(name="cell5")
        cls.soma5 = cls.cell5.add_sec("soma", add_leak=True)
        cls.dend = h.Section("dend", "cell5")
        cls.dend.insert("pas")
        cell6 = Cell(name="cell6")
        cls.soma6 = cell6.add_sec("soma", add_leak=True)
        cls.soma6.hoc.insert("pas")
        cell6.set_leak("soma", Rm=1000, E_leak = -77, g_leak=0.002)


    def test_cell1_g_pas(self):
        self.assertEqual(self.soma1.hoc.g_pas, 0.001)

    def test_cell1_E_pas(self):
        self.assertEqual(self.soma1.hoc.e_pas, -70.0)

    def test_cell2_g_pas(self):
        self.assertEqual(self.soma2.hoc.g_pas, 0.002)

    def test_cell2_E_pas(self):
        self.assertEqual(self.soma2.hoc.e_pas, -70.0)

    def test_cell3_g_pas(self):
        self.assertTrue(np.isclose(self.soma3.hoc.g_pas, 0.003))

    def test_cell3_E_pas(self):
        self.assertEqual(self.soma3.hoc.e_pas, -70.0)

    def test_cell4_g_pas(self):
        self.assertEqual(self.soma4.hoc.g_pas, 0.001)

    def test_cell4_E_pas(self):
        self.assertEqual(self.soma4.hoc.e_pas, -80.0)

    def test_cell5(self):
        self.cell5.set_leak("soma", E_leak=-80)
        self.assertEqual(self.soma5.hoc.e_pas, -80)

    def test_cell5_dend(self):

        self.cell5.set_leak(self.dend, E_leak=-80)
        self.assertEqual(self.dend.e_pas, -80)

    def test_cell5_dend_rm(self):
        self.cell5.set_leak(self.dend, Rm=10000)
        self.assertEqual(self.dend.g_pas, 1/10000)

    def test_cell5_dend_g_pas(self):
        self.cell5.set_leak(self.dend, g_leak=0.02)
        self.assertEqual(self.dend.g_pas, 0.02)

    def test_cell6_soma_e_leak(self):
        self.assertEqual(self.soma6.hoc.g_pas, 0.002)

    def test_cell6_soma_g_leak(self):
        self.assertEqual(self.soma6.hoc.e_pas, -77)


class TestFiltering(unittest.TestCase):
    def test_distance(self):
        path = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(path, "..",
                                "commons/morphologies/asc/cell1.asc")
        cell = Cell("cell")
        cell.load_morpho(filepath=filepath)
        soma = cell.filter_secs("soma")

        # Filter sections by distance to the soma (return only those distance > 1000 um)
        far_secs = cell.filter_secs(obj_filter=lambda s: h.distance(soma.hoc(0.5), s.hoc(0.5)) > 1000)
        self.assertEqual(len(far_secs), 32)
if __name__ == '__main__':
    unittest.main()
