import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Configuração do Streamlit
st.set_page_config(layout="centered")
st.title("Previsor de Preço de Lanches 🍔")
st.subheader("Modelo de Regressão Linear")
st.divider()

# Carregar o arquivo já codificado
try:
    # Acessa o arquivo lanches.csv mais atualizado
    df = pd.read_csv("lanches.csv")
except FileNotFoundError:
    st.error("Erro: O arquivo 'lanches.csv' não foi encontrado.")
    st.stop()

# Garantir que as colunas são limpas e convertidas para minúsculas.
df.columns = df.columns.str.strip().str.lower()

# ----------------------------------------------------
# NOVO TREINAMENTO DO MODELO (FORÇANDO PROPORCIONALIDADE)
# ----------------------------------------------------

# 1. Identificar colunas de sabor (One-Hot Encoded)
colunas_sabor = [col for col in df.columns if col not in ['comprimento', 'preço']]

# 2. Engenharia de Features: Criar termos de interação (Sabor * Comprimento)
# Este é o segredo para forçar o preço a ser uma função direta do comprimento.
for col in colunas_sabor:
    # CORREÇÃO: Padronizar o nome da coluna de interação substituindo espaços por underscores.
    col_feature_name = col.replace(' ', '_')
    df[f'{col_feature_name}_comp'] = df[col] * df['comprimento']

# 3. Separar variáveis independentes (x) e dependente (y)
# X agora contém APENAS as colunas de interação (Sabor * Comprimento).
x = df.filter(like='_comp') 
y = df["preço"]

# 4. Treinar o modelo FORÇANDO fit_intercept=False
# Isso força o preço a ser 0 quando o comprimento for 0 (perfeita proporcionalidade).
try:
    # fit_intercept=False garante que o modelo aprende a proporção.
    modelo = LinearRegression(fit_intercept=False)
    modelo.fit(x, y)
    
    # st.success("Modelo retreinado com sucesso com a nova estrutura de features!") # Mensagem de sucesso opcional
    
except Exception as e:
    st.error(f"Erro ao treinar o modelo: {e}")
    st.stop()


# ----------------------------------------------------
# LÓGICA DE PREVISÃO
# ----------------------------------------------------

# Preparar as opções de lanche para a UI
opcoes_ui = [sabor.title() for sabor in colunas_sabor]

# Selecionar o tipo de lanche
tipo_lanche_ui = st.selectbox("Escolha o tipo de lanche:", opcoes_ui)
# min_value alterado para inteiro (1) e step para 5 (inteiro) para evitar o warning de formatação.
tamanho = st.number_input("Tamanho do lanche (cm):", min_value=1, step=5, format="%d")

if st.button("Prever Preço"):
    if tamanho > 0:
        # 1. Obter o nome da coluna de sabor no formato que o modelo espera (minúsculas).
        coluna_sabor_min = tipo_lanche_ui.lower()
        
        # 2. Obter o nome da feature de INTERAÇÃO, padronizando o espaço para underscore.
        feature_name = coluna_sabor_min.replace(' ', '_') + '_comp'

        # 3. Preparar a entrada de PREVISÃO com as novas features de interação
        entrada_interacao = {}
        
        # Iterar sobre todas as features de treino (ex: 'frango_comp', 'carne_seca_com_cream_cheese_comp')
        for col in x.columns: 
            # 4. Definir a feature de interesse (sabor e comprimento) com o valor do tamanho.
            if col == feature_name:
                entrada_interacao[col] = tamanho
            else:
                # 5. Para todas as outras features de interação (outros sabores), o valor é zero.
                entrada_interacao[col] = 0

        # 6. Converter para DataFrame na ordem correta das colunas de treino
        entrada_df = pd.DataFrame([entrada_interacao], columns=x.columns)

        try:
            # Fazer a previsão
            preco_previsto = modelo.predict(entrada_df)[0]
            
            # Garantir que o preço não é negativo
            preco_previsto = max(0, preco_previsto) 

            st.markdown(
                f"""
                <div style='background-color: #f0f8ff; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #cceeff;'>
                    <h3 style='color: #007bff;'>Resultado da Previsão</h3>
                    <p style='font-size: 1.1em;'>O preço previsto para um {tipo_lanche_ui} de {tamanho:.0f} cm é</p>
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
st.caption("Ajuste de Modelo: Usamos termos de interação (Sabor x Comprimento) e forçamos o modelo a não ter intercepto para garantir uma proporcionalidade perfeita.")
