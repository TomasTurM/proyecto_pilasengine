# -*- coding: UTF-8 -*-
import pilasengine


# Barrera
class Barrera(pilasengine.actores.Actor):

    def iniciar(self):
        self.x = -250
        self.y = 0
        self.vida = 100
        colisiones_barrera = self.pilas.fisica.Rectangulo(0, 0, 100, 500, sensor=False, dinamica=False)
        self.figura_de_colision = colisiones_barrera
        self.imagen = self.pilas.imagenes.cargar('src/img/barrier.jpg')

        self.barra_vida_barrera = self.pilas.actores.Energia()
        self.barra_vida_barrera.escala = 1
        self.barra_vida_barrera.x = 0
        self.barra_vida_barrera.y = 200


# Pared Invisible Superior
class ParedSup(pilasengine.actores.actor_invisible.ActorInvisible):

    def iniciar(self):
        self.x = 60
        self.y = 200
        colision_sup = self.pilas.fisica.Rectangulo(0, 0, 525, 10, sensor=False, dinamica=False)
        self.figura_de_colision = colision_sup


# Pared Invisible Inferior
class ParedInf(pilasengine.actores.Actor):

    def iniciar(self):
        self.x = 60
        self.y = -150
        colision_inf = self.pilas.fisica.Rectangulo(0, 0, 525, 10, sensor=False, dinamica=False)
        self.figura_de_colision = colision_inf
        self.imagen = self.pilas.imagenes.cargar('src/img/cerco_inf.png')
        self.escala = 0.1
