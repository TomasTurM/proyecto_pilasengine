# -*- coding: UTF-8 -*-

# Importo Pilas Engine
import pilasengine

from balas import Balitas
from personajes import Personaje, Mira
from npcs import MovimientoZombie, Zombie, ZombieSpawn
from objetos import Barrera, ParedSup, ParedInf
from escenas import EscenaMenu, EscenaControles, EscenaJuego, EscenaGameOver

# Inicializo Pilas Engine
pilas = pilasengine.iniciar()

pilas.actores.vincular(Balitas)

pilas.actores.vincular(Personaje)

pilas.actores.vincular(Mira)

pilas.habilidades.vincular(MovimientoZombie)

pilas.actores.vincular(Zombie)

pilas.actores.vincular(ZombieSpawn)

pilas.actores.vincular(Barrera)

pilas.actores.vincular(ParedSup)

pilas.actores.vincular(ParedInf)

pilas.escenas.vincular(EscenaMenu)

pilas.escenas.vincular(EscenaControles)

pilas.escenas.vincular(EscenaJuego)

pilas.escenas.vincular(EscenaGameOver)

pilas.escenas.EscenaJuego()
