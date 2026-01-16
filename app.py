import streamlit as st
import calendar
from datetime import date
import plotly.graph_objects as go

# ===== CONFIGURAÇÃO DO NEGÓCIO =====
DATA_BASE = date(2020, 1, 1)
PERIODICIDADE = 3

CORES = {
    "A/B": "#8BC34A",   # verde
    "C/D": "#FB8C00",   # laranja
    "OFF": "#E0E0E0"    # cinza (fora do mês)
}

# ===== REGRA DO RODÍZIO =====
def grupo_por_data(d):
    delta = (d - DATA_BASE).days
    return "A/B" if (delta // PERIODICIDADE) % 2 == 0 else "C/D"

# ===== GERA CALENDÁRIO =====
def gerar_calendario(ano, mes):
    cal = calendar.Calendar(calendar.SUNDAY)
    semanas = cal.monthdatescalendar(ano, mes)

    dados = []
    cores = []

    for semana in semanas:
        linha = []
        linha_cor = []

        for d in semana:
            if d.month == mes:
                grupo = grupo_por_data(d)
                linha.append(f"{d.day}<br><b>{grupo}</b>")
                linha_cor.append(CORES[grupo])
            else:
                # FORA DO MÊS → CINZA E SEM TURMA
                linha.append(str(d.day))
                linha_cor.append(CORES["OFF"])

        dados.append(linha)
        cores.append(linha_cor)

    return dados, cores


# ===== APP =====
st.title("Calendário de Rodízio")

ano = st.selectbox("Ano", list(range(2020, 2036)), index=5)
mes = st.selectbox(
    "Mês",
    list(range(1, 13)),
    format_func=lambda x: calendar.month_name[x]
)

dados, cores = gerar_calendario(ano, mes)

fig = go.Figure(
    data=[
        go.Table(
            header=dict(
                values=["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SÁB"],
                fill_color="#1976D2",
                font=dict(color="white", size=14),
                align="center"
            ),
            cells=dict(
                values=list(zip(*dados)),
                fill_color=cores,
                font=dict(color="black", size=13),
                align="center",
                height=55
            )
        )
    ]
)

fig.update_layout(
    title=f"{calendar.month_name[mes]} / {ano}",
    margin=dict(l=10, r=10, t=60, b=10)
)

st.plotly_chart(fig, use_container_width=True)
