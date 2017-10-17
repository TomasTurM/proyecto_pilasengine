# Importo Pilas Engine
import pilasengine
from math import atan

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
        #self.aprender('seguirclicks')
    
    def actualizar(self):
        pass
        #self.x = self.personaje.x
        #self.y = self.personaje.y
    
    def calc_trayecto(self, x2, y2):
        m1 = y2 - self.y
        m2 = x2 - self.x
        
        return (atan(m1/m2))
        
        
           

pilas.actores.vincular(zombie)





# Invocacion de Personaje
personaje = pilas.actores.personaje()

# Invocacion de Zombie
zombie = pilas.actores.zombie()


print(zombie.calc_trayecto(personaje.x, personaje.y))



# Practicando Pilas (No son parte del proyecto)
#mono = pilas.actores.Mono()
#mono.x = [220]
#mono.y = [220]
#bomba = pilas.actores.Bomba()
#bomba.explotar()
#mono.aprender(pilas.habilidades.RotarConMouse, lado_seguimiento='ABAJO')