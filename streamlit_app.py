import streamlit as st
import pandas as pd

st.title("📊 Cohort Dashboard")

# Завантаження Excel-файлу через браузер
uploaded_file = st.file_uploader("Завантажте Excel-файл (cohort.xlsx)", type=["xlsx"])

if uploaded_file:
    # Зчитування файлу
    df = pd.read_excel(uploaded_file, skiprows=2)
    df.columns = ["PlayerId", "NetRev", "SumDep"]
    df["NetRev"] = pd.to_numeric(df["NetRev"], errors="coerce")
    df["SumDep"] = pd.to_numeric(df["SumDep"], errors="coerce")

    # Загальні значення
    total_netrev = df["NetRev"].sum()
    total_dep = df["SumDep"].sum()

    st.subheader("🔢 Загальні показники:")
    st.metric("Загальний NetRev", f"{total_netrev:.2f}")
    st.metric("Загальний SumDep", f"{total_dep:.2f}")

    st.markdown("---")

    st.subheader("📋 Дані по кожному юзеру:")
    st.dataframe(df)
else:
    st.info("⬆️ Завантажте файл, щоб побачити дашборд.")
