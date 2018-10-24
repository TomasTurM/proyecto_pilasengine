# -*- coding: UTF-8 -*-
import pilasengine


# Sangre
class Sangre(pilasengine.actores.Actor):

    def iniciar(self, x, y):
        self.x = x
        self.y = y
        self.imagen = self.pilas.imagenes.cargar('src/img/blood.png')
        self.escala = 0.25
        self.pilas.tareas.una_vez(2, self.eliminar)

# NPC (Zombies)
class Zombie(pilasengine.actores.Actor):

    def iniciar(self):
        self.vida = 100
        self.resistencia = 0
        self.x = 250
        self.y = 100
        self.imagen = self.pilas.imagenes.cargar('src/img/zombie.png')
        self.espejado = True
        self.escala = 0.25
        self.figura = self.pilas.fisica.Circulo(0, 0, 25, dinamica=False, sensor=False)
        self.radio_de_colision = 25

        self.hit = None

        # Barra de vida
        self.barra_vida = self.pilas.actores.Energia()
        self.barra_vida.escala = 0.5

    def terminar_hit(self):
        self.hit.terminar()

    def sangre(self):
        sangre_x = self.x
        sangre_y = self.y
        self.sangre = self.pilas.actores.Sangre(sangre_x, sangre_y)
        """
        self.sangre.imagen = self.pilas.imagenes.cargar('src/img/blood.png')
        self.sangre.escala = 0.25
        self.sangre.x = sangre_x
        self.sangre.y = sangre_y
        self.pilas.tareas.una_vez(2, self.sangre.eliminar)
        """

    def parar_figura(self):
        self.eliminar_habilidades()
        self.eliminar_comportamientos()
        self.eliminar_figura(figura)
        self.figura.x = -300
        self.figura.y = 0
        self.eliminar()

    def actualizar(self):
        self.barra_vida.x = self.x
        self.barra_vida.y = self.y + 30
        self.x = self.figura.x
        self.y = self.figura.y
 

# Habilidad - Movimiento de Zombie con Parametros -
class MovimientoZombie(pilasengine.habilidades.Habilidad):

    def iniciar(self, receptor, velocidad, pilas):
        self.receptor = receptor
        self.velocidad = velocidad
        self.pilas = pilas
        self.pilas.tareas.siempre(0, self.mover_izq)

    def mover_izq(self):
        self.receptor.figura.x -= self.velocidad


# Actor invisible - Spawneador de Zombies
class ZombieSpawn(pilasengine.actores.actor_invisible.ActorInvisible):

    def iniciar(self):
        self.x = 400
        self.y = 0

    def spawn(self, z):
        z.figura.x = 400
        z.figura.y = self.pilas.azar(-140, 180)
        z.resistencia = self.pilas.azar(0, 60)

        velocidad = self.pilas.azar(2, 5)
        z.aprender("MovimientoZombie", velocidad, self.pilas)
