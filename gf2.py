class GF2(object):
    """Galois field GF(2)."""
    
    def __init__(self, a=0):
        self.value = int(a) & 1
    
    def __add__(self, rhs):
        return GF2(self.value + GF2(rhs).value)
    
    def __mul__(self, rhs):
        return GF2(self.value * GF2(rhs).value)
    
    def __sub__(self, rhs):
        return GF2(self.value - GF2(rhs).value)
    
    def __truediv__(self, rhs):
        return GF2(self.value / GF2(rhs).value)
    
    def __repr__(self):
        return str(self.value)
    
    def __eq__(self, rhs):
        if isinstance(rhs, GF2):
            return self.value == rhs.value
        return self.value == rhs
    
    def __le__(self, rhs):
        if isinstance(rhs, GF2):
            return self.value <= rhs.value
        return self.value <= rhs
    
    def __lt__(self, rhs):
        if isinstance(rhs, GF2):
            return self.value < rhs.value
        return self.value < rhs
    
    def __int__(self):
        return self.value
    
    def __long__(self):
        return self.value
