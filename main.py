
import streamlit as st


class Lista:

    def __init__(self):
        if "lista" not in st.session_state:
            st.session_state.lista = []

    def adicionar(self, nome, preco, quantidade, unidade_medida):
        if nome.strip() and preco >= 0 and quantidade > 0:
            item = {
                "nome": nome,
                "preco": preco,
                "quantidade": quantidade,
                "valor": preco * quantidade,
                "unidade_medida": unidade_medida
            }

            st.session_state.lista.append(item)
            return True

        return False

    def exibir(self):
        for i, item in enumerate(st.session_state.lista, start=1):
            st.write(
                f"**{i}. {item['nome']}** | "
                f"Preço: R$ {item['preco']:.2f} | "
                f"Quantidade: {item['quantidade']} {item['unidade_medida']} | "
                f"Valor: R$ {item['valor']:.2f}"
            )

    def total(self):
        return sum(item["valor"] for item in st.session_state.lista)

    def limpar(self):
        st.session_state.lista = []


class Aplicacao:

    def __init__(self):
        self.lista = Lista()

    def executar(self):
        st.title("Calculadora de Lista")

        nome = st.text_input("Nome do item:")
        preco = st.number_input("Preço unitário (R$):", min_value=0.0, step=0.50)
        quantidade = st.number_input("Quantidade:", min_value=0.01, step=1.0)
        unidade = st.selectbox(
            "Unidade de medida:",
            ["unidade", "kg", "g", "litro", "ml", "pacote", "caixa"]
        )

        if st.button("Adicionar"):
            if self.lista.adicionar(nome, preco, quantidade, unidade):
                st.success(f"{nome} adicionado!")
                st.rerun()
            else:
                st.warning("Informe um nome válido.")

        st.subheader("Lista de itens")
        self.lista.exibir()

        st.divider()

        st.metric("Valor total", f"R$ {self.lista.total():.2f}")

        if st.button("Limpar lista"):
            self.lista.limpar()
            st.rerun()


if __name__ == "__main__":
    app = Aplicacao()
    app.executar()
