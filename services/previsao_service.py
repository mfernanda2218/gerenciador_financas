from datetime import datetime, timedelta
from collections import defaultdict

class PrevisaoService:
    """
    Serviço para lógica de negócio relacionada à previsão financeira.
    """
    def __init__(self, transacoes, categorias):
        self.transacoes = transacoes
        self.categorias = {c.id: c.nome for c in categorias} # Mapeia ID da categoria para nome

    def prever_gastos_proximo_mes(self, num_meses_historico=3):
        """
        Prevê os gastos do próximo mês com base na média dos últimos N meses.
        Args:
            num_meses_historico (int): Número de meses para considerar no histórico.
        Returns:
            dict: Um dicionário com a previsão de gastos por categoria para o próximo mês.
        """
        # Calcular a data de início para o histórico
        hoje = datetime.now()
        data_limite = (hoje - timedelta(days=30 * num_meses_historico)).date() # Aproximadamente N meses atrás

        gastos_por_mes_categoria = defaultdict(lambda: defaultdict(float))
        meses_contados = set()

        # Agrupa gastos por categoria e mês
        for t in self.transacoes:
            if t.data >= data_limite and t.tipo == 'despesa':
                mes_ano = t.data.strftime('%Y-%m')
                categoria_nome = self.categorias.get(t.categoria_id, 'Sem Categoria')
                gastos_por_mes_categoria[mes_ano][categoria_nome] += float(t.valor)
                meses_contados.add(mes_ano)

        # Calcula a média dos gastos por categoria
        previsao_por_categoria = defaultdict(float)
        if not meses_contados:
            return {} # Não há dados históricos suficientes

        for mes_ano in gastos_por_mes_categoria:
            for categoria, valor in gastos_por_mes_categoria[mes_ano].items():
                previsao_por_categoria[categoria] += valor

        # Divide pelo número de meses para obter a média
        num_meses_validos = len(meses_contados)
        for categoria in previsao_por_categoria:
            previsao_por_categoria[categoria] /= num_meses_validos

        return {k: round(v, 2) for k, v in previsao_por_categoria.items()} # Arredonda para 2 casas decimais
