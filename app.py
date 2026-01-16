import streamlit as st
import calendar
from datetime import date
import plotly.graph_objects as go

# ===== CONFIGURAÇÃO FIXA =====
DATA_BASE = date(2025, 12, 30)

CORES = {
    "A/B": "#8BC34A",   # verde 
    "C/D": "#FB8C00",   # laranja 
    "OFF": "#E0E0E0"    # cinza
}

# ===== REGRA DE NEGÓCIO (FECHADA E CORRETA) =====
def grupo_por_data(d):
    delta = (d - DATA_BASE).days
    pos = delta % 6 
    return "A/B" if pos < 3 else "C/D"

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
            if d.month != mes:
                # fora do mês
                linha.append(str(d.day))
                linha_cor.append(CORES["OFF"])
            else:
                grupo = grupo_por_data(d)
                linha.append(f"{d.day}<br><b>{grupo}</b>")
                linha_cor.append(CORES[grupo])

        dados.append(linha)
        cores.append(linha_cor)

    return dados, cores

# ===== APP =====
st.title("Calendário de Rodízio")

ano = st.selectbox("Ano", list(range(2025, 2036)), index=1)
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
                fill_color=list(zip(*cores)),     
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
