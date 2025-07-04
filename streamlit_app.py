import streamlit as st
import pandas as pd

# Завантаження Excel-файлу
@st.cache_data
def load_data():
    df = pd.read_excel("cohort.xlsx", skiprows=2)
    df.columns = ["PlayerId", "NetRev", "SumDep"]
    df["NetRev"] = pd.to_numeric(df["NetRev"], errors="coerce")
    df["SumDep"] = pd.to_numeric(df["SumDep"], errors="coerce")
    return df

# Заголовок
st.title("🎯 Cohort Dashboard")

# Завантаження даних
df = load_data()

# Розрахунок загальних сум
total_netrev = df["NetRev"].sum()
total_dep = df["SumDep"].sum()

# Відображення загальних сум
st.subheader("🔢 Загальні показники по всім юзерам:")
st.metric("Загальний NetRev", f"{total_netrev:.2f}")
st.metric("Загальний SumDep", f"{total_dep:.2f}")

# Розділювач
st.markdown("---")

# Показ таблиці
st.subheader("📋 Дані по кожному юзеру:")
st.dataframe(df)
