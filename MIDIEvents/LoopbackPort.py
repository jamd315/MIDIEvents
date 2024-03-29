import logging
import threading

import mido

logger = logging.getLogger("MIDIEvents")


class LoopbackPort(mido.ports.BaseIOPort):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._callback = None

    def _open(self, callback=None):
        self._callback_lock = threading.RLock()

    def _send(self, msg):
        if self._callback:
            self._callback(msg)
            logger.debug("{} message sent to callback".format(msg))
        else:
            self._messages.append(msg)
            logger.debug("{} message sent to internal queue".format(msg))

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, func):
        with self._callback_lock:
            if func:
                for msg in self.iter_pending():
                    func(msg)
            self._callback = func
