from utils import Utils
import numpy as np

utilidades = Utils()


class Solver():


    def dividir_região(self, points, size_map, raio_radar):
        '''
            Dado o tamanho do mapa e seus pontos, faz uma divisão geométrica do mapa em regiões.
        '''
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
                    regiao_id = f"Terreno{terrain_type}|REGIAO{i}_{j}"
                    regioes[regiao_id] = []
            
            
            for point in terrain_points:
                i = min(int(point.x // largura_regiao), divisoes_x - 1)
                j = min(int(point.y // altura_regiao), divisoes_y - 1)
                regiao_id = f"Terreno{terrain_type}|REGIAO{i}_{j}"
                regioes[regiao_id].append(point)
        
        return regioes
    

    def calcular_cobertura_total(self, radares, todos_pontos, raio_radar):
       
        pontos_cobertos_total = set()
        
        for radar in radares:
            pontos_cobertos = self.pontos_cobertos_por_radar(radar, todos_pontos, raio_radar)
          
            pontos_cobertos_total.update(id(p) for p in pontos_cobertos)
        
        return len(pontos_cobertos_total)


    def calcular_potencial_cobertura(self,pontos_regiao, raio_radar):
        """
        Calcula o potencial de cobertura da região. Para cada ponto é calculado o quanto esse ponto pode cobrir se um radar for alocado alí.
        """
        if not pontos_regiao:
            return 0
        
        # Número máximo de pontos que podem ser cobertos por um radar
        max_cobertura = 0
        for ponto in pontos_regiao:
            cobertura = len(self.pontos_cobertos_por_radar(ponto, pontos_regiao, raio_radar))
            max_cobertura = max(max_cobertura, cobertura)
        
        return max_cobertura / len(pontos_regiao)

    def calcular_centralidade(self, pontos_regiao):
        """
            Ter a centralidade do conjunto de pontos auxilia no calculo da sobreposição 
            TODO: Verificar sem calculo.
        """
        if not pontos_regiao:
            return 0
        
        
        centro_x = sum(p.x for p in pontos_regiao) / len(pontos_regiao)
        centro_y = sum(p.y for p in pontos_regiao) / len(pontos_regiao)
        
        
        dist_media = sum(
            np.sqrt((p.x - centro_x)**2 + (p.y - centro_y)**2) 
            for p in pontos_regiao
        ) / len(pontos_regiao)
        
        return 1 / (1 + dist_media)  

    def calcular_sobreposicao(self, posicao_candidata, radares_existentes, raio_radar):
        """
        Calcula a sobreposição com radares já posicionados
        PS: Calculo aproximado
        """
        if not radares_existentes:
            return 0
        
        sobreposicao_total = 0
        for radar_existente in radares_existentes:
            distancia = np.sqrt(
                (posicao_candidata.x - radar_existente.x)**2 + 
                (posicao_candidata.y - radar_existente.y)**2
            )
            
            if distancia < 2 * raio_radar:
                
                if distancia <= raio_radar:
                
                    sobreposicao_total += 1.0
                else:
                
                    sobreposicao_total += (2 * raio_radar - distancia) / raio_radar
        
        return min(sobreposicao_total, 1.0)  # Normaliza entre 0 e 1
    
    def pontos_cobertos_por_radar(self, posicao_radar, pontos_candidatos, raio_radar):
        """
        Retorna todos os pontos que estão dentro do raio de cobertura de um radar.
        """
        pontos_cobertos = []
        
        for ponto in pontos_candidatos:
            distancia = np.sqrt(
                (posicao_radar.x - ponto.x)**2 + 
                (posicao_radar.y - ponto.y)**2
            )
            
            #Indica que o raio está cobrindo o ponto
            if distancia <= raio_radar:
                pontos_cobertos.append(ponto)
        
        return pontos_cobertos

    def heuristica_regional(self, points, size_map, num_radares, raio_radar):
        """
        Método principal da heuristica
        """
        
        regioes = self.dividir_região(points, size_map, raio_radar)
        
        #Retorna uma lista decrescente de regiões com base no seu score.
        regioes_priorizadas = self.priorizar_regioes(regioes, raio_radar)
        
        radares_posicionados = []
        pontos_cobertos = set()
        
        # P/ cada região realiza uma busca gulosa do melhor ponto candidato (resolver_regiao) 
        for regiao_info in regioes_priorizadas:
            # print(f"Radares posicionados até agora = {len(radares_posicionados)}")
            
            if len(radares_posicionados) >= num_radares:
                break
                
            radares_restantes = num_radares - len(radares_posicionados)
            #print(f"RESOLVENDO REGIÃO = {regiao_info}")
            novos_radares = self.resolver_regiao(
                regiao_info, radares_restantes, raio_radar, pontos_cobertos
            )
            
            radares_posicionados.extend(novos_radares)
            
            # Atualiza pontos cobertos
            for radar in novos_radares:
                pontos_cobertos.update(
                    self.pontos_cobertos_por_radar(radar, points, raio_radar)
                )
        
        radares_finais = radares_posicionados
        return radares_finais
    
    def priorizar_regioes(self, regioes, raio_radar):
        regioes_avaliadas = []
        
        for regiao_id, pontos_regiao in regioes.items():
            if not pontos_regiao:
                continue
                
            densidade = len(pontos_regiao)
            
            # Se terreno == 0 (sem elevação === Melhor)
            qualidade_terreno = sum(
                2 if p.terrain_type == 0 else 1 if p.terrain_type == 1 else 0.5 
                for p in pontos_regiao
            ) / len(pontos_regiao)
            
            potencial_cobertura = self.calcular_potencial_cobertura(
                pontos_regiao, raio_radar
            )
            
            centralidade = self.calcular_centralidade(pontos_regiao)
            
            score_regiao = (0.2 * densidade + 
                    0.4 * qualidade_terreno + 
                    0.3 * potencial_cobertura + 
                    0.1 * centralidade)
            
            regioes_avaliadas.append({
                'id': regiao_id,
                'pontos': pontos_regiao,
                'score': score_regiao,
                'densidade': densidade,
                'qualidade_terreno': qualidade_terreno
            })
        
        return sorted(regioes_avaliadas, key=lambda x: x['score'], reverse=True)
    
    def resolver_regiao(self, regiao_info, max_radares, raio_radar, pontos_ja_cobertos):
       
        pontos_regiao = regiao_info['pontos']
        
        pontos_nao_cobertos = [
            p for p in pontos_regiao 
            if id(p) not in pontos_ja_cobertos
        ]
        
        if not pontos_nao_cobertos:
            return []
        
        radares_regiao = []
        
        # Busca Gulosa
        for _ in range(max_radares):
            melhor_posicao = self.encontrar_melhor_posicao_regiao(
                pontos_nao_cobertos, raio_radar, radares_regiao
            )
            
            if not melhor_posicao:
                break
                
            radares_regiao.append(melhor_posicao)
            
            
            pontos_cobertos_novo = self.pontos_cobertos_por_radar(
                melhor_posicao, pontos_nao_cobertos, raio_radar
            )
            
            pontos_nao_cobertos = [
                p for p in pontos_nao_cobertos 
                if id(p) not in {id(pc) for pc in pontos_cobertos_novo}
            ]
            
            if not pontos_nao_cobertos:
                break
        
        return radares_regiao

    def encontrar_melhor_posicao_regiao(self, pontos_disponiveis, raio_radar, radares_existentes):
        """
        Encontra a melhor posição para um radar dentro da região
        """
        if not pontos_disponiveis:
            return None
        
        melhor_posicao = None
        melhor_score = -1
        
        #Alternativa gulosa que busca um ponto possível dentro de todos os outrso
        for candidato in pontos_disponiveis:
            
            pontos_cobertos = self.pontos_cobertos_por_radar(
                candidato, pontos_disponiveis, raio_radar
            )
            
            
            sobreposicao = self.calcular_sobreposicao(
                candidato, radares_existentes, raio_radar
            )
            
            
            cobertura = len(pontos_cobertos)
            qualidade = 2 if candidato.terrain_type == 0 else 1 if candidato.terrain_type == 1 else 0.5
            
            # Penaliza sobreposição
            score = cobertura * qualidade * (1 - sobreposicao * 0.5)
            
            if score > melhor_score:
                melhor_score = score
                melhor_posicao = candidato
        
        return melhor_posicao