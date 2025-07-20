import matplotlib.pyplot as plt
import matplotlib
from typing import List
from model.point import Point
import numpy as np
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

    def divide_hibrida(self, points, size_map, raio_radar):
        regioes = {}
    
        
        terrenos = {0: [], 1: [], 2: []}
        for point in points:
            terrenos[point.terrain_type].append(point)
        

        for terrain_type, terrain_points in terrenos.items():
            if not terrain_points:
                continue
            
            divisoes_x = max(1, int(size_map[0] / (2 * raio_radar)))
            divisoes_y = max(1, int(size_map[1] / (2 * raio_radar)))
            
            largura_regiao = size_map[0] / divisoes_x
            altura_regiao = size_map[1] / divisoes_y
            
            for i in range(divisoes_x):
                for j in range(divisoes_y):
                    regiao_id = f"T{terrain_type}_R{i}_{j}"
                    regioes[regiao_id] = []
            
          
            for point in terrain_points:
                i = min(int(point.x // largura_regiao), divisoes_x - 1)
                j = min(int(point.y // altura_regiao), divisoes_y - 1)
                regiao_id = f"T{terrain_type}_R{i}_{j}"
                regioes[regiao_id].append(point)
        
        return regioes