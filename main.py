# Importo Pilas Engine
import pilasengine

# Inicializo Pilas Engine
pilas = pilasengine.iniciar()

# Bala    
class balitas(pilasengine.actores.Actor):
    def iniciar(self):
        # Propiedades de Bala
        self.radio_de_colision = 5
        self.imagen = pilas.imagenes.cargar('src/img/personaje.png')
        
        # Habilidades de Bala
        self.aprender('eliminarsesisaledepantalla')    
        self.aprender('puedeexplotar')
       
    def eliminar(self):
        self.eliminar()
        
        
pilas.actores.vincular(balitas)

# Personaje
class personaje(pilasengine.actores.Actor):
     
    def iniciar(self):

        # Controles
        teclas = {
        pilas.simbolos.a: 'izquierda',
        pilas.simbolos.d: 'derecha',
        #pilas.simbolos.w: 'arriba',
        #pilas.simbolos.s: 'abajo',
        pilas.simbolos.c: 'click',
        }
        
        # Definimos el control del Personaje
        mi_control = pilas.control.Control(teclas)
        
        # Propiedades del Personaje
        self.y = -185
        self.x = 0
        self.rotacion = 90
        self.radio_de_colision = 25
        self.imagen = pilas.imagenes.cargar('src/img/personaje.png')
        self.espejado = True
        
        # Habilidades del Personaje
        self.aprender('dispararconclick', municion='balitas', angulo_salida_disparo=self.rotacion, frecuencia_de_disparo = 10, control = mi_control)
        self.aprender('moverseconelteclado', control = mi_control)
        self.aprender('rotarconmouse')
        self.aprender('limitadoabordesdepantalla')
    
    def eliminar(self):
        self.eliminar()
    
    #def respawn(self):
        #self.x = 0
        #self.y = 0
    
    def actualizar(self):
        pass
    
pilas.actores.vincular(personaje)


# Habilidad - Movimiento de Zombie con Parametros - 
class movimiento_zombie (pilasengine.habilidades.Habilidad):
    
    def iniciar(self, receptor, velocidad):
        self.receptor = receptor
        self.velocidad = velocidad
        pilas.tareas.siempre(0, self.mover_izq)
        #pilas.utils.interpolar(self.receptor.figura, 'x', -500, duracion=self.velocidad)  
                
    def mover_izq(self):
        self.receptor.figura.x -= 5
        

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
        self.figura = self.pilas.fisica.Circulo(0, 0, 25, dinamica=False)
        self.radio_de_colision = 25
        
        # Barra de vida
        self.barra_vida = self.pilas.actores.Energia()
        self.barra_vida.escala = 0.5
        
        # Hablilidades Zombie
        self.aprender('puedeexplotar')
    
    def eliminar(self):
        self.eliminar()
        self.figura.eliminar()
        
        
    #Seguir Jugador
    #def seguir_jugador(self):
    #   self.x = [self.actor.x],5
    #   self.y = [self.actor.y],5   
            
    def actualizar(self):
        self.barra_vida.x = self.x
        self.barra_vida.y = self.y + 50
        self.x = self.figura.x
        self.y = self.figura.y
        
        
pilas.actores.vincular(zombie)


class zombie_spawn (pilasengine.actores.actor_invisible.ActorInvisible):
    
    def iniciar(self):
        self.x = 0    
        self.y = 0
        
    def spawn(self, z):
     
        z.figura.x = 400
        z.figura.y = pilas.azar(-100,200) 
        z.resistencia = pilas.azar(0,75)
                
        velocidad = pilas.azar(7,15)    
        z.aprender("movimiento_zombie", velocidad)
        
        
pilas.actores.vincular(zombie_spawn)


# Barrera
class barrera (pilasengine.actores.Actor):
    
    def iniciar(self):
    
        self.x = -275
        self.y = 35
        self.vida = 100   
        colisiones_barrera = pilas.fisica.Rectangulo(0, 0, 60, 350, sensor=False, dinamica=False) 
        self.figura_de_colision = colisiones_barrera
        
        self.barra_vida_barrera = self.pilas.actores.Energia()
        self.barra_vida_barrera.escala = 1
        self.barra_vida_barrera.x = 0
        self.barra_vida_barrera.y = 200
        
    def actualizar(self):
        if self.figura_de_colision.figuras_en_contacto:
            self.vida -= 1
        

pilas.actores.vincular(barrera)


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
        fondo.escala = 1.85
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
        pilas.fisica.eliminar_paredes()
        
        # Invocacion Spawn
        self.zombie_spawn = pilas.actores.zombie_spawn()
        
        # Invocacion de Personaje
        self.personaje = pilas.actores.personaje()
        
        # Invocacion de Barrera
        self.barrera = pilas.actores.barrera()
        
        # Grupo de Enemigos
        self.enemigos = pilas.actores.Grupo()
        
        pilas.colisiones.agregar("balitas", "zombie", self.hit_zombie)
        
        pilas.colisiones.agregar("balitas", "zombie_atacando", self.hit_zombie)
        
        pilas.colisiones.agregar("zombie", "barrera", self.atacar_barrera)
        
        pilas.colisiones.agregar("balitas", "barrera", self.auto_ataque)
        
        # Spawn
        pilas.tareas.siempre(2, self.spawn)
        
        
    def hit_zombie(self, balitas, zombie):
        balitas.eliminar()
        zombie.vida -= 100 - zombie.resistencia
        zombie.barra_vida.progreso = zombie.vida
            
        if zombie.vida <= 0:
            zombie.barra_vida.eliminar()
            zombie.eliminar()
        
    def spawn(self):
                
        z = pilas.actores.zombie()
        self.zombie_spawn.spawn(z)
        self.enemigos.agregar(z)
        
    def atacar_barrera(self, zombie, barrera):
        pass
        
    def auto_ataque(self, balitas, barrera):
        balitas.eliminar()
        barrera.vida -= 1
        barrera.barra_vida_barrera.progreso = barrera.vida
        

            
        # Hay un error: Se crean multiples zombie_atacando
        
        #if barrera.vida <= 0:
            # Game Over
        #else:
        #    pass
                
               
pilas.escenas.vincular(escena_juego)

# Escena Game Over
class escena_game_over(pilasengine.escenas.Escena):
    
    def iniciar(self):
        fondo = pilas.fondos.Espacio()
        self.titulo_game_over()
        self.calavera()
        self.contador_zombies()
        self.inicio_escena()
        
    def titulo_game_over(self):
        self.titulo = pilas.actores.Actor()
        #self.titulo.imagen = pilas.imagenes.cargar('src/img/')
        #self.titulo.escala = 1
        self.titulo.y = 100
        self.titulo.transparencia = 100
        
    def calavera(self):
        self.calavera = pilas.actores.Actor()
        #self.calavera.imagen = pilas.imagenes.cargar('src/img/')
        #self.calavera.escala = 1
        self.calavera.z = 1
        self.calavera.transparencia = 100
                           
    def contador_zombies_txt(self):
        self.contador_txt = pilas.actores.Texto("Zombies muertos:")
        self.contador_txt.y = -25
        self.contador_txt.color = pilas.colores.Color(241, 0, 0, 0)
        self.contador_txt.transparencia = 100
        
    def contador_zombies(self, contador):
        self.contador = pilas.actores.Texto(contador)
        self.contador.y = -35
        self.contador.color = pilas.colores.Color(0, 212, 0, 0)
        self.contador.transparencia = 100
    
    def incio_escena(self):
        self.titulo.transparencia = [0], 3
        self.calavera.transparencia = [0], 3
        self.contador_txt.transparencia = [0], 3
        self.contador.transparencia = [0], 3
        
pilas.escenas.vincular(escena_game_over)
                
                        
                                         
pilas.escenas.escena_menu()








# Practicando Pilas (No son parte del proyecto)
#mono = pilas.actores.Mono()
#mono.x = [220]
#mono.y = [220]
#bomba = pilas.actores.Bomba()
#bomba.explotar()
#mono.aprender(pilas.habilidades.RotarConMouse, lado_seguimiento='ABAJO')