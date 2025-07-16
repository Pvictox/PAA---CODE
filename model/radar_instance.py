from model.point import Point
from typing import List
from scipy.spatial import KDTree
import numpy as np


class RadarInstance:
    def __init__(self, points: List[Point], raio_radar):
        self.points = points
        self.raio_radar = raio_radar
        self.points_numpy = np.array([[p.x, p.y] for p in points])
        self.terrain_numpy = np.array([p.terrain_type for p in points])
        self.tree = KDTree(self.points_numpy)
        
    def get_neighbors(self, point_index, raio):
        if raio:
            neighbors = self.tree.query_ball_point(self.points_numpy[point_index], raio)
            neigborhood = []
            for neighbor in neighbors:
                if neighbor != point_index:
                    neigborhood.append(self.points[neighbor])
            return neigborhood
        else:
            return self.raio_radar*2 #Se não há raio para se buscar então retorna o próprio raio. Isso é importante para evitar sobreposição de raios.
    
    def get_covered_area(self, points_radar:List[int], n_samples=100000):
        if len(points_radar) == 0:
            return 0
        
        radar_positions = self.points_numpy[points_radar]
        
        min_x = radar_positions[:, 0].min() - self.raio_radar
        max_x = radar_positions[:, 0].max() + self.raio_radar
        min_y = radar_positions[:, 1].min() - self.raio_radar
        max_y = radar_positions[:, 1].max() + self.raio_radar
        
        samples = np.random.uniform(
            low=[min_x, min_y], 
            high=[max_x, max_y], 
            size=(n_samples, 2)
        )
        
        covered = np.zeros(n_samples, dtype=bool)
        
        for radar_idx in points_radar:
            radar_pos = self.points_numpy[radar_idx]
            
          
            distances_sq = np.sum((samples - radar_pos)**2, axis=1)
            
          
            covered |= (distances_sq <= self.raio_radar**2) #União de conjuntos in-place
        
        total_area = (max_x - min_x) * (max_y - min_y)
        coverage_ratio = np.sum(covered) / n_samples
        return total_area * coverage_ratio




    