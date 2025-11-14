import random

class JuegoBase:

    def __init__(self, vida_inicial=3, tiempo_inicial=3):
        self._vida = vida_inicial
        self._tiempo = tiempo_inicial
        self._ronda = 1


    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, nueva_vida):
        if nueva_vida >= 0:
            self._vida = nueva_vida

    @property
    def tiempo(self):
        return self._tiempo

    @tiempo.setter
    def tiempo(self, nuevo_tiempo):
        if nuevo_tiempo >= 0:
            self._tiempo = nuevo_tiempo

    @property
    def ronda(self):
        return self._ronda

    @ronda.setter
    def ronda(self, nueva_ronda):
        if nueva_ronda > 0:
            self._ronda = nueva_ronda


class Juego(JuegoBase):

    def __init__(self):
        super().__init__(vida_inicial=3, tiempo_inicial=3)
        self._secuencia = ""
        self._teclas = 3  

    @property
    def secuencia(self):
        return self._secuencia

    @property
    def teclas(self):
        return self._teclas

    @teclas.setter
    def teclas(self, valor):
        if 1 <= valor <= 15:   
            self._teclas = valor

    def generar_secuencia(self):
        caracteres = [
            'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
            'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
            '0','1','2','3','4','5','6','7','8','9',
            '.', ';', ',', ':', '!', "?", "#"
        ]

        seq = "".join(random.choice(caracteres) for _ in range(self._teclas))
        self._secuencia = seq.lower()
        return " ".join(seq).upper()

    def verificar(self, entrada_usuario):

        if entrada_usuario == self._secuencia:
            self.tiempo = 3
            if self._teclas < 9:
                self._teclas += 1
            return True
        
        else:
            self.vida -= 1
            self.tiempo = 3
            return False
