# 🥪 Previsor de Preço de Lanches

### *Um modelo de Regressão Linear para prever o preço de lanches de acordo com o tipo e o comprimento (em cm).*

---

## 💡 Ideia Principal

Tudo começou com uma curiosidade:

> “E se eu quisesse um lanche de 20cm ou 40cm? Quanto custaria?” 🤔

Sabemos que o **Subway** trabalha com tamanhos de **15cm** e **30cm**, e em alguns casos o preço do de 30cm é **o dobro** do de 15cm.
Então pensei:

> “Será que consigo criar um modelo que calcule automaticamente o preço proporcional de qualquer tamanho de lanche?”

Foi aí que nasceu o **Previsor de Preço de Lanches**, um projeto que une **Python + Machine Learning (Regressão Linear)** para prever o preço de diferentes tipos de lanches com base no seu comprimento.

---

## ⚙️ Tecnologias Utilizadas

* 🐍 **Python 3.11+**
* 📦 **Pandas** — manipulação e análise dos dados
* 🧠 **Scikit-learn** — criação e treino do modelo de regressão linear
* 🌐 **Streamlit** — construção da interface web interativa
* ⚙️ **Poetry** — gerenciamento de dependências e ambiente virtual

---

## 💻 Como Executar o Projeto

### 🔹 1. Clonar o repositório
```bash
git clone https://github.com/marinakallybo/Previsor-Pre-os-Lanches.git
cd .\Previsor-Pre-os-Lanches\
````

### 🔹 2. Instalar o Poetry (caso ainda não tenha)

```bash
pip install poetry
```

### 🔹 3. Instalar as dependências

```bash
poetry install
```

### 🔹 4. Ativar o ambiente virtual

```bash
poetry shell
```

### 🔹 5. Rodar o app

```bash
streamlit run app.py
```

Após isso, o Streamlit abrirá automaticamente no navegador. 🎉

---

## 🧩 Estrutura do Projeto

```
📂 PROJETO-ML/
├── 📁 .venv/               # Ambiente virtual (criado automaticamente pelo Poetry)
├── 📁 src/                 # Módulos auxiliares (opcional)
├── 📁 tests/               # Testes automáticos
│
├── 📄 app.py               # Aplicação principal (modelo + interface)
├── 📄 lanches.csv          # Base de dados (lanches + preços)
├── 📄 pyproject.toml       # Configuração do Poetry e dependências
├── 📄 poetry.lock          # Controle de versões exatas
└── 📄 README.md            # Documentação do projeto
```

---

## 🍞 Conjunto de Dados

O arquivo `lanches.csv` foi criado com base nos lanches do **Subway**.
Foram selecionados **5 tipos de lanches**:

* Frango
* Frango Teriyaki
* Carne Seca com Cream Cheese
* Vegetariano
* Steak Churrasco

Cada lanche possui valores de **comprimento (15 e 30 cm)** e **preço proporcional**.
O formato da base utiliza **One-Hot Encoding**, onde cada tipo de lanche é representado por uma coluna com valores 0 ou 1 — assim o modelo entende variáveis categóricas corretamente.

Exemplo:

| Frango | Frango Teriyaki | Carne Seca com Cream Cheese | Vegetariano | Steak Churrasco | comprimento | preço |
| :----: | :-------------: | :-------------------------: | :---------: | :-------------: | :---------: | :---: |
|    1   |        0        |              0              |      0      |        0        |      15     | 18.30 |
|    1   |        0        |              0              |      0      |        0        |      30     | 36.60 |
|    0   |        1        |              0              |      0      |        0        |      15     | 25.20 |
|    0   |        1        |              0              |      0      |        0        |      30     | 44.10 |

---

## 🧠 Funcionamento do Modelo

O modelo utiliza **Regressão Linear Composta**, garantindo que o **preço aumente proporcionalmente** ao comprimento do lanche.
Ele cria termos de interação entre o tipo e o comprimento, como:

```python
frango_comp = Frango * Comprimento
```

Essas colunas permitem que o modelo aprenda quanto **cada cm de cada tipo de lanche** influencia no preço final.
O modelo é treinado com:

```python
LinearRegression(fit_intercept=False)
```

Isso assegura que o preço de 0 cm seja 0 — mantendo a proporcionalidade perfeita.

---

## 🧪 Testes de Proporcionalidade

O projeto inclui testes que verificam se o preço previsto é **idêntico** ao preço real dos dados de treino, garantindo total coerência matemática.

Exemplo:

| Sabor  | Comprimento (cm) | Preço Real | Preço Previsto | Diferença | Status |
| :----- | :--------------: | :--------: | :------------: | :-------: | :----: |
| Frango |        15        |    18.3    |      18.3      |    0.00   |    ✅   |
| Frango |        30        |    36.6    |      36.6      |    0.00   |    ✅   |

---

## 💻 Interface Interativa

A aplicação em **Streamlit** permite que o usuário:

✅ Escolha o tipo de lanche

✅ Digite o comprimento desejado (20 cm, 40 cm, etc.)

✅ Veja o preço previsto em tempo real

🔗 Acesse o projeto online:
👉 [https://marinakallybo-previsor-pre-os-lanches-app-mzedzy.streamlit.app](https://marinakallybo-previsor-pre-os-lanches-app-mzedzy.streamlit.app)

---

## 📚 Aprendizados

Esse projeto me ajudou a entender de forma prática:

* Diferença entre **regressão linear simples** e **múltipla**
* Como aplicar **One-Hot Encoding** em variáveis categóricas
* Como garantir **proporcionalidade e coerência** em modelos matemáticos
* Como criar uma aplicação **interativa de Machine Learning**
* Como usar o **Poetry** para gerenciar um projeto Python de forma profissional

---

## ✨ Autora

**Marina Kally**
📍 Desenvolvido com foco em aprendizado e prática de Machine Learning aplicado a casos reais.
🔗 [LinkedIn](https://www.linkedin.com/in/marina-kally-695535252)




