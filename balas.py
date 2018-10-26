# -*- coding: UTF-8 -*-
import pilasengine

# Bala
class Balitas(pilasengine.actores.Actor):
    def iniciar(self):
        # Propiedades de Bala
        self.radio_de_colision = 5
        self.figura_balita = self.pilas.fisica.Circulo(0, 0, 5, dinamica=False, sensor=False)
        self.imagen = self.pilas.imagenes.cargar('src/img/bullet_v2.png')
        self.espejado = True

        # Habilidades de Bala
        self.aprender('eliminarsesisaledepantalla')

    def actualizar(self):
        self.figura_balita.x = self.x
        self.figura_balita.y = self.y
