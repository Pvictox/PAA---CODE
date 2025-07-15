
'''
Essa classe representa um determinado ponto no plano cartesiano e também qual o terreno associado a ele.
    - Terreno = Variável que vai de 0 a 2, onde 0 indicará que o terreno é elevado e 2 indica que é plano.

Para o nosso problema, iremos considerar que quanto mais plano o terreno, melhor é para se alocar um radar

'''

class Point:
    x: float
    y: float
    terrain_type : int

    def __init__(self, x, y, terrain_type):
        self.x = x
        self.y = y
        self.terrain_type = terrain_type

    def __iter__(self):
        return iter([self.x, self.y, self.terrain_type])


