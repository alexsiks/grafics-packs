import streamlit as st

st.title("Calculadora de Lista")

if "lista" not in st.session_state:
    st.session_state.lista = []

nome = st.text_input("Informe o nome do item:")

if st.button("Adicionar"):
    if nome.strip():
        st.session_state.lista.append(nome.strip())
        st.success(f"Item '{nome}' adicionado!")
    else:
        st.warning("Informe um nome válido.")

st.subheader("Lista de itens")

for i, item in enumerate(st.session_state.lista, start=1):
    st.write(f"{i}. {item}")

if st.button("Limpar lista"):
    st.session_state.lista = []
    st.rerun()