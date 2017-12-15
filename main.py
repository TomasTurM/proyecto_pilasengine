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
        
    def actualizar(self):
        self.receptor.x = [-300], self.velocidad
        

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
        self.radio_de_colision = 25
        
        # Barra de vida
        self.barra_vida = self.pilas.actores.Energia()
        self.barra_vida.escala = 0.5
        
        # Hablilidades Zombie
        self.aprender('puedeexplotar')
    
    def eliminar(self):
        self.eliminar()
        
        
    #Seguir Jugador
    #def seguir_jugador(self):
    #   self.x = [self.actor.x],5
    #   self.y = [self.actor.y],5   
            
    def actualizar(self):
        self.barra_vida.x = self.x
        self.barra_vida.y = self.y + 50
        
        
pilas.actores.vincular(zombie)


class zombie_spawn (pilasengine.actores.actor_invisible.ActorInvisible):
    
    def iniciar(self):
        self.x = 0    
        self.y = 0
        
    def spawn(self, z):
     
        z.x = 400
        z.y = pilas.azar(-100,200) 
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
        colisiones_barrera = pilas.fisica.Rectangulo(0, 0, 60, 350, sensor=True, dinamica=False) 
        self.figura_de_colision = colisiones_barrera
        
        self.barra_vida_barrera = self.pilas.actores.Energia()
        self.barra_vida_barrera.escala = 1
        self.barra_vida_barrera.x = 0
        self.barra_vida_barrera.y = 200
        
    def actualizar(self):
        if self.figura_de_colision.figuras_en_contacto:
            self.vida -= 1
        

pilas.actores.vincular(barrera)

            
# Escenario de juego            
class escena_juego(pilasengine.escenas.Escena):
    
    def iniciar(self):
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
        toco = False
        toco_1 = False
        
        if toco == False:
            if toco_1 == False:
                zombie_atacando = pilas.actores.zombie()
                zombie_atacando.x = zombie.x
                zombie_atacando.y = zombie.y
                zombie.eliminar()
                toco_1 = True
            else:
                pass
        else:
            pass
            
        # Hay un error: Se crean multiples zombie_atacando
        
        #if barrera.vida <= 0:
            # Game Over
        #else:
        #    pass
        
     
               
pilas.escenas.vincular(escena_juego)
           
pilas.escenas.escena_juego()








# Practicando Pilas (No son parte del proyecto)
#mono = pilas.actores.Mono()
#mono.x = [220]
#mono.y = [220]
#bomba = pilas.actores.Bomba()
#bomba.explotar()
#mono.aprender(pilas.habilidades.RotarConMouse, lado_seguimiento='ABAJO')