import streamlit as st
import pandas as pd
import statsmodels.formula.api as smf
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

data = pd.read_csv("./dashboardData.csv")
tabOptions = ["Tabela", "Rozkład zmiennych", "Zależności ceny od zmiennych", "Model regresji"]
tab = option_menu(
    menu_title="Menu",
    options=["Tabela", "Rozkład zmiennych", "Zależności ceny od zmiennych", "Model regresji"]
)
variableOptions = ["carat", "clarity", "cut", "color", "x dimension", "y dimension", "z dimension", "depth", "table", "price"]

if tab == tabOptions[0]:
    st.header(tabOptions[0])
    st.dataframe(data=data.iloc[:, :-1])

elif tab == tabOptions[1]:
    st.header(tabOptions[1])
    selectedVariable = st.selectbox("Zmienna", variableOptions)

    st.plotly_chart(px.histogram(data, x=selectedVariable))

elif tab == tabOptions[2]:
    st.header(tabOptions[2])

    selectedVariable = st.selectbox("Zmienna", variableOptions[:9])

    st.plotly_chart(px.scatter(data, x=selectedVariable, y="price"))
    
elif tab == tabOptions[3]:
    st.header(tabOptions[3])
    model = smf.ols(data=data, formula="price ~ carat").fit()
    data["fitted"] = model.fittedvalues

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["carat"], y=data["price"], name="price vs carat", mode="markers"))
    fig.add_trace(go.Scatter(x=data["carat"], y=data["fitted"], name="Fitted regression line"))
    fig.update_layout(title="Regression line of price vs carat", xaxis_title="Price")
    st.plotly_chart(fig)