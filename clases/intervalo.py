%% file intervalo_adriano.py
class Intervalo(object):
    def __init__(self, min, max=None):
        
        if max is None:
            max = min
        
        self.min = min
        self.max = max
        
        if min > max:
            self.min=max
            self.max=min
        
        
    def __repr__(self):
        #return "Intervalo(%s, %s)" % (self.min, self.max)
        return "Intervalo({}, {})".format(self.min, self.max)
    
    def __str__(self):
        return "[{}, {}]".format(self.min, self.max)
        
    # Para el IPython notebook:
    def _repr_html_(self):
        return "[{}, {}]".format(self.min, self.max)
    
    # def _repr_latex_(self):
    #     return "$[{}^{}]$".format(self.min, self.max)

    def __add__(self, otro):
        return Intervalo(self.min+otro.min, self.max+otro.max)
    def __sub__(self,otro):
        return Intervalo(self.min-otro.max,self.max-otro.min)
        