import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Configuração do Streamlit
st.set_page_config(layout="centered")
st.title(" Previsor de Preço de Lanches 🥪 ")
st.subheader("Modelo de Regressão Linear com Proporcionalidade")
st.divider()

# Carregar o arquivo já codificado
try:
    df = pd.read_csv("lanches.csv")
except FileNotFoundError:
    st.error("Erro: O arquivo 'lanches.csv' não foi encontrado.")
    st.stop()

# Garantir que as colunas são limpas e convertidas para minúsculas.
df.columns = df.columns.str.strip().str.lower()


# TREINAMENTO DO MODELO

colunas_sabor = [col for col in df.columns if col not in ['comprimento', 'preço']]

# Engenharia de Features: Criar termos de interação (Sabor * Comprimento)
# Isso força o preço a ser uma função direta e proporcional do comprimento.
for col in colunas_sabor:
    col_feature_name = col.replace(' ', '_')
    df[f'{col_feature_name}_comp'] = df[col] * df['comprimento']

# X contém APENAS as colunas de interação.
x = df.filter(like='_comp') 
y = df["preço"]

try:
    # fit_intercept=False força o modelo a aprender a proporção perfeita (preço=0 quando comprimento=0).
    modelo = LinearRegression(fit_intercept=False)
    modelo.fit(x, y)
    
except Exception as e:
    st.error(f"Erro ao treinar o modelo: {e}")
    st.stop()


# TESTES DE PROPORCIONALIDADE

with st.expander("📊 Testes de Proporcionalidade ", expanded=True):
    previsoes = modelo.predict(x)
    
    df_teste = df[['comprimento', 'preço']].copy()
    df_teste['Preço Previsto'] = previsoes
    
    # Adicionar a coluna de sabor (desfazer o one-hot encoding para visualização)
    df_teste['Sabor'] = df[colunas_sabor].idxmax(axis=1).str.title()
    
    df_teste['Diferença'] = df_teste['Preço Previsto'] - df_teste['preço']
    # np.isclose verifica se o erro é extremamente pequeno
    df_teste['Status'] = np.isclose(df_teste['Diferença'], 0, atol=1e-2)
    
    df_teste.rename(columns={'preço': 'Preço Real', 'comprimento': 'Comprimento (cm)'}, inplace=True)
    
    total_testes = len(df_teste)
    testes_aprovados = df_teste['Status'].sum()
    
    if testes_aprovados == total_testes:
        st.success(f"✅ Todos os {total_testes} testes aprovados!")
    else:
        st.error(f"❌ {total_testes - testes_aprovados} de {total_testes} testes falharam. O modelo não está 100% proporcional.")
    
    st.dataframe(
        df_teste[['Sabor', 'Comprimento (cm)', 'Preço Real', 'Preço Previsto', 'Diferença', 'Status']],
        hide_index=True
    )

st.divider()


# LÓGICA DE PREVISÃO


# Preparar as opções de lanche para o usuário
opcoes_ui = [sabor.title() for sabor in colunas_sabor]

tipo_lanche_ui = st.selectbox("Escolha o tipo de lanche:", opcoes_ui)
tamanho = st.number_input("Tamanho do lanche (cm):", min_value=1, step=5, format="%d")

if st.button("Prever Preço"):
    if tamanho > 0:
        coluna_sabor_min = tipo_lanche_ui.lower()
        
        # Nome da feature de interação que o modelo espera
        feature_name = coluna_sabor_min.replace(' ', '_') + '_comp'

        entrada_interacao = {}
        
        for col in x.columns: 
            # Define o valor de 'tamanho' apenas na feature de interação do sabor selecionado.
            if col == feature_name:
                entrada_interacao[col] = tamanho
            else:
                entrada_interacao[col] = 0 # Outros sabores são 0

        entrada_df = pd.DataFrame([entrada_interacao], columns=x.columns)

        try:
            preco_previsto = modelo.predict(entrada_df)[0]
            preco_previsto = max(0, preco_previsto) 

            st.markdown(
                f"""
                <div style='background-color: #f0f8ff; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #cceeff;'>
                    <h3 style='color: #007bff;'>Resultado da Previsão</h3>
                    <p style='font-size: 1.1em;'>O preço previsto para um **{tipo_lanche_ui}** de **{tamanho:.0f} cm** é</p>
                    <p style='font-size: 2.5em; font-weight: bold; color: #28a745;'>R$ {preco_previsto:.2f} 💰</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Erro ao fazer a previsão: {e}")
    else:
        st.warning("Por favor, insira um comprimento de lanche válido.")

st.divider()
st.caption("Desenvolvido por Marina Kally - Modelo de Regressão Linear com Proporcionalidade")
