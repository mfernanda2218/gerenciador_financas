// Garante que o script só será executado após o carregamento completo do HTML.
document.addEventListener('DOMContentLoaded', function () {
    // Pega o elemento <canvas> onde o gráfico será renderizado.
    const ctx = document.getElementById('previsaoChart');

    // Verifica se o elemento canvas e os dados da previsão existem antes de continuar.
    // A variável `previsaoData` é criada no template HTML.
    if (ctx && typeof previsaoData !== 'undefined') {

        // Extrai as categorias (labels) e os valores (data) do objeto de dados.
        const categorias = Object.keys(previsaoData);
        const valores = Object.values(previsaoData);

        new Chart(ctx, {
            type: 'bar', // Tipo do gráfico. Pode ser 'bar', 'pie', 'doughnut', 'line', etc.
            data: {
                labels: categorias, // Rótulos do eixo X (ex: 'Alimentação', 'Transporte')
                datasets: [{
                    label: 'Valor Previsto (R$)',
                    data: valores, // Dados do eixo Y (os valores monetários)
                    backgroundColor: [ // Cores das barras
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(255, 206, 86, 0.5)',
                        'rgba(75, 192, 192, 0.5)',
                        'rgba(153, 102, 255, 0.5)',
                        'rgba(255, 159, 64, 0.5)'
                    ],
                    borderColor: [ // Cores das bordas das barras
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true, // Torna o gráfico responsivo
                maintainAspectRatio: false, // Permite que o gráfico preencha o container
                scales: {
                    y: {
                        beginAtZero: true, // Garante que o eixo Y comece no zero
                        ticks: {
                            // Formata os ticks do eixo Y para o formato de moeda BRL
                            callback: function(value, index, values) {
                                return 'R$ ' + value.toFixed(2).replace('.', ',');
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false // Oculta a legenda, pois o título do gráfico já é descritivo
                    },
                    title: {
                        display: true,
                        text: 'Previsão de Gastos por Categoria',
                        font: {
                            size: 18
                        }
                    },
                    tooltip: {
                        callbacks: {
                           // Formata a dica que aparece ao passar o mouse
                           label: function(context) {
                               let label = context.dataset.label || '';
                               if (label) {
                                   label += ': ';
                               }
                               if (context.parsed.y !== null) {
                                   label += new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(context.parsed.y);
                               }
                               return label;
                           }
                        }
                    }
                }
            }
        });
    }
});