import streamlit as st
import pickle

import numpy as np
import pandas as pd

termos = ['homem', 'mestre', 'pessoa', 
          'real', 'porta', 'fortuna', 
          'esquerda', 'direita', 'espada', 
          'licença','sala', 
          'judeu', 'pecado', 'industria', 
          'retrato', 'negro', 'academia', 
          'exame', 'sinal', 'voto', 
          'carambola', 'mortal']
termos = sorted(termos)

def random_samples_clusters(corpus, method, termo_alvo, num_examples_per_cluster = 5):
    """
    Seleciona aleatoriamente exemplos de sentença por cluster.

    Args:
        corpus (pandas.DataFrame): DataFrame contendo os dados de entrada.
        method (str): Nome do método de cluster.
            - 'pca': Clusterização usando PCA.
            - 'tsne': Clusterização usando t-SNE.
        num_examples_per_cluster (int, optional): Número de exemplos a serem selecionados por cluster.
            Padrão: 5.

    Returns:
        None
    """
    # Dictionary to store examples from each cluster
    cluster_examples = {}

    # Iterate over each unique cluster label
    for cluster_label in corpus[method].unique():
        # Select sentences and years from the current cluster
        cluster_data = corpus[corpus[method] == cluster_label][['sentence', 'ano']]

        # Sample random examples from the cluster
        sampled_examples = cluster_data.sample(n=num_examples_per_cluster)

        # Stohre examples in the dictionary with te cluster label as key
        cluster_examples[cluster_label] = sampled_examples

    # Print examples from each cluster
    for cluster_label, examples in cluster_examples.items():
        st.write(f"Cluster {cluster_label}:")
        for idx, row in examples.iterrows():
            st.write(f"  Example {idx + 1} (Year: {row['ano']}): {row['sentence']}")
        st.write()



st.title('Análise diacrônica da mudança semântica lexical nas representações vetoriais em língua portuguesa.')
st.write('Amostragem de textos por cluster utilizando o algoritmo de clusterização kmeans.')

option_termo = st.selectbox(
    "Termo",
    (["--"] + termos))

option_method = st.selectbox(
    "Método",
    (["--", "pca", "tsne"]))

st.write("Você selecionou o termo:", option_termo)

option_nexamples = st.slider("Quantos exemplos de cada cluster deseja exibir?", 0, 5, 3)

if st.button("Exibir exemplos", type="primary"):
    if option_termo is not "--" and option_method is not "--":
        try:
            corpus = pd.read_csv(f'embeddings_t1/tycholina_{option_termo}_embb_cluster_t1.csv')
            # fig = grafico_similares(option_model, option_termo)
            random_samples_clusters(corpus, option_method, option_termo, num_examples_per_cluster = option_nexamples)
            # st.plotly_chart(fig)
        except:
            st.write('erro, tente diminuir o número de exemplos por cluster.')
    else:
        st.write("Selecione um termos e método.")