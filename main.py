from factory.data_factory import DataFactory
from utils import Utils
from model.radar_instance import RadarInstance
from solver import Solver
from time import time
from evaluator import Evaluator
from solver_sem_regiao import Solver_Sem_Regiao
def main():

    NUM_POINTS = 10000
    SIZE_MAP = (100000, 100000)
    NUM_RADAR = 100
    RAIO_RADAR = 15

    evaluator = Evaluator()
    factory = DataFactory()
    solver = Solver()
    solver_sem_regiao = Solver_Sem_Regiao()
    utilidades = Utils()
    points = factory.generate_terrain(num_points=NUM_POINTS, size_map=SIZE_MAP, num_clusters=3)
    radar_instance = RadarInstance(points=points, raio_radar=RAIO_RADAR)

    print("===== Aplicando Heurística ======")
    #radares_finais = solver.heuristica_regional(points=points, num_radares=NUM_RADAR, size_map=SIZE_MAP, raio_radar=RAIO_RADAR)
    
    print("===== Calculando Area ======")
    #area = utilidades.calcular_area_total_aproximada(radares_finais, 10)
    #print(f"Área total coberta: {area}")
    
    utilidades.show_points_on_map(points)
    
    resultados = {
            'regional': {'tempos': [], 'avaliacoes': []},
            'gulosa': {'tempos': [], 'avaliacoes': []}
        }
        
    
    print("=========== COMPARANDO ==========")
    
    
    start_time = time()
    radares_regional = solver.heuristica_regional(points=points, num_radares=NUM_RADAR, size_map=SIZE_MAP, raio_radar=RAIO_RADAR)
    tempo_regional = time() - start_time
    print("AVALIANDNDO")
    avaliacao_regional = evaluator.avaliar_solucao(radares_regional, points, raio_radar=RAIO_RADAR)
    resultados['regional']['tempos'].append("{:.2f}".format(tempo_regional))
    resultados['regional']['avaliacoes'].append(avaliacao_regional)
    
    print("========== GULOSA ============")
    
    # Gulosa sem região
    start_time = time()
    radares_guloso = solver_sem_regiao.heuristica_gulosa(points=points, num_radares=NUM_RADAR, raio_radar=RAIO_RADAR)
    tempo_guloso = time() - start_time
    
    avaliacao_gulosa = evaluator.avaliar_solucao(radares_guloso, points, raio_radar=RAIO_RADAR)
    resultados['gulosa']['tempos'].append("{:.2f}".format(tempo_guloso))
    resultados['gulosa']['avaliacoes'].append(avaliacao_gulosa)

    print(resultados)
    

    #print("==== PLOTTING POINTS ====")
    #utilities.show_points_on_map(points)
    # for point in points:
    #     print(point.x, point.y, point.terrain_type)




if __name__ == "__main__":
    main()
