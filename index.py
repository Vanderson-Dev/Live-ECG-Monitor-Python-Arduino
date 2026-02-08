
### Codigo para simulação

import streamlit as st
import matplotlib.pyplot as plt
from collections import deque
import random
import time
import numpy as np      #adicionado por william para o pbm

st.markdown(
    """
    <style>
        [data-testid="stStatusWidget"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Configurações do buffer
max_pontos = 200
dados = deque([0]*max_pontos, maxlen=max_pontos)

bpm_max = 0
bpm_min = float("inf")

st.set_page_config(layout="wide")


# Título no Streamlit
st.markdown(
    "<h1 style='text-align: center;'>Batimentos</h1>",
    unsafe_allow_html=True
)
# Layout com margens (gráfico centralizado)
left, center, right = st.columns([1, 6, 1])

grafico_placeholder = center.empty()

bpm_placeholder = right.empty()
right.markdown("---")
max_placeholder = right.empty()
right.markdown("---")
min_placeholder = right.empty()

limiar = 800 # valor acima do qual consideramos um "batimento" adicionado por william
ultimos_batimentos = deque(maxlen=10) # guarda tempos dos últimos batimentos adicionado por william

# Loop principal de atualização
while True:
    # Simula leitura do Arduino
    valor = random.randint(0, 1023)
    dados.append(valor)

    #detector batimento
    if valor > limiar:
        tempo_atual = time.time()
        if len(ultimos_batimentos) == 0 or (tempo_atual - ultimos_batimentos[-1])> 0.3:
            ultimos_batimentos.append(tempo_atual)
    
    #calcula BPM
    bpm = 0
    if len(ultimos_batimentos)>1:
        intervalos = np.diff(ultimos_batimentos)
        media_intervalo = np.mean(intervalos)
        bpm = 60/media_intervalo

    if bpm > 0:
        bpm_max = max(bpm_max, bpm)
        bpm_min = min(bpm_min, bpm)

    # Cria figura do matplotlib
    fig, ax = plt.subplots(figsize=(8, 4))

    # Cor de fundo
    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    # Linha do gráfico (vermelha)
    ax.plot(dados, color="red", linewidth=2)

    # Limites
    ax.set_ylim(0, 1023)

    # Títulos e labels (brancos)
    #ax.set_title(f"Último valor: {valor}", color="white")
    ax.set_ylabel("Sinal", color="white")
    ax.set_xlabel("Tempo", color="white")

    # Eixos e ticks brancos
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")

    # Bordas do gráfico brancas
    for spine in ax.spines.values():
        spine.set_color("white")
    
    ax.grid(
        True,
        color="white",
        linestyle="--",
        linewidth=0.5,
        alpha=0.3
    )

    # Mostra/atualiza gráfico no Streamlit
    grafico_placeholder.pyplot(fig)
    plt.close(fig) 
    

    if bpm > 0:
        if bpm < 50:
            status = "🟡 Baixa"
        elif bpm <= 100:
            status = "🟢 Normal"
        else:
            status = "🔴 Alta"
    else:
        status = "⏳ Calculando..."

    bpm_placeholder.metric(
        label="❤️ Frequência Cardíaca",
        value=f"{bpm:.1f} BPM",
        delta=status
    )

    max_placeholder.metric(
        label="📈 Frequência Máxima",
        value=f"{bpm_max:.1f} BPM",
        delta="Máx"
    )

    min_placeholder.metric(
        label="📉 Frequência Mínima",
        value=f"{bpm_min:.1f} BPM",
        delta= "Min",
        delta_color="red"
    )


    # Pequena pausa para não travar o navegador
    time.sleep(0.05)
