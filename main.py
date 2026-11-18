
import streamlit as st
import pandas as pd


class Lista:

    def __init__(self):
        if "lista" not in st.session_state:
            st.session_state.lista = []

    def adicionar(self, nome, preco, quantidade, unidade_medida):
        if nome.strip() and preco > 0 and quantidade > 0:

            item = {
                "nome": nome.strip().title(),
                "preco": preco,
                "quantidade": quantidade,
                "valor": preco * quantidade,
                "unidade_medida": unidade_medida
            }

            st.session_state.lista.append(item)
            return True

        return False

    def obter_dados(self):
        return pd.DataFrame(st.session_state.lista)

    def total(self):
        return sum(item["valor"] for item in st.session_state.lista)

    def limpar(self):
        st.session_state.lista = []

    def remover(self, indice):
        if 0 <= indice < len(st.session_state.lista):
            st.session_state.lista.pop(indice)


class Aplicacao:

    def __init__(self):
        self.lista = Lista()

    def executar(self):

        st.set_page_config(
            page_title="Lista de Compras",
            page_icon="🛒",
            layout="wide"
        )

        st.title("🛒 Lista de Compras")
        st.caption("Gerencie seus produtos, quantidades e valores.")

        with st.container(border=True):
            st.subheader("Adicionar produto")

            with st.form("form_produto", clear_on_submit=True):

                col1, col2 = st.columns([2, 1])

                with col1:
                    nome = st.text_input("Nome do produto")

                with col2:
                    unidade = st.selectbox(
                        "Unidade de medida",
                        ["unidade", "kg", "g", "litro", "ml", "pacote", "caixa"]
                    )

                col3, col4 = st.columns(2)

                with col3:
                    preco = st.number_input(
                        "Preço unitário (R$)",
                        min_value=0.0,
                        step=0.50,
                        format="%.2f"
                    )

                with col4:
                    quantidade = st.number_input(
                        "Quantidade",
                        min_value=0.01,
                        value=1.0,
                        step=1.0
                    )

                adicionar = st.form_submit_button(
                    "➕ Adicionar produto",
                    use_container_width=True
                )

                if adicionar:
                    if self.lista.adicionar(nome, preco, quantidade, unidade):
                        st.success(f"{nome} adicionado com sucesso!")
                    else:
                        st.warning("Informe o nome e um preço maior que zero.")

        st.divider()

        df = self.lista.obter_dados()

        st.subheader("Resumo da compra")

        col1, col2, col3 = st.columns(3)

        col1.metric("Produtos", len(df))
        col2.metric(
            "Quantidade de itens",
            f"{df['quantidade'].sum():g}" if not df.empty else "0"
        )
        col3.metric("Valor total", f"R$ {self.lista.total():,.2f}")

        st.divider()

        st.subheader("📋 Produtos adicionados")

        if not df.empty:

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "nome": st.column_config.TextColumn("Produto"),
                    "preco": st.column_config.NumberColumn(
                        "Preço unitário",
                        format="R$ %.2f"
                    ),
                    "quantidade": st.column_config.NumberColumn(
                        "Quantidade",
                        format="%.2f"
                    ),
                    "unidade_medida": st.column_config.TextColumn("Unidade"),
                    "valor": st.column_config.NumberColumn(
                        "Valor total",
                        format="R$ %.2f"
                    )
                }
            )

            col1, col2 = st.columns(2)

            with col1:
                indice = st.selectbox(
                    "Produto para remover",
                    range(len(df)),
                    format_func=lambda i: df.iloc[i]["nome"]
                )

                if st.button("🗑️ Remover produto", use_container_width=True):
                    self.lista.remover(indice)
                    st.rerun()

            with col2:
                if st.button("🧹 Limpar lista", use_container_width=True):
                    self.lista.limpar()
                    st.rerun()

        else:
            st.info("Sua lista está vazia. Adicione seu primeiro produto!")

        st.divider()

        st.caption("Lista de compras | Desenvolvido em Python + Streamlit")


if __name__ == "__main__":
    st.set_page_config(
        page_title="Lista de Compras",
        page_icon="🛒",
        layout="wide"
    )

    app = Aplicacao()
    app.executar()
