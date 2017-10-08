# Importo Pilas Engine
import pilasengine




















# Practicando Pilas (No son parte del proyecto)
pilas = pilasengine.iniciar()
mono = pilas.actores.Mono()
mono.x = [220]
mono.y = [220]
bomba = pilas.actores.Bomba()
bomba.explotar()
mono.aprender(pilas.habilidades.RotarConMouse, lado_seguimiento='ABAJO')