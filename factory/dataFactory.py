import random
import numpy as np
from typing import Tuple
from model.point import Point

class DataFactory:
    seed = random.randint(0,100)

    def __init__(self):
        random.seed(self.seed)
        np.random.seed(self.seed)
    
    def generate_terrain(self, num_points:int, size_map:Tuple[int, int], num_clusters):
        '''
            Função que gera o terreno com base na quantidade de clusters e tamanho do mapa.
            num_points = quantidade de pontos para serem postos no mapa.
            size_map = Tamanho do mapa {EX: (100,100)}
            num_clusters = Número de clusters. 

            Os clusters são utilizados para melhor distribuição dos pontos de acordo com o terreno. 
        '''

        current_points = []

        centers_cluster = {
            0: [(np.random.uniform(0,size_map[0]), np.random.uniform(0,size_map[1]))  
                for _ in range(num_clusters//3 + 1)],
            1: [(np.random.uniform(0,size_map[0]), np.random.uniform(0,size_map[1])) 
                for _ in range(num_clusters//3 + 1)],
            2: [(np.random.uniform(0,size_map[0]), np.random.uniform(0,size_map[1])) 
                for _ in range(num_clusters//3 + 1)]
        }

        for _ in range (num_points):
            #terrain_type = random.randint(0,2)
            terrain_type = np.random.choice([0,1,2], p=[0.25, 0.5, 0.25]) 

            current_point_center = random.choice(centers_cluster[terrain_type])

            angulo = np.random.uniform(0, 2*np.pi)
            raio = np.random.exponential(scale=15)

            x = current_point_center[0] + raio * np.cos(angulo)
            y = current_point_center[1] + raio * np.sin(angulo)
            
            x = np.clip(x, 0,size_map[0]) #Para não cair em um cenário onde um ponto está fora dos limites do map
            y = np.clip(y, 0,size_map[1])
            
            current_points.append(Point(x, y, terrain_type))
        
        return current_points

