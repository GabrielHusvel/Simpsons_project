import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def process_csv(uploaded_file):
    """
    Processa um arquivo CSV carregado pelo usuário.

    Args:
        uploaded_file: Arquivo CSV carregado.

    Returns:
        Um DataFrame Pandas se o arquivo for válido, senão retorna uma mensagem de erro.
    """
    try:
        # Lê o arquivo CSV
        df = pd.read_csv(uploaded_file)

        # Verifica se as colunas 'Fala' e 'Categoria' existem
        required_cols = ["Fala", "Categoria"]
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"O arquivo CSV deve conter as colunas: {', '.join(required_cols)}")

        return df

    except pd.errors.EmptyDataError:
        return "O arquivo CSV está vazio."
    except pd.errors.ParserError:
        return "Erro ao analisar o arquivo CSV. Por favor, verifique se o formato está correto."
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Ocorreu um erro inesperado: {e}"


def analisar_categorias(df):
    """
    Analisa um DataFrame Pandas para contar e calcular a proporção de ocorrências de cada categoria.

    Args:
        df: Um DataFrame Pandas com colunas 'Fala' e 'Categoria'.

    Returns:
        Um DataFrame Pandas com as categorias, suas contagens e proporções.
    """
    # Verifica se o DataFrame contém as colunas necessárias
    if not all(col in df.columns for col in ['Fala', 'Categoria']):
        raise ValueError("O DataFrame deve conter as colunas 'Fala' e 'Categoria'.")

    # Conta as ocorrências de cada categoria
    contagens = df['Categoria'].value_counts()

    # Calcula as proporções
    total = len(df)
    proporcoes = contagens / total

    # Cria um DataFrame com os resultados
    resultado = pd.DataFrame({
        'Categoria': contagens.index,
        'Contagem': contagens.values,
        'Proporção': proporcoes.values
    })

    return resultado


def plot_proportions_pie_chart(df):
    """
    Gera e exibe um gráfico de pizza Plotly a partir de um DataFrame.

    Args:
        df: Um DataFrame Pandas com colunas 'Categoria', 'Contagem', e 'Proporção'.
    """

    required_cols = ['Categoria', 'Contagem', 'Proporção']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"O DataFrame deve conter as colunas: {', '.join(required_cols)}")

    # Cria o gráfico de pizza
    fig = go.Figure(data=[go.Pie(
        labels=df['Categoria'],
        values=df['Proporção'],
        textinfo='percent',
        insidetextorientation='radial'
    )])

    fig.update_traces(hoverinfo='label+percent', textfont_size=20,
                      marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(title_text="Proporções das Categorias")

    st.plotly_chart(fig)



def main():
    st.title("Análise de Sentimento com Gráfico de Pizza")
    st.markdown("Carregue um arquivo CSV contendo as colunas 'Fala' e 'Categoria'.")

    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

    if uploaded_file is not None:
        result = process_csv(uploaded_file)

        if isinstance(result, pd.DataFrame):
            st.success("Arquivo CSV carregado com sucesso!")
            st.dataframe(result)

            try:
                categorias_df = analisar_categorias(result)
                st.subheader("Resumo das Categorias")
                st.dataframe(categorias_df)
                st.subheader("Gráfico de Pizza")
                plot_proportions_pie_chart(categorias_df)
            except ValueError as e:
                st.error(f"Erro: {e}")
        else:
            st.error(result)

if __name__ == "__main__":
    main()