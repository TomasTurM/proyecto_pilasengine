# Importo Pilas Engine
import pilasengine

# Inicializo Pilas Engine
pilas = pilasengine.iniciar()

# Bala    
class Balitas(pilasengine.actores.Actor):
    def iniciar(self):
        # Propiedades de Bala
        self.radio_de_colision = 5
        self.figura_balita = self.pilas.fisica.Circulo(0, 0, 5, dinamica=False, sensor=False)
        self.imagen = pilas.imagenes.cargar('src/img/bullet_v2.png')
        self.espejado = True
        
        # Habilidades de Bala
        self.aprender('eliminarsesisaledepantalla') 
        
    def actualizar(self):
        self.figura_balita.x = self.x
        self.figura_balita.y = self.y
        
        
pilas.actores.vincular(Balitas)

# Personaje
class Personaje(pilasengine.actores.Actor):
     
    def iniciar(self):

        # Controles
        teclas = {
        pilas.simbolos.a: 'izquierda',
        pilas.simbolos.d: 'derecha',
        pilas.simbolos.c: 'click',
        }
        
        # Definimos el control del Personajeq
        mi_control = pilas.control.Control(teclas)
        
        # Propiedades del Personaje
        self.y = -210
        self.x = 0
        self.rotacion = 90
        self.radio_de_colision = 25
        self.imagen = pilas.imagenes.cargar('src/img/img_soldier.png')
        self.escala = 0.25
        figura_personaje = pilas.fisica.Circulo(0, 0, 25, dinamica=False, sensor=False)
        self.figura_de_colision = figura_personaje
        
        # Habilidades del Personaje
        self.aprender('dispararconclick', municion='Balitas', angulo_salida_disparo=self.rotacion, frecuencia_de_disparo = 7, control = mi_control, distancia=57)
        self.aprender('moverseconelteclado', control = mi_control)
        self.aprender('rotarconmouse')
    
    def eliminar(self):
        self.eliminar()
    
pilas.actores.vincular(Personaje)

# Mira
class Mira(pilasengine.actores.Actor):
   
    def iniciar(self):
        
        self.imagen = pilas.imagenes.cargar('src/img/mira.png')
        self.escala = 0.12
        self.z = -3
        self.aprender('seguiralmouse')
        

pilas.actores.vincular(Mira)


# Habilidad - Movimiento de Zombie con Parametros - 
class MovimientoZombie (pilasengine.habilidades.Habilidad):
    
    def iniciar(self, receptor, velocidad):
        self.receptor = receptor
        self.velocidad = velocidad
        pilas.tareas.siempre(0, self.mover_izq)
                
    def mover_izq(self):
        self.receptor.figura.x -= self.velocidad
        

pilas.habilidades.vincular(MovimientoZombie)
    
# NPC (Zombies)
class Zombie(pilasengine.actores.Actor):
    
    def iniciar(self):

        self.vida = 100
        self.resistencia = 0
        self.x = 250
        self.y = 100
        self.imagen = pilas.imagenes.cargar('src/img/zombie.png')
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
        
    def sangre(self, x, y):
        self.sangre = pilas.actores.Actor()
        self.sangre.imagen = pilas.imagenes.cargar('src/img/blood.png')
        self.sangre.escala = 0.25
        self.sangre.x = x
        self.sangre.y = y
        pilas.tareas.una_vez(2, self.sangre.eliminar)
            
    def actualizar(self):
        self.barra_vida.x = self.x
        self.barra_vida.y = self.y + 30
        self.x = self.figura.x
        self.y = self.figura.y
        
        
pilas.actores.vincular(Zombie)


class ZombieSpawn (pilasengine.actores.actor_invisible.ActorInvisible):
    
    def iniciar(self):
        self.x = 400
        self.y = 0
        
    def spawn(self, z):
     
        z.figura.x = 400
        z.figura.y = pilas.azar(-140,180) 
        z.resistencia = pilas.azar(0,60)
                
        velocidad = pilas.azar(2,5)    
        z.aprender("MovimientoZombie", velocidad)
        
        
pilas.actores.vincular(ZombieSpawn)


# Barrera
class Barrera(pilasengine.actores.Actor):
    
    def iniciar(self):
    
        self.x = -250
        self.y = 0
        self.vida = 100   
        colisiones_barrera = pilas.fisica.Rectangulo(0, 0, 100, 500, sensor=False, dinamica=False) 
        self.figura_de_colision = colisiones_barrera
        self.imagen = pilas.imagenes.cargar('src/img/barrier.jpg')
        
        self.barra_vida_barrera = self.pilas.actores.Energia()
        self.barra_vida_barrera.escala = 1
        self.barra_vida_barrera.x = 0
        self.barra_vida_barrera.y = 200
        

pilas.actores.vincular(Barrera)

# Pared Invisible Superior
class ParedSup(pilasengine.actores.actor_invisible.ActorInvisible):
    
    def iniciar(self):
        self.x = 60
        self.y = 200
        colision_sup = pilas.fisica.Rectangulo(0, 0, 525, 10, sensor=False, dinamica=False)
        self.figura_de_colision = colision_sup
        
        
pilas.actores.vincular(ParedSup)

# Pared Invisible Inferior
class ParedInf(pilasengine.actores.Actor):
    
    def iniciar(self):
        self.x = 60
        self.y = -150
        colision_inf = pilas.fisica.Rectangulo(0, 0, 525, 10, sensor=False, dinamica=False)
        self.figura_de_colision = colision_inf
        self.imagen = pilas.imagenes.cargar('src/img/cerco_inf.png')
        self.escala = 0.1
        
        
pilas.actores.vincular(ParedInf)

# Escena de menu principal
class EscenaMenu(pilasengine.escenas.Escena):
    
    def iniciar(self): 
        fondo = self.pilas.fondos.Fondo()
        fondo.imagen = pilas.imagenes.cargar('src/img/zombie-background.jpg')
        fondo.escala = 0.45
        self.titulo_menu()
        self.boton_iniciar = pilas.actores.Boton()
        self.boton_iniciar.imagen = pilas.imagenes.cargar('src/img/boton_iniciar.png')
        self.boton_iniciar.conectar_presionado(self.translacion_controles)
        self.boton_iniciar.escala = 0.85
        self.boton_iniciar.x = 0
        self.boton_iniciar.y = -60
        self.boton_iniciar.transparencia = 100
        pilas.tareas.agregar(8, self.aparece_boton) 
       
    def titulo_menu(self):
        self.titulo = self.pilas.actores.Actor()
        self.titulo.imagen = pilas.imagenes.cargar('src/img/titulo_menu.png')
        self.titulo.escala = 0.85
        self.titulo.y = 300
        self.titulo.y = [75], 8
        
    def translacion_controles(self):
        self.titulo.transparencia = [100], 3
        self.boton_iniciar.transparencia = [100], 3
        pilas.tareas.agregar(4, self.start)
        
    def start(self):
        self.pilas.escenas.EscenaControles()
        
    def aparece_boton(self):
        self.boton_iniciar.transparencia = [0], 3
        
        
pilas.escenas.vincular(EscenaMenu)

# Escena de controles
class EscenaControles(pilasengine.escenas.Escena):
    def iniciar(self):
        fondo = self.pilas.fondos.Fondo()
        fondo.imagen = pilas.imagenes.cargar('src/img/weapons_room_background.png')
        fondo.escala = 2
        self.titulo_controles()
        self.imagen_controles()
        self.boton_ready()        
        self.inicio_escena()
    
    def titulo_controles(self):
        self.titulo = self.pilas.actores.Actor()
        self.titulo.imagen = pilas.imagenes.cargar('src/img/controles.png')
        self.titulo.escala = 0.85
        self.titulo.y = 185
        self.titulo.transparencia = 100
        
    def imagen_controles(self):
        self.imagen_controles = self.pilas.actores.Actor()
        self.imagen_controles.imagen = pilas.imagenes.cargar('src/img/imagen_controles.png')
        self.imagen_controles.escala = 0.65
        self.imagen_controles.y = 25
        self.imagen_controles.transparencia = 100 
        
    def boton_ready(self):
        self.btn_ready = self.pilas.actores.Boton()
        self.btn_ready.imagen = pilas.imagenes.cargar('src/img/btn_ready.png')
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
        pilas.tareas.agregar(3, self.ready)
        
    def ready(self):
        self.pilas.escenas.EscenaJuego()
        
        
pilas.escenas.vincular(EscenaControles)
            
# Escena de juego            
class EscenaJuego(pilasengine.escenas.Escena):
    
    def iniciar(self):
        fondo = self.pilas.fondos.Fondo()
        fondo.imagen = pilas.imagenes.cargar('src/img/fondo_suelo.jpg')
        fondo.escala = 1.60
        
        pilas.fisica.eliminar_paredes()
        
        self.contador_muertes = 0
        
        # Invocacion Spawn
        self.zombie_spawn = pilas.actores.ZombieSpawn()
        
        # Invocacion de Personaje
        self.personaje = pilas.actores.Personaje()
        
        # Invocacion de Barrera
        self.barrera = pilas.actores.Barrera()
        
        self.pared_sup = pilas.actores.ParedSup()
        
        self.pared_inf = pilas.actores.ParedInf()
        
        # Invocacion de mira
        self.mira = pilas.actores.Mira()
        
        # Grupo de Enemigos
        self.enemigos = pilas.actores.Grupo()
        
        pilas.colisiones.agregar("balitas", "zombie", self.hit_zombie)
        
        pilas.colisiones.agregar("balitas", "barrera", self.auto_ataque)
        
        pilas.colisiones.agregar("zombie", "barrera", self.zombie_hit_tarea)
        
        # Spawn
        pilas.tareas.siempre(1, self.spawn)  
        
    def hit_zombie(self, balitas, zombie):
        balitas.eliminar()
        zombie.vida -= 75 - zombie.resistencia
        zombie.barra_vida.progreso = zombie.vida
            
        if zombie.vida <= 0:
            zombie.barra_vida.eliminar()
            
            if zombie.hit != None:
                zombie.terminar_hit()   
                            
            zombie.sangre(zombie.x, zombie.y)           
            zombie.eliminar()
            self.contador_muertes = self.contador_muertes + 1
             
            
    def zombie_hit_tarea(self, zombie, barrera):
        zombie.hit = pilas.tareas.siempre(1, self.zombie_hit, zombie, barrera)
            
    def zombie_hit(self, zombie, barrera):
        barrera.vida -= pilas.azar(3, 10)
        barrera.barra_vida_barrera.progreso = barrera.vida   
            
        if barrera.vida <= 0:
            pilas.escenas.EscenaGameOver(self.contador_muertes)
        
    def spawn(self):
        tiempo_spawn = pilas.azar(1,3)
        pilas.tareas.una_vez(tiempo_spawn, self.spawn_zombie)
        
    def spawn_zombie(self):
        z = pilas.actores.Zombie()
        self.zombie_spawn.spawn(z)
        self.enemigos.agregar(z)
        
    def auto_ataque(self, balitas, barrera):
        balitas.eliminar()
        barrera.vida -= 1
        barrera.barra_vida_barrera.progreso = barrera.vida
                
               
pilas.escenas.vincular(EscenaJuego)

# Escena Game Over
class EscenaGameOver(pilasengine.escenas.Escena):
    
    def iniciar(self, contador_muertes):
        self.contador_final = contador_muertes
        fondo = pilas.fondos.Blanco()
        self.titulo_game_over()
        self.calavera()
        self.contador_zombies_txt()
        self.contador_zombies(self.contador_final)
        self.inicio_escena()
        pilas.tareas.una_vez(5, self.fin_escena)
        
    def titulo_game_over(self):
        self.titulo = pilas.actores.Actor()
        self.titulo.imagen = pilas.imagenes.cargar('src/img/titulo_game_over.png')
        self.titulo.escala = 1
        self.titulo.y = 50
        self.titulo.transparencia = 100
        
    def calavera(self):
        self.calavera = pilas.actores.Actor()
        self.calavera.imagen = pilas.imagenes.cargar('src/img/calavera_fondo.png')
        self.calavera.escala = 0.85
        self.calavera.x = -7
        self.calavera.z = 1
        self.calavera.transparencia = 100
                           
    def contador_zombies_txt(self):
        self.contador_txt = pilas.actores.Texto("Zombies eliminados:")
        self.contador_txt.y = -25
        self.contador_txt.color = pilas.colores.Color(241, 0, 0, 0)
        self.contador_txt.escala = 1.50
        self.contador_txt.transparencia = 100
        
    def contador_zombies(self, contador):
        self.contador = pilas.actores.Texto(str(contador))
        self.contador.y = -100
        self.contador.color = pilas.colores.Color(0, 212, 0, 0)
        self.contador.escala = 2
        self.contador.transparencia = 100
        
    def boton_retry(self):
        self.boton_retry = self.pilas.actores.Boton()
        self.boton_retry.imagen = pilas.imagenes.cargar('src/img/boton_retry.png')
        self.boton_retry.escala = 1
        self.boton_retry.conectar_presionado(self.retry)
        self.boton_retry.transparencia = 100
        self.boton_retry.transparencia = [0], 3
        
    def retry(self):
        pilas.escenas.EscenaJuego()
    
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
        
        
pilas.escenas.vincular(EscenaGameOver)
                                                   
pilas.escenas.EscenaMenu()