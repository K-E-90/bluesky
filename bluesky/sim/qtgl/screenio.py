try:
    # Try Qt4 first
    from PyQt4.QtCore import QObject, QTimer, pyqtSlot
    from PyQt4.QtCore import QCoreApplication as qapp
except ImportError:
    # Else PyQt5 imports
    from PyQt5.QtCore import QObject, QTimer, pyqtSlot
    from PyQt5.QtCore import QCoreApplication as qapp
import numpy as np
import time

# Local imports
from ...ui.qtgl import ACDataEvent, RouteDataEvent, PanZoomEvent, SimInfoEvent, StackTextEvent, ShowDialogEvent, DisplayFlagEvent, StackTextEventType


class ScreenIO(QObject):
    # =========================================================================
    # Settings
    # =========================================================================
    # Update rate of simulation info messages [Hz]
    siminfo_rate = 2

    # Update rate of aircraft update messages [Hz]
    acupdate_rate = 5

    # =========================================================================
    # Slots
    # =========================================================================
    @pyqtSlot()
    def send_siminfo(self):
        t  = time.time()
        dt = t - self.prevtime
        qapp.postEvent(qapp.instance(), SimInfoEvent((self.sim.samplecount - self.prevcount) / dt, self.sim.simdt, self.sim.simt, self.sim.traf.ntraf, self.sim.mode))
        self.prevtime  = t
        self.prevcount = self.sim.samplecount

    @pyqtSlot()
    def send_aircraft_data(self):
        data       = ACDataEvent()
        data.id    = list(self.sim.traf.id)
        data.lat   = np.array(self.sim.traf.lat, dtype=np.float32, copy=True)
        data.lon   = np.array(self.sim.traf.lon, dtype=np.float32, copy=True)
        data.alt   = np.array(self.sim.traf.alt, copy=True)
        data.tas   = np.array(self.sim.traf.tas, copy=True)
        data.iconf = np.array(self.sim.traf.iconf, copy=True)
        data.trk   = np.array(self.sim.traf.trk, dtype=np.float32, copy=True)
        qapp.postEvent(qapp.instance(), data)

    # =========================================================================
    # Functions
    # =========================================================================
    def __init__(self, sim):
        super(ScreenIO, self).__init__()

        # Keep reference to parent simulation object for access to simulation data
        self.sim = sim

        # Timing bookkeeping counters
        self.prevtime = 0.0
        self.prevcount = 0

        # Output event timers
        self.siminfo_timer = QTimer()
        self.siminfo_timer.timeout.connect(self.send_siminfo)
        self.siminfo_timer.start(1000/self.siminfo_rate)

        self.acupdate_timer = QTimer()
        self.acupdate_timer.timeout.connect(self.send_aircraft_data)
        self.acupdate_timer.start(1000/self.acupdate_rate)

    def moveToThread(self, target_thread):
        self.siminfo_timer.moveToThread(target_thread)
        self.acupdate_timer.moveToThread(target_thread)
        super(ScreenIO, self).moveToThread(target_thread)

    def echo(self, text):
        qapp.postEvent(qapp.instance(), StackTextEvent(text))

    def zoom(self, zoomfac):
        qapp.postEvent(qapp.instance(), PanZoomEvent(PanZoomEvent.Zoom, zoomfac))

    def pan(self, pan, absolute=False):
        if absolute:
            qapp.postEvent(qapp.instance(), PanZoomEvent(PanZoomEvent.PanAbsolute, pan))
        else:
            qapp.postEvent(qapp.instance(), PanZoomEvent(PanZoomEvent.Pan, pan))

    def showroute(self, acid):
        data       = RouteDataEvent()
        data.acidx = self.sim.traf.id2idx(acid)
        if data.acidx >= 0:
            route = self.sim.traf.route[data.acidx]
            n_segments   = len(route.wplat) + 1
            data.lat     = np.empty(n_segments, dtype=np.float32)
            data.lat[0]  = self.sim.traf.lat[data.acidx]
            data.lat[1:] = route.wplat
            data.lon     = np.empty(n_segments, dtype=np.float32)
            data.lon[0]  = self.sim.traf.lon[data.acidx]
            data.lon[1:] = route.wplon
        qapp.postEvent(qapp.instance(), data)

    def show_file_dialog(self):
        qapp.postEvent(qapp.instance(), ShowDialogEvent())
        return ''

    def feature(self, switch, argument=''):
        qapp.postEvent(qapp.instance(), DisplayFlagEvent(switch, argument))

    def event(self, event):
        if event.type() == StackTextEventType:
            self.sim.stack.stack(event.text)
        return True