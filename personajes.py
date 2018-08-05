# -*- coding: UTF-8 -*-
import pilasengine


# Personaje
class Personaje(pilasengine.actores.Actor):

    def iniciar(self):
        # Controles
        teclas = {
            self.pilas.simbolos.a: 'izquierda',
            self.pilas.simbolos.d: 'derecha',
            self.pilas.simbolos.c: 'click',
        }

        # Definimos el control del Personajeq
        mi_control = self.pilas.control.Control(teclas)

        # Propiedades del Personaje
        self.y = -210
        self.x = 0
        self.rotacion = 90
        self.radio_de_colision = 25
        self.imagen = self.pilas.imagenes.cargar('src/img/img_soldier.png')
        self.escala = 0.25
        figura_personaje = self.pilas.fisica.Circulo(0, 0, 25, dinamica=False, sensor=False)
        self.figura_de_colision = figura_personaje

        # Habilidades del Personaje
        self.aprender('dispararconclick', municion='Balitas', angulo_salida_disparo=self.rotacion,
                      frecuencia_de_disparo=7, control=mi_control, distancia=57)
        self.aprender('moverseconelteclado', control=mi_control)
        self.aprender('rotarconmouse')

    def eliminar(self):
        self.eliminar()


# Mira
class Mira(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = self.pilas.imagenes.cargar('src/img/mira.png')
        self.escala = 0.12
        self.z = -3
        self.aprender('seguiralmouse')
