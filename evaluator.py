from solver import Solver
import numpy as np
from utils import Utils

utilidades = Utils()
solver_com_regioes = Solver()

class Evaluator():
    
    
    def avaliar_solucao(self, radares, todos_pontos, raio_radar):
        #area = utilidades.calcular_area_total_aproximada(radares=radares, raio_radar=raio_radar)
        if not radares:
            return {
                'cobertura_total': 0,
                'cobertura_percentual': 0.0,
                'num_radares': 0,
                'eficiencia': 0.0,
                #'area_coberta': 0.0,
            }
        
        # Cobertura total
        cobertura_total = solver_com_regioes.calcular_cobertura_total(radares, todos_pontos, raio_radar)
        cobertura_percentual = cobertura_total / len(todos_pontos) * 100
        
        
        eficiencia = cobertura_total / len(radares) if radares else 0
        
        return {
            'cobertura_total': cobertura_total,
            'cobertura_percentual': cobertura_percentual,
            'num_radares': len(radares),
            'eficiencia': eficiencia,
            #'area_coberta': area,
        }