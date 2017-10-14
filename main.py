# Importo Pilas Engine
import pilasengine

# Inicializo Pilas Engine
pilas = pilasengine.iniciar()

# Bala    
class bala(pilasengine.actores.Actor):
    def iniciar(self):
        # Propiedades de Bala
        self.radio_de_colision = 5
        self.imagen = pilas.imagenes.cargar('src/img/personaje.png')
        
        # Habilidades de Bala
        self.aprender('eliminarsesisaledepantalla')
        
        
pilas.actores.vincular(bala)

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
        self.aprender('dispararconclick', municion='bala', angulo_salida_disparo=self.rotacion, frecuencia_de_disparo = 50, control = mi_control)
        self.aprender('moverseconelteclado', control = mi_control)
        self.aprender('rotarconmouse')
        self.aprender('limitadoabordesdepantalla')
        self.aprender('puedeexplotar')
    
    def eliminar(self):
        self.eliminar()
    
    def respawn(self):
        self.x = 0
        self.y = 0
    
    def actualizar(self):
        pass

		    
pilas.actores.vincular(personaje)

personaje = pilas.actores.personaje()








# Practicando Pilas (No son parte del proyecto)
#mono = pilas.actores.Mono()
#mono.x = [220]
#mono.y = [220]
#bomba = pilas.actores.Bomba()
#bomba.explotar()
#mono.aprender(pilas.habilidades.RotarConMouse, lado_seguimiento='ABAJO')