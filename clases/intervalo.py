# -*- coding: utf-8 -*- 

class Intervalo(object):
    """
    Se define la clase 'Intervalo', y los métodos para la aritmética básica de intervalos, 
    es decir, suma, resta, multiplicación y división. Se incluyen otras funciones
    que serán útiles.
    """
    def __init__(self,lo,hi=None):
        """ 
        Definimos las propiedades del objeto Intervalo a partir de sus bordes,
        lo y hi, donde lo <= hi. En el caso en que el intervalo sólo tenga
        un número, éste se interpreta como un intervalo 'delgado' o 'degenerado'.
        """
        if hi is None:
            hi = lo
        elif (hi < lo):
            lo, hi = hi, lo
        
        self.lo = lo
        self.hi = hi
        
    def __repr__(self):
        return "Intervalo [{},{}]".format(self.lo,self.hi)
    
    def __str__(self):
        # Esta función sirve con 'print'
        return "[{},{}]".format(self.lo,self.hi)

    def _repr_html_(self):
        return "[{}, {}]".format(self.lo, self.hi)
    
    def _repr_latex_(self):
        return "$[{}, {}]$".format(self.lo, self.hi)

    # Aquí vienen las operaciones aritméticas
    def __add__(self, otro):
        """
        Suma de intervalos
        """
        try:
            return Intervalo(self.lo + otro.lo, self.hi + otro.hi)
        except:
            return self + Intervalo(otro)

    def __radd__(self, otro):
        return self + otro
        
    def __mul__(self, otro):
        try:
            S=[self.lo*otro.lo , self.lo * otro.hi , self.hi * otro.lo , self.hi * otro.hi ]
            return Intervalo( min(S), max(S) )
        except:
            return self * Intervalo(otro)

    def __rmul__(self, otro):
        return self * otro

    # Esta es la funcion igualdad para intervalos
    def __eq__(self, otro):
        if self.lo == otro.lo and self.hi == otro.hi:
            return True
        else:
            return False

    def __and__(self, otro):
        if not isinstance(otro,Intervalo):
            otro = Intervalo(otro)
        if (self.lo > otro.hi) | (self.hi < otro.lo):
            return None
        else:
            a = max( self.lo, otro.lo )
            b = min( self.hi, otro.hi )
            return Intervalo(a,b)
    
    def __rand__(self, otro):
        return self & otro
    
    #negativo del intervalo
    def __neg__(self):
        return Intervalo(-self.hi, -self.lo)
        
    def __div__(self, otro):
        if otro.lo <= 0 <= otro.hi:
            raise ZeroDivisionError
        else:
            return Intervalo.__mul__(self,Intervalo(1./(otro.hi),1./(otro.lo)))

    def middle(self):
        '''
        Calcula el punto medio del intervalo
        '''
        return (self.lo+self.hi)/2
        
    def radio(self):
        '''        
        Calcula el radio del intervalo
        '''
        return (self.hi-self.lo)/2
        
    def width(self):
        '''
        Cacula la anchura
        '''
        return self.hi-self.lo
        
    def Abs(self):
        
        return max([abs(self.lo),abs(self.hi)])

# A partir de aqui vamos a definir EL METODO para la funcion seno sobre
#la calse intervalos


def sin(self):
    import numpy as np
    if (self.hi - self.lo) >= (2.*np.pi):  # El intervalo corresponde a todo el dominio de sin
    
        return Intervalo(-1,1)
    
    else:
        
        Smin = ( (self.lo/(2.*np.pi)) - int(self.lo/(2.*np.pi)) )*(2.*np.pi)  #escalamiento del intervalo para (0,2pi)
        Smax = ( (self.hi/(2.*np.pi)) - int(self.hi/(2.*np.pi)) )*(2.*np.pi)
        

        if Smax == 0:       # para tomar angulo cero como 2pi
            Smax = 2.*np.pi
        if Smin == 0:
            Smin = 2.*np.pi

        if Smin < 0: #Para cotas negativas, se pasa al intervalo (0,2pi)
            Smin = Smin + (2.*np.pi)
        if Smax < 0:
            Smax = Smax + (2.*np.pi)
            
    
#        print Smin,Smax
        
        if Smax < Smin:  #Orden invertido, se consideran condiciones periodicas
        
            if Smin <= (1.5*np.pi) and Smax >= (np.pi):    
                return Intervalo(-1,1)
            
            if Smin > (1.5*np.pi) and Smax < (np.pi):      #Parte monotona creciente
                return Intervalo(np.sin(Smin),np.sin(Smax))
            
            
        else:
            
            if Smin <= (0.5*np.pi) and Smax >= (1.5*np.pi):
                return Intervalo(-1,1)
            
            if Smin > (np.pi) and Smax < (1.5*np.pi):     #Parte monotona decreciente
                return Intervalo(np.sin(Smax),np.sin(Smin))
            
# Dividimos regiones (0,pi) y (pi,2pi)

            if Smax <= (np.pi):
                
                if Smin <= (0.5*np.pi) and Smax >= (0.5*np.pi):
                    return Intervalo(min(np.sin(Smax),np.sin(Smin)),1)
                
                if Smax < (0.5*np.pi):        # parte creciente
                    return Intervalo(0,np.sin(Smax))
                
        
            if Smin >= (np.pi):
                
                if Smin <= (1.5*np.pi) and Smax >= (1.5*np.pi):
                    return Intervalo(-1,max(np.sin(Smax),np.sin(Smin)))
                
                if Smin > (1.5*np.pi):          #parte creciente
                    return Intervalo(-1,np.sin(Smax))