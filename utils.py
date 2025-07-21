import matplotlib.pyplot as plt
import matplotlib
from typing import List
from model.point import Point
import numpy as np
import math
matplotlib.use('Agg')  
'''
    Classe de utilidades.
'''
class Utils:
    '''
        Mostra os pontos presentes em um mapa. O mapa em 'si' não é necessário já que cada Point possui suas coordenadas X e Y.
    '''
    def show_points_on_map(self, points:List[Point]):
        fig, ax = plt.subplots(1,1, figsize=(10,10))
        
        colors = {0:'red', 1:'blue', 2:'green'}
        label = {0: 'Ruim', 1: 'Aceitável', 2: 'Bom'}

        for terrain_type in [0, 1, 2]:
            terrain_points = [p for p in points if p.terrain_type == terrain_type]
            if terrain_points:
                x_coords = [p.x for p in terrain_points]
                y_coords = [p.y for p in terrain_points]
                ax.scatter(x_coords, y_coords, c=colors[terrain_type], 
                          label=label[terrain_type], alpha=0.7, s=50)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title("Points")
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.savefig('points.png')

    def calcular_area_total_aproximada(self, radares, raio_radar) :

        '''
            Dado a lista de radares posicionados, é calculado a área (aproximada) de cobertura.
            PS: Sem medida. Não sei se consideramos metros ou KM (?)
        '''

        if not radares:
            return 0.0
        
        x_min = min(r.x - raio_radar for r in radares)
        x_max = max(r.x + raio_radar for r in radares)
        y_min = min(r.y - raio_radar for r in radares) # Calculando limite dos eixos X e Y
        y_max = max(r.y + raio_radar for r in radares)
        
        x_points = np.arange(x_min, x_max)
        y_points = np.arange(y_min, y_max)
        
        area_coberta = 0.0

        for x in x_points:
            for y in y_points:
            
                for radar in radares:
                    distancia = math.sqrt((x - radar.x)**2 + (y - radar.y)**2)
                    if distancia <= raio_radar:
                        area_coberta += 1 
                        break  
        
        return area_coberta