import time


class TwinService(object):
    """
    inspired by roblox TwinService
    """

    class LinearTwin(object):

        def __init__(self, a: int, b: int, length: float) -> None:

            self._a = a
            self._b = b

            self._c = a

            self.length = length

            self._finish_time = time.time() + length
            self._start_time = time.time()
            self._finished = False
            self._completed = 0.0

        def update(self) -> int:
            """
            returns c' current position in terms of a and b
            """

            if not self._finished:
                if self._finish_time <= time.time():
                    self._finished = True
            else:
                return self._b

            self._completed = (time.time() - self._start_time) / self.length

            self._c = self._a + self._completed * (self._b - self._a)

            return self._c