import numpy as np
from neuron import h, gui
from matplotlib import pyplot

class BallAndStick(object):
	"""Two-section cell: A soma with active channels and
	a dendrite with passive properties."""
	def __init__(self):
		self.create_sections()
		self.build_topology()
		self.build_subsets()
		self.define_geometry()
		self.define_biophysics()

	def create_sections(self):
		"""Create the sections of the cell."""
		self.soma = h.Section(name='soma',cell=self)
		self.dend = h.Section(name='dend',cell=self)

	def build_topology(self):
		"""Connect the sections of the cell."""
		self.dend.connect(self.soma(1))

	def define_geometry(self):
		"""Set the 3D geometry of the cell."""
		self.soma.L = self.soma.diam = 12.6157
		self.dend.L = 200
		self.dend.diam = 1
		self.dend.nseg = 5
		h.define_shape() # Translate into 3D points

	def define_biophysics(self):
		"""Assign the membrane properties across the cell."""
		for sec in self.all:
			sec.Ra = 100
			sec.cm = 1
		# Insert active Hodgkin-Huxley current in the soma
		self.soma.insert('hh')
		for seg in self.soma:
			seg.hh.gnabar = 0.12 
			seg.hh.gkbar = 0.036
			seg.hh.gl = 0.0003
			seg.hh.el = -54.3
		# Insert passive current in the dendrite
		self.dend.insert('pas')
		for seg in self.dend:
			seg.pas.g = 0.001
			seg.pas.e = -65

	def build_subsets(self):
		"""Build subset lists. For now we define 'all'."""
		self.all = h.SectionList()
		self.all.wholetree(sec=self.soma)

#############
def attach_current_clamp(cell, delay=5, dur=1, amp=.1, loc=1):
		"""Attach a current Clamp to a cell.
		:param cell: Cell object to attach the current clamp.
		:param delay: Onset of the injected current
		:param dur: Duration of the stimulus
		:param amp: Magnitude of the current
		:param loc: Location on the cell object where the stimulus is placed."""
		
		stim = h.IClamp(cell.dend(loc))
		stim.delay = delay
		stim.dur = dur
		stim.amp = amp
		return stim

def set_recording_vectors(cell):
		"""Set soma, dendrite and time recording vectors.
		:param cell: Cell to record from.
		:return: the soma, dendrite and time vectors as a tuple."""
		
		soma_v_vec = h.Vector()
		dend_v_vec = h.Vector()
		t_vec = h.Vector()
		soma_v_vec.record(cell.soma(0.5)._ref_v)
		dend_v_vec.record(cell.dend(0.5)._ref_v)
		t_vec.record(h._ref_t)
		return soma_v_vec, dend_v_vec, t_vec

def simulate(tstop=25):
		"""Initialize and run the simulation.
		:param tstop: Duration of the simulation."""
		
		h.tstop = tstop
		h.run()

def show_output(soma_v_vec, dend_v_vec, t_vec, new_fig=True):
		"""Draw the output.
		:param soma_v_vec: Membrane potential vector at the soma.
		:param dend_v_vec: Membrane potential vector at the dendrite.
		:param t_vec: Timestamp vector.
		:param new_fig: Flag to create a new figure."""
		
		if new_fig:
			pyplot.figure(figsize=(8,4))
		soma_plot = pyplot.plot(t_vec,soma_v_vec, color='black')
		dend_plot = pyplot.plot(t_vec,dend_v_vec, color='red')
		pyplot.legend(soma_plot+dend_plot, ['soma','dend(0.5)'])
		pyplot.xlabel('time (ms)')
		pyplot.ylabel('membrane potential (mV)')

cell = BallAndStick()
#h.psection(sec=cell.dend)
stim = attach_current_clamp(cell)
soma_v_vec, dend_v_vec, t_vec = set_recording_vectors(cell)
simulate()
show_output(soma_v_vec,dend_v_vec,t_vec)
pyplot.show()