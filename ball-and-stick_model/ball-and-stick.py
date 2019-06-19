from neuron import h, gui
from matplotlib import pyplot

#create sections
soma = h.Section(name='soma')
dend = h.Section(name='dend')

h.psection(sec=soma)

#topology
dend.connect(soma(1))
h.psection(sec=dend)
h.topology()

#geometry
## soma as a square cylinder such that diam = h
## radius = 500 micron
soma.L = soma.diam = 12.6157
dend.L = 200
dend.diam = 1
print("Surface area of soma = {}".format(soma(0.5).area()))

#plot shape
shape_window = h.PlotShape() #by default, no diam is shown
shape_window.exec_menu('Show Diam')

#biophysics
for sec in h.allsec(): #iterate over all sections
	sec.Ra = 100 ## axial resistance in Ohm*cm
	sec.cm = 1 ## membrane capacitance in microFarad/cm2

soma.insert('hh') #insert active Hodgkin-Huxley current in the soma
for seg in soma:
	seg.hh.gnabar = 0.12 ## sodium conductance in S/cm2
	seg.hh.gkbar = 0.036 # potassium conductance in S/cm2
	seg.hh.gl = 0.0003 # leak conductance in S/cm2
	seg.hh.el = -54.3 # reversal potential in mV

dend.insert('pas')
for seg in dend:
	seg.pas.g = 0.001 # passive conductance in S/cm2
	seg.pas.e = -65 # leak reversal potential in mV

for sec in h.allsec():
	h.psection(sec=sec)


#stimulation
## current pulse starting 5ms after start of the simulation
## duration 1ms, amperage 0.1 nA
## injected at the end of the dendrite
stim = h.IClamp(dend(1))
print("segment = {}".format(stim.get_segment()))
stim.delay = 5
stim.dur = 1
stim.amp = 0.1

##--what's going on in the soma
v_vec = h.Vector()
t_vec = h.Vector()
v_vec.record(soma(0.5)._ref_v)
t_vec.record(h._ref_t)
simdur = 25.0

##--what's going on in the dendrite
dend_v_vec = h.Vector()
dend_v_vec.record(dend(0.5)._ref_v)

h.tstop = simdur
h.run()

soma_plot = pyplot.plot(t_vec,v_vec, color = 'black')
dend_plot = pyplot.plot(t_vec, dend_v_vec, color = 'red')

pyplot.legend(soma_plot+dend_plot, ['soma','dend'])
pyplot.xlabel('time (ms)')
pyplot.ylabel('potential (mV)')
pyplot.show()



