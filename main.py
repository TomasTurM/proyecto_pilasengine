# Importo Pilas Engine
import pilasengine

# Inicializo Pilas Engine
pilas = pilasengine.iniciar()

# Bala    
class balitas(pilasengine.actores.Actor):
    def iniciar(self):
        # Propiedades de Bala
        self.radio_de_colision = 5
        self.figura_balita = self.pilas.fisica.Circulo(0, 0, 5, dinamica=False, sensor=False)
        self.imagen = pilas.imagenes.cargar('src/img/bullet_v2.png')
        self.espejado = True
        
        # Habilidades de Bala
        self.aprender('eliminarsesisaledepantalla')    
        self.aprender('puedeexplotar')
       
    def eliminar(self):
        del self.figura_balita
        self.eliminar()
        
    def actualizar(self):
        self.figura_balita.x = self.x
        self.figura_balita.y = self.y
        
        
pilas.actores.vincular(balitas)

# Personaje
class personaje(pilasengine.actores.Actor):
     
    def iniciar(self):

        # Controles
        teclas = {
        pilas.simbolos.a: 'izquierda',
        pilas.simbolos.d: 'derecha',
        pilas.simbolos.c: 'click',
        }
        
        # Definimos el control del Personaje
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
        self.aprender('dispararconclick', municion='balitas', angulo_salida_disparo=self.rotacion, frecuencia_de_disparo = 7, control = mi_control, distancia=57)
        self.aprender('moverseconelteclado', control = mi_control)
        self.aprender('rotarconmouse')
    
    def eliminar(self):
        self.eliminar()
    
    #def respawn(self):
        #self.x = 0
        #self.y = 0
    
pilas.actores.vincular(personaje)

# Mira
class mira(pilasengine.actores.Actor):
   
    def iniciar(self):
        
        self.imagen = pilas.imagenes.cargar('src/img/mira.png')
        self.escala = 0.12
        self.z = -3
        self.aprender('seguiralmouse')
        

pilas.actores.vincular(mira)


# Habilidad - Movimiento de Zombie con Parametros - 
class movimiento_zombie (pilasengine.habilidades.Habilidad):
    
    def iniciar(self, receptor, velocidad):
        self.receptor = receptor
        self.velocidad = velocidad
        pilas.tareas.siempre(0, self.mover_izq)
                
    def mover_izq(self):
        self.receptor.figura.x -= self.velocidad
        

pilas.habilidades.vincular(movimiento_zombie)
    

# Habilidad - Vida de Zombie con Parametros - 
#class vida_zombie (pilasengine.habilidades.Habilidad):
#    
#    def iniciar(self, receptor, vida):
#        self.receptor = receptor
#        self.vida = vida
#        
#    def actualizar(self):
#        self.receptor
        
        
        
        
# Habilidad - Resistencia de Zombie con Parametros - 
#class resistencia_zombie (pilasengine.habilidades.Habilidad):
#    
#    def iniciar(self, receptor, vida):
#        self.receptor = receptor
#        self.resistencia = resistencia
#        
#    def actualizar(self):
#        self.receptor.resistencia = self.resistencia
    

# NPC (Zombies)
class zombie(pilasengine.actores.Actor):
    
    #def __init__(self, actor):
    #    self.actor = actor
    
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
        
        # Hablilidades Zombie
        self.aprender('puedeexplotar')
    
    def eliminar(self):
        self.figura.eliminar()
        self.eliminar()
        
    def terminar_hit(self):
        self.hit.terminar()
            
        
    #Seguir Jugador
    #def seguir_jugador(self):
    #   self.x = [self.actor.x],5
    #   self.y = [self.actor.y],5   
            
    def actualizar(self):
        self.barra_vida.x = self.x
        self.barra_vida.y = self.y + 30
        self.x = self.figura.x
        self.y = self.figura.y
        
        
pilas.actores.vincular(zombie)


class zombie_spawn (pilasengine.actores.actor_invisible.ActorInvisible):
    
    def iniciar(self):
        self.x = 0    
        self.y = 0
        
    def spawn(self, z):
     
        z.figura.x = 400
        z.figura.y = pilas.azar(-140,180) 
        z.resistencia = pilas.azar(0,60)
                
        velocidad = pilas.azar(2,5)    
        z.aprender("movimiento_zombie", velocidad)
        
        
pilas.actores.vincular(zombie_spawn)


# Barrera
class barrera (pilasengine.actores.Actor):
    
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
        

pilas.actores.vincular(barrera)

# Pared Invisible Superior
class pared_sup(pilasengine.actores.actor_invisible.ActorInvisible):
    
    def iniciar(self):
        self.x = 60
        self.y = -150
        colision_sup = pilas.fisica.Rectangulo(0, 0, 525, 10, sensor=False, dinamica=False)
        self.figura_de_colision = colision_sup
        
        
pilas.actores.vincular(pared_sup)

# Pared Invisible Inferior
class pared_inf(pilasengine.actores.Actor):
    
    def iniciar(self):
        self.x = 60
        self.y = -150
        colision_inf = pilas.fisica.Rectangulo(0, 0, 525, 10, sensor=False, dinamica=False)
        self.figura_de_colision = colision_inf
        self.imagen = pilas.imagenes.cargar('src/img/cerco_inf.png')
        self.escala = 0.1
        
        
pilas.actores.vincular(pared_inf)


# Escena de menu principal
class escena_menu(pilasengine.escenas.Escena):
    
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
        self.pilas.escenas.escena_controles()
        
    def aparece_boton(self):
        self.boton_iniciar.transparencia = [0], 3
        
        
pilas.escenas.vincular(escena_menu)

# Escena de controles
class escena_controles(pilasengine.escenas.Escena):
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
        self.pilas.escenas.escena_juego()
        
        
pilas.escenas.vincular(escena_controles)
            
# Escena de juego            
class escena_juego(pilasengine.escenas.Escena):
    
    def iniciar(self):
        fondo = self.pilas.fondos.Fondo()
        fondo.imagen = pilas.imagenes.cargar('src/img/fondo_suelo.jpg')
        fondo.escala = 1.60
        
        pilas.fisica.eliminar_paredes()
        
        self.contador_muertes = 0
        
        # Invocacion Spawn
        self.zombie_spawn = pilas.actores.zombie_spawn()
        
        # Invocacion de Personaje
        self.personaje = pilas.actores.personaje()
        
        # Invocacion de Barrera
        self.barrera = pilas.actores.barrera()
        
        self.pared_sup = pilas.actores.pared_sup()
        
        self.pared_inf = pilas.actores.pared_inf()
        
        # Invocacion de mira
        self.mira = pilas.actores.mira()
        
        # Grupo de Enemigos
        self.enemigos = pilas.actores.Grupo()
        
        pilas.colisiones.agregar("balitas", "zombie", self.hit_zombie)
        
        pilas.colisiones.agregar("balitas", "barrera", self.auto_ataque)
        
        pilas.colisiones.agregar("zombie", "barrera", self.zombie_hit_tarea)
        
        # Spawn
        pilas.tareas.siempre(2, self.spawn)
        
        
    def hit_zombie(self, balitas, zombie):
        balitas.eliminar()
        zombie.vida -= 75 - zombie.resistencia
        zombie.barra_vida.progreso = zombie.vida
            
        if zombie.vida <= 0:
            zombie.barra_vida.eliminar()
            
            if zombie.hit != None:
                zombie.terminar_hit()            
            
            zombie.eliminar()
            self.contador_muertes = self.contador_muertes + 1
            
    def zombie_hit_tarea(self, zombie, barrera):
        zombie.hit = pilas.tareas.siempre(1, self.zombie_hit, zombie, barrera)
            
    def zombie_hit(self, zombie, barrera):
        barrera.vida -= pilas.azar(3, 10)
        barrera.barra_vida_barrera.progreso = barrera.vida   
            
        if barrera.vida <= 0:
            pilas.escenas.escena_game_over(self.contador_muertes)
        
    def spawn(self):
                
        z = pilas.actores.zombie()
        self.zombie_spawn.spawn(z)
        self.enemigos.agregar(z)
        
    def auto_ataque(self, balitas, barrera):
        balitas.eliminar()
        barrera.vida -= 1
        barrera.barra_vida_barrera.progreso = barrera.vida
                
               
pilas.escenas.vincular(escena_juego)

# Escena Game Over
class escena_game_over(pilasengine.escenas.Escena):
    
    def iniciar(self, contador_muertes):
        self.contador_final = contador_muertes
        fondo = pilas.fondos.Blanco()
        self.titulo_game_over()
        self.calavera()
        self.contador_zombies_txt()
        self.contador_zombies(self.contador_final)
        self.inicio_escena()
        
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
    
    def inicio_escena(self):
        self.titulo.transparencia = [0], 3
        self.calavera.transparencia = [0], 3
        self.contador_txt.transparencia = [0], 3
        self.contador.transparencia = [0], 3
        
pilas.escenas.vincular(escena_game_over)
                
                        
                                         
pilas.escenas.escena_menu()
#pilas.escenas.escena_juego()








# Practicando Pilas (No son parte del proyecto)
#mono = pilas.actores.Mono()
#mono.x = [220]
#mono.y = [220]
#bomba = pilas.actores.Bomba()
#bomba.explotar()
#mono.aprender(pilas.habilidades.RotarConMouse, lado_seguimiento='ABAJO')