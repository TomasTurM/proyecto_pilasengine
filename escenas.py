# -*- coding: UTF-8 -*-
import pilasengine


# Escena de menu principal
class EscenaMenu(pilasengine.escenas.Escena):

    def iniciar(self):
        fondo = self.pilas.fondos.Fondo()
        fondo.imagen = self.pilas.imagenes.cargar('src/img/zombie-background.jpg')
        fondo.escala = 0.45
        self.titulo_menu()
        self.boton_iniciar = self.pilas.actores.Boton()
        self.boton_iniciar.imagen = self.pilas.imagenes.cargar('src/img/boton_iniciar.png')
        self.boton_iniciar.conectar_presionado(self.translacion_controles)
        self.boton_iniciar.escala = 0.35
        self.boton_iniciar.x = 0
        self.boton_iniciar.y = -60
        self.boton_iniciar.transparencia = 100
        self.pilas.tareas.agregar(8, self.aparece_boton)

    def titulo_menu(self):
        self.titulo = self.pilas.actores.Actor()
        self.titulo.imagen = self.pilas.imagenes.cargar('src/img/titulo_menu.png')
        self.titulo.escala = 1.5
        self.titulo.y = 300
        self.titulo.y = [85], 8

    def translacion_controles(self):
        self.titulo.transparencia = [100], 3
        self.boton_iniciar.transparencia = [100], 3
        self.pilas.tareas.agregar(4, self.start)

    def start(self):
        self.pilas.escenas.EscenaControles()

    def aparece_boton(self):
        self.boton_iniciar.transparencia = [0], 3


# Escena de controles
class EscenaControles(pilasengine.escenas.Escena):
    def iniciar(self):
        fondo = self.pilas.fondos.Fondo()
        fondo.imagen = self.pilas.imagenes.cargar('src/img/weapons_room_background.png')
        fondo.escala = 2
        self.titulo_controles()
        self.imagen_controles()
        self.boton_ready()
        self.inicio_escena()

    def titulo_controles(self):
        self.titulo = self.pilas.actores.Actor()
        self.titulo.imagen = self.pilas.imagenes.cargar('src/img/controles.png')
        self.titulo.escala = 0.85
        self.titulo.y = 185
        self.titulo.transparencia = 100

    def imagen_controles(self):
        self.imagen_controles = self.pilas.actores.Actor()
        self.imagen_controles.imagen = self.pilas.imagenes.cargar('src/img/imagen_controles.png')
        self.imagen_controles.escala = 0.65
        self.imagen_controles.y = 25
        self.imagen_controles.transparencia = 100

    def boton_ready(self):
        self.btn_ready = self.pilas.actores.Boton()
        self.btn_ready.imagen = self.pilas.imagenes.cargar('src/img/btn_ready.png')
        self.btn_ready.escala = 0.50
        self.btn_ready.y = -150
        self.btn_ready.transparencia = 100
        self.btn_ready.conectar_presionado(self.translacion_juego)

    def inicio_escena(self):
        self.titulo.transparencia = [0], 3
        self.imagen_controles.transparencia = [0], 3
        self.btn_ready.transparencia = [0], 3

    def translacion_juego(self):
        self.titulo.transparencia = [100], 3
        self.imagen_controles.transparencia = [100], 3
        self.btn_ready.transparencia = [100], 3
        self.pilas.tareas.agregar(3, self.ready)

    def ready(self):
        self.pilas.escenas.EscenaJuego()


# Escena de juego
class EscenaJuego(pilasengine.escenas.Escena):

    def iniciar(self):
        fondo = self.pilas.fondos.Fondo()
        fondo.imagen = self.pilas.imagenes.cargar('src/img/fondo_suelo.jpg')
        fondo.escala = 1.60

        self.pilas.fisica.eliminar_paredes()

        self.contador_muertes = 0

        # Invocacion Spawn
        self.zombie_spawn = self.pilas.actores.ZombieSpawn()

        # Invocacion de Personaje
        self.personaje = self.pilas.actores.Personaje()

        # Invocacion de Barrera
        self.barrera = self.pilas.actores.Barrera()

        self.pared_sup = self.pilas.actores.ParedSup()

        self.pared_inf = self.pilas.actores.ParedInf()

        # Invocacion de mira
        self.mira = self.pilas.actores.Mira()

        # Grupo de Enemigos
        self.enemigos = self.pilas.actores.Grupo()

        self.pilas.colisiones.agregar("balitas", "zombie", self.hit_zombie)

        self.pilas.colisiones.agregar("balitas", "barrera", self.auto_ataque)

        self.pilas.colisiones.agregar("zombie", "barrera", self.zombie_hit_tarea)

        # Spawn
        self.pilas.tareas.siempre(1, self.spawn)

    def hit_zombie(self, balitas, zombie):
        balitas.eliminar()
        zombie.vida -= 75 - zombie.resistencia
        zombie.barra_vida.progreso = zombie.vida

        if zombie.vida <= 0:
            zombie.barra_vida.eliminar()

            if zombie.hit is not None:
                zombie.terminar_hit()

            zombie.sangre(zombie.x, zombie.y)
            pilas.eliminar_colisiones_con_actor(zombie)
            self.contador_muertes = self.contador_muertes + 1

    def zombie_hit_tarea(self, zombie, barrera):
        zombie.hit = self.pilas.tareas.siempre(1, self.zombie_hit, zombie, barrera)

    def zombie_hit(self, zombie, barrera):
        barrera.vida -= self.pilas.azar(3, 10)
        barrera.barra_vida_barrera.progreso = barrera.vida

        if barrera.vida <= 0:
            self.pilas.escenas.EscenaGameOver(self.contador_muertes)

    def spawn(self):
        tiempo_spawn = self.pilas.azar(1, 3)
        self.pilas.tareas.una_vez(tiempo_spawn, self.spawn_zombie)

    def spawn_zombie(self):
        z = self.pilas.actores.Zombie()
        self.zombie_spawn.spawn(z)
        self.enemigos.agregar(z)

    def auto_ataque(self, balitas, barrera):
        balitas.eliminar()
        barrera.vida -= 1
        barrera.barra_vida_barrera.progreso = barrera.vida


# Escena Game Over
class EscenaGameOver(pilasengine.escenas.Escena):

    def iniciar(self, contador_muertes):
        self.contador_final = contador_muertes
        self.fondo = self.pilas.fondos.Blanco()
        self.titulo_game_over()
        self.calavera()
        self.contador_zombies_txt()
        self.contador_zombies(self.contador_final)
        self.inicio_escena()
        self.pilas.tareas.una_vez(5, self.fin_escena)

    def titulo_game_over(self):
        self.titulo = self.pilas.actores.Actor()
        self.titulo.imagen = self.pilas.imagenes.cargar('src/img/titulo_game_over.png')
        self.titulo.escala = 1
        self.titulo.y = 50
        self.titulo.x = 10
        self.titulo.transparencia = 100

    def calavera(self):
        self.calavera = self.pilas.actores.Actor()
        self.calavera.imagen = self.pilas.imagenes.cargar('src/img/calavera_fondo.png')
        self.calavera.escala = 0.85
        self.calavera.x = -7
        self.calavera.z = 1
        self.calavera.transparencia = 100

    def contador_zombies_txt(self):
        self.contador_txt = self.pilas.actores.Texto("Zombies eliminados:")
        self.contador_txt.y = -25
        self.contador_txt.color = self.pilas.colores.Color(241, 0, 0, 0)
        self.contador_txt.escala = 1.50
        self.contador_txt.transparencia = 100

    def contador_zombies(self, contador):
        self.contador = self.pilas.actores.Texto(str(contador))
        self.contador.y = -100
        self.contador.color = self.pilas.colores.Color(0, 212, 0, 0)
        self.contador.escala = 2
        self.contador.transparencia = 100

    def boton_retry(self):
        self.boton_retry = self.pilas.actores.Boton()
        self.boton_retry.imagen = self.pilas.imagenes.cargar('src/img/boton_retry.png')
        self.boton_retry.escala = 0.25
        self.boton_retry.conectar_presionado(self.retry)
        self.boton_retry.transparencia = 100
        self.boton_retry.transparencia = [0], 3

    def retry(self):
        self.pilas.escenas.EscenaJuego()

    def inicio_escena(self):
        self.titulo.transparencia = [0], 3
        self.calavera.transparencia = [0], 3
        self.contador_txt.transparencia = [0], 3
        self.contador.transparencia = [0], 3

    def fin_escena(self):
        self.titulo.transparencia = [100], 3
        self.calavera.transparencia = [100], 3
        self.contador_txt.transparencia = [100], 3
        self.contador.transparencia = [100], 3
        self.boton_retry()
