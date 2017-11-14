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
        pilas.simbolos.w: 'arriba',
        pilas.simbolos.s: 'abajo',
        pilas.simbolos.c: 'click',
        }
        
        # Definimos el control del Personaje
        mi_control = pilas.control.Control(teclas)
        
        # Propiedades del Personaje
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

# NPC (Zombies)
class zombie(pilasengine.actores.Actor):
    
    def iniciar(self):

        self.x = 250
        self.y = 100
        self.radio_de_colision = 25
        #self.imagen = pilasengine.actores.actor.Actor.obtener_imagen(pilasengine.actores.Aceituna())
        
        # Hablilidades Zombie
        self.aprender('puedeexplotar')
     
 
    def actualizar(self):
        pass
    
    def eliminar(self):
        self.eliminar()
        
    #Seguir Jugador
    def seguir_jugador(self, personaje):
       self.x = [personaje.x],5
       self.y = [personaje.y],5   
        
        
pilas.actores.vincular(zombie)


class zombie_spawn (pilasengine.actores.actor_invisible.ActorInvisible):
    
    def iniciar(self):
        self.x = 200
        self.y = 200
        
    def spawn(self, z):
        
        enemigos = pilas.actores.Grupo()
        enemigos.agregar(z)
     
        z.x = pilas.azar(-200, 200)
        z.y = pilas.azar(-200, 200) 
        
        
pilas.actores.vincular(zombie_spawn)

            
class escena_juego(pilasengine.escenas.Escena):
    
    def iniciar(self):
        # Invocacion Spawn
        self.zombie_spawn = pilas.actores.zombie_spawn()
        
        # Invocacion de Personaje
        self.personaje = pilas.actores.personaje()

        # Invocacion de Zombie
        self.zombie = pilas.actores.zombie()
        
        pilas.colisiones.agregar("balitas", "zombie", self.hit_zombie)
        
        # Spawn
        pilas.tareas.siempre(2, self.spawnYseguir)
        
        
    def hit_zombie(self, zombie, balitas):
        
        balitas.eliminar()
        zombie.eliminar() 
        
    def spawnYseguir (self):
        
        z = pilas.actores.zombie()
        self.zombie_spawn.spawn(z)
        pilas.tareas.siempre(0, z.seguir_jugador(self.personaje))
        
        
        
     
               
pilas.escenas.vincular(escena_juego)
           
pilas.escenas.escena_juego()








# Practicando Pilas (No son parte del proyecto)
#mono = pilas.actores.Mono()
#mono.x = [220]
#mono.y = [220]
#bomba = pilas.actores.Bomba()
#bomba.explotar()
#mono.aprender(pilas.habilidades.RotarConMouse, lado_seguimiento='ABAJO')