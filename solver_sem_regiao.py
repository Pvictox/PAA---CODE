from utils import Utils
import numpy as np
from solver import Solver

solver_com_regioes = Solver()
utilidades = Utils()


class Solver_Sem_Regiao():
     def heuristica_gulosa(self, points, num_radares, raio_radar):
        radares = []
        pontos_restantes = points.copy()
        
        for _ in range(num_radares):
            if not pontos_restantes:
                break
                
            melhor_posicao = None
            melhor_score = -1
            
            for candidato in pontos_restantes:
                pontos_cobertos = solver_com_regioes.pontos_cobertos_por_radar(
                    candidato, pontos_restantes, raio_radar
                )
                
                cobertura = len(pontos_cobertos)
                qualidade = 2 if candidato.terrain_type == 0 else 1 if candidato.terrain_type == 1 else 0.5
                sobreposicao = solver_com_regioes.calcular_sobreposicao(candidato, radares, raio_radar)
                
                
                score = cobertura * qualidade * (1 - sobreposicao * 0.5)
                
                if score > melhor_score:
                    melhor_score = score
                    melhor_posicao = candidato
            
            if melhor_posicao is None:
                break
                
            radares.append(melhor_posicao)
            
            pontos_cobertos = solver_com_regioes.pontos_cobertos_por_radar(
                melhor_posicao, pontos_restantes, raio_radar
            )
            pontos_restantes = [
                p for p in pontos_restantes 
                if id(p) not in {id(pc) for pc in pontos_cobertos}
            ]
        
        return radares
    

     