import matplotlib.pyplot as plt
from typing import List
from model.point import Point

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
