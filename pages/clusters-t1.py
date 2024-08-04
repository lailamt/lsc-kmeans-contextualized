import streamlit as st
import pickle

import numpy as np
import pandas as pd
import random

termos = ['homem', 'mestre','pessoa','real','porta',
        'memoria','fortuna','esquerda','direita',
        'espada','licença','virgem','vasco',
        'página','sala','judeu','pecado',
        'industria','vergonhas','retrato','negro',
        'impressa','academia','cambio','marcha',
        'exame','rede','tela','sinal',
        'voto','coxinha','lagarta','broca',
        'biscate','carambola','mortal','perereca',
        'peteca','birosca','estilete','peteca','ruge']
termos = sorted(termos)

def random_samples_clusters(corpus, termo_alvo, num_examples_per_cluster = 5):
    """
    Seleciona aleatoriamente exemplos de sentença por cluster.

    Args:
        corpus (pandas.DataFrame): DataFrame contendo os dados de entrada.
        num_examples_per_cluster (int, optional): Número de exemplos a serem selecionados por cluster.
            Padrão: 5.

    Returns:
        None
    """
    # Dictionary to store examples from each cluster
    cluster_examples = {}

    # Iterate over each unique cluster label
    for cluster_label in corpus['cluster'].unique():
        # Select sentences and years from the current cluster
        cluster_data = corpus[corpus['cluster'] == cluster_label][['sentenca', 'ano']]

        # Sample random examples from the cluster
        sampled_examples = cluster_data.sample(n=num_examples_per_cluster)

        # Stohre examples in the dictionary with te cluster label as key
        cluster_examples[cluster_label] = sampled_examples

    # Print examples from each cluster
    for cluster_label, examples in cluster_examples.items():
        st.write(f"Cluster {cluster_label}:")
        for idx, row in examples.iterrows():
            st.write(f"  Example {idx + 1} (Year: {row['ano']}): {row['sentenca']}")
        st.write()

def imprimir_clusters(dataframe, exemplos_por_cluster = 5):
    """
    Imprime os clusters do dataframe, com exemplos de textos aleatórios.

    Args:
        dataframe: DataFrame com as colunas 'Ano', 'Texto' e 'Cluster'.
        exemplos_por_cluster: Número de exemplos de textos a serem impressos por cluster.
    """

    clusters_unicos = dataframe['cluster'].unique()
    clusters_unicos.sort()  # Garante a ordem crescente dos clusters

    for cluster in clusters_unicos:
        st.write(f"Cluster {cluster}:")
        textos_cluster = dataframe[dataframe['cluster'] == cluster]
        num_exemplos = min(exemplos_por_cluster, len(textos_cluster))  # Limita o número de exemplos
        textos_aleatorios = random.sample(list(textos_cluster['sentenca']), num_exemplos)
        for i in range(num_exemplos):
            ano = textos_cluster.iloc[i]['ano']
            texto = textos_aleatorios[i]
            st.write(f"  {ano} - {texto}")
        st.write()  # Linha em branco entre os clusters



st.title('Análise diacrônica da mudança semântica lexical nas representações vetoriais em língua portuguesa.')
st.write('Amostragem de textos por cluster utilizando o algoritmo de clusterização kmeans.')

option_termo = st.selectbox(
    "Termo",
    (["--"] + termos))

option_modelo = st.selectbox(
    "Modelo",
    (["--", "bertimbau", "roberta", "albertina"]))

st.write("Você selecionou o termo:", option_termo)

option_nexamples = st.slider("Quantos exemplos de cada cluster deseja exibir?", 0, 5, 3)

if st.button("Exibir exemplos", type="primary"):
    if ((option_termo != "--") and (option_modelo != "--")):
        try:
            corpus = pd.read_csv(f'clusters_t1/{option_modelo}/{option_termo}_cluster_t1.csv')
            max_exemplos_por_cluster = corpus['cluster'].value_counts().min()
            # Ajuste o valor de option_nexamples
            option_nexamples = min(option_nexamples, max_exemplos_por_cluster)
            imprimir_clusters(corpus, exemplos_por_cluster = option_nexamples)
            # imprimir_clusters(corpus, exemplos_por_cluster = option_nexamples)
            # fig = grafico_similares(option_model, option_termo)
            # random_samples_clusters(corpus, option_termo, num_examples_per_cluster = option_nexamples)
            # st.plotly_chart(fig)
        except:
            st.write('erro, termo não encontrado na janela.')
    else:
        st.write("Selecione um termos e método.")