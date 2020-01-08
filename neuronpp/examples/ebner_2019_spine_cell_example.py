from neuron import h
from neuron.units import mV
import matplotlib.pyplot as plt

from neuronpp.cells.core.netstim_cell import NetStimCell
from neuronpp.cells.core.spine_cell import SpineCell
from neuronpp.cells.ebner2019_cell import Ebner2019Cell
from neuronpp.utils.Record import Record
from neuronpp.utils.run_sim import RunSim


class Ebner2019SpineCell(Ebner2019Cell, SpineCell):
    def __init__(self, name):
        SpineCell.__init__(self, name)
        Ebner2019Cell.__init__(self, name)


WEIGHT = 0.0035		# µS, conductance of (single) synaptic potentials
WARMUP = 200


if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.dt = 0.025

    # define cell
    cell = Ebner2019SpineCell(name="cell")
    cell.load_morpho(filepath='morphologies/swc/my.swc', seg_per_L_um=1, add_const_segs=11)
    cell.add_spines(spine_number=10, head_nseg=10, neck_nseg=10, sections='dend')
    cell.add_soma_mechanisms()
    cell.add_apical_mechanisms(sections='dend head neck')
    cell.add_4p_synapse(sec_names="head", loc=1)  # add synapse at the top of each spine's head

    # stimulation
    stim = NetStimCell("stim_cell").add_netstim("stim1", start=WARMUP + 1, number=300, interval=1)
    cell.add_netcons(source=stim, weight=WEIGHT, delay=1)

    # create plots
    rec_w = Record(cell.filter_point_processes(pp_type_name="Syn4P", sec_names="head[0][0]"), variables="w")
    rec_v = Record(cell.filter_secs(sec_names="head[0]"), locs=1.0, variables="v")

    # init and run
    h.finitialize(-70 * mV)
    sim = RunSim(warmup=WARMUP)
    sim.run(runtime=500)

    # plot
    rec_w.plot()
    rec_v.plot()
    plt.show()
