import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go

def convertFrequencyToMonth(frequence, salary):
    if frequence == 'Yearly':
        return (salary / 12)
    elif frequence == 'Weekly':
        return (salary * 4) 
    elif frequence == 'Monthly':
        return salary    
    else:
      return None

schema = pd.read_csv('survey_results_schema.csv')   
dados = pd.read_csv('survey_results_public.csv')

df = pd.DataFrame(dados)

st.title('Trabalho Prático 2 - Streamlit - Python para Ciência de Dados')
"""
##
Felipe Jonata Oliveira França
"""

st.header(""" 1 - Porcentagem das pessoas que responderam que se consideram profissionais, não profissionais, estudante, hobby, ....""") 
qtd = dados['MainBranch'].value_counts()
total = len(dados['MainBranch'])
percent = (qtd / total) * 100 
percent = percent.map(lambda n: '{0:.2f}%'.format(n))
percent

st.markdown("""---""")
st.header(""" 2 - Distribuição das pessoas que responderam por localidade. Qual o país que teve maior participação?""") 
countrys = dados['Country'].value_counts()
countrys_total = len(dados['Country'])
percent_countrys = (countrys / countrys_total) * 100
percent_countrys = percent_countrys.map(lambda n: '{0:.2f}%'.format(n))
percent_countrys
countrys
st.write("""**O país com maior participação foi os EUA com 15288 participações seguido da India com 10511 e o Brasil contou com 2254 participações**""") 
st.markdown("""---""")

st.header(""" 3 - Qual a distribuição nível de estudo dos participantes?""") 
EdLevel = dados['EdLevel'].value_counts()
EdLevel_total = len(dados['EdLevel'])
EdLevel_percent = (EdLevel / EdLevel_total) * 100
EdLevel_percent = EdLevel_percent.map(lambda n: '{0:.2f}%'.format(n))
EdLevel_percent
st.markdown("""---""")


st.header(""" 4 - Qual a distribução de tempo de trabalho para cada tipo de profissional respondido na questão 1. ?""") 
selecao = (
        (dados['MainBranch'] == 'I am a developer by profession') | 
        (dados['MainBranch'] == 'I am a student who is learning to code') |
        (dados['MainBranch'] == 'I am not primarily a developer, but I write code sometimes as part of my work') |
        (dados['MainBranch'] == 'I code primarily as a hobby') |
        (dados['MainBranch'] == 'I used to be a developer by profession, but no longer am') |
        (dados['MainBranch'] == 'None of these')
) 
df1 = dados[selecao]
df_filtrado = df1[['MainBranch','YearsCodePro']]
df_filtrado.dropna(inplace=True)
df_filtrado['YearsCodePro'].replace(to_replace="Less than 1 year", value='1', inplace=True)
df_filtrado['YearsCodePro'].replace(to_replace="More than 50 years", value='51', inplace=True)
df_filtrado['YearsCodePro'] = df_filtrado['YearsCodePro'].astype(int)
df_result = df_filtrado.groupby(['MainBranch']).mean()
df_result

st.markdown("""---""")


st.header(""" 5 - Das pessoas que trabalham profissionalmente: """) 
st.subheader(""" 5 - A - Qual a profissão delas?: """) 
selecao = (
        (dados['MainBranch'] == 'I am a developer by profession') | 
        (dados['MainBranch'] == 'I am not primarily a developer, but I write code sometimes as part of my work')     
) 
df_profissao = dados[selecao]
df_profissao['MainBranch'].unique()
qtd = df_profissao.Employment.value_counts()
total = len(df_profissao.Employment)
percent = (qtd / total) * 100
percent = percent.map(lambda n: '{0:.2f}%'.format(n))
percent

st.subheader(""" 5 - B - Qual a escolaridade?: """) 
df_escolaridade = dados[selecao]
df_escolaridade['EdLevel'].unique()
qtd = df_escolaridade['EdLevel'].value_counts()
total = len(df_escolaridade['EdLevel'])
percent = (qtd / total) * 100
percent = percent.map(lambda n: '{0:.2f}%'.format(n))
percent


st.subheader(""" 5 - C - Qual o tamanho das empresas de pessoas que trabalham profissionalmente?""") 
selecao = (
    (dados['MainBranch'] == 'I am a developer by profession')
) 
df_org_size = dados[selecao]
df_org_size['OrgSize'].value_counts()
qtd = df_org_size['OrgSize'].value_counts()
total = len(df_org_size['OrgSize'])
percent = (qtd / total) * 100
percent = percent.map(lambda n: '{0:.2f}%'.format(n))
percent
st.markdown("""---""")


st.header(""" 6 - Média salarial das pessoas que responderam?""") 
    
countrys = dados['Country'].value_counts()
selecao = np.where((dados.Country.isin(countrys.index)),True, False)
df3 = dados[selecao]
df_filtrado = df3[['Country', 'CompTotal', 'CompFreq', 'Currency']]
df_filtrado.dropna(inplace=True)
df = df_filtrado[(np.abs(stats.zscore(df_filtrado['CompTotal'])) < 3)] 
df_filtrado = df.sort_values(by='Country').reset_index(drop=True)

df_res = df_filtrado.groupby(['Country', 'Currency', 'CompFreq'])['CompTotal'].mean().reset_index()
df_res['CompTotal'] = round(df_res['CompTotal'], 2)
df_res

st.markdown("""---""")

st.header(""" 7 - Pegando os 5 países que mais responderam o questionário, qual é o salário destas pessoas?""") 
countrys = dados['Country'].value_counts()
countrys = pd.DataFrame(countrys[:5])
selecao = np.where((dados.Country.isin(countrys.index)),True, False)
df3 = dados[selecao]
df_filtrado = df3[['Country', 'CompTotal', 'CompFreq', 'Currency']]
df_filtrado.dropna(inplace=True)
df = df_filtrado[(np.abs(stats.zscore(df_filtrado['CompTotal'])) < 3)] 
df_filtrado = df.sort_values(by='Country').reset_index(drop=True)

df_res = df_filtrado.groupby(['Country', 'Currency', 'CompFreq'])['CompTotal'].mean().reset_index()
df_res['CompTotal'] = round(df_res['CompTotal'], 2)
df_res

st.markdown("""---""")


st.header(""" 8 - Qual a porcentagem das pessoas que trabalham com python?""") 
total_devs = dados[['LanguageHaveWorkedWith']].dropna()
total_devs_python = total_devs[total_devs['LanguageHaveWorkedWith'].str.contains('Python')]
percent = (len(total_devs_python) / len(total_devs)) * 100
percent = "{:.0%}".format(percent)
st.write(percent +" disseram que trabalham com Python")
st.markdown("""---""")


st.header(""" 9 - Sobre python: """) 
st.subheader(""" 9 - A - Qual o nível de salário de quem trabalha com python globalmente? """) 

df_survey = dados
df_python = df_survey[['LanguageHaveWorkedWith', 'CompFreq', 'CompTotal', 'Currency']].dropna()
df_python = df_python[df_python['LanguageHaveWorkedWith'].str.contains('Python')]
df_python = df_python[df_python['Currency'] == 'USD\tUnited States dollar']
df_python = df_python[(np.abs(stats.zscore(df_python['CompTotal'])) < 3)]
df_comp_total_converted = df_python.apply(lambda x: convertFrequencyToMonth(x.CompFreq, x.CompTotal), axis=1)
st.write("A média salarial em USD é $" + str(round(df_comp_total_converted.mean(), 2)))


st.subheader(""" 9 - B - Para o Brasil, qual o nível salarial? """) 
df_python = dados[['LanguageHaveWorkedWith', 'CompFreq', 'CompTotal', 'Country', 'Currency']].dropna()
df_python = df_python[df_python['LanguageHaveWorkedWith'].str.contains('Python')]
df_python = df_python[df_python['Country'] == 'Brazil']
df_python = df_python[df_python['Currency'] == 'BRL\tBrazilian real']
df_comp_total_converted = df_python.apply(lambda x: convertFrequencyToMonth(x.CompFreq, x.CompTotal), axis=1)
st.write("Média salarial no Brasil é R$" + str(round(df_comp_total_converted.mean(), 2)))


st.subheader(""" 9 - C - Para os 5 países que mais tiveram participação, qual a média salarial? """) 

df_geral = dados[['LanguageHaveWorkedWith', 'CompFreq', 'CompTotal', 'Country', 'Currency']].dropna()
df_geral = df_geral[df_geral['LanguageHaveWorkedWith'].str.contains('Python')]

countrys = dados['Country'].value_counts()
countrys = list(countrys[:5].index)

selecao = (
    (dados['Country'].isin(countrys))
) 
df_countrys = dados[selecao]

for country in countrys:
    df_python_country = df_geral[df_geral['Country'] == country]
    currency = ''
    if country == 'Canada':
        df_python_country = df_python_country[df_python_country['Currency'] == 'CAD\tCanadian dollar']
        currency = 'CAD'
    elif country == 'United States of America':
        df_python_country = df_python_country[df_python_country['Currency'] == 'USD\tUnited States dollar']
        currency = 'USD'
    elif country == 'India':
        df_python_country = df_python_country[df_python_country['Currency'] == 'INR\tIndian rupee']
        currency = 'INR'
    elif country == 'Germany':
        df_python_country = df_python_country[df_python_country['Currency'] == 'EUR European Euro']
        currency = 'EUR'
    else:
        df_python_country = df_python_country[df_python_country['Currency'] == 'GBP\tPound sterling']
        currency = 'GBP'
    
    result = df_python_country.apply(lambda x: convertFrequencyToMonth(x.CompFreq, x.CompTotal), axis=1)
    
    st.write("O salário médio mensal dos desenvolvedores Python no {} é {} {}".format(country,  currency, str(round(result.mean(), 2))))


st.markdown("""---""")

st.header(""" 10 - De todos as pessoas, Qual o sistema operacional utilizado por elas? """) 
qtd = dados['OpSys'].value_counts()
total = len(dados['OpSys'])
percent = (qtd / total) * 100
percent = percent.map(lambda n: '{0:.2f}%'.format(n))
percent
st.markdown("""---""")

st.header(""" 11 - Das pessoas que trabalham com python, qual a distribuição de sistema operacional utilizado por elas. """) 
df_python = dados[['LanguageHaveWorkedWith', 'OpSys']]
df_python.dropna(inplace=True)
df_python = df_python[df_python['LanguageHaveWorkedWith'].str.contains('Python')]
df_python = df_python['OpSys'].value_counts()
total = len(dados['OpSys'])
percent = (qtd / total) * 100
percent = percent.map(lambda n: '{0:.2f}%'.format(n))
percent

st.markdown("""---""")


st.header(""" 12 - Qual a média de idade das pessoas que responderam? """) 
df_age = dados[['Age']]
df = df_age.value_counts().rename_axis('Idades').reset_index(name='Totais')

fig = go.Figure(data=[go.Pie(labels=df['Idades'], values=df['Totais'], pull=[0, 0, 0.2, 0])])
st.plotly_chart(fig, use_container_width=True)

st.markdown("""---""")


st.header(""" 13 - E em python? Qual a média de idade? """) 
df_python = dados[['LanguageHaveWorkedWith','Age']].dropna()
df_python = df_python[df_python['LanguageHaveWorkedWith'].str.contains('Python')]

df_age = df_python[['Age']]
df = df_age.value_counts().rename_axis('Idades').reset_index(name='Totais')
df

fig = px.bar(df, x='Idades', y='Totais')
st.plotly_chart(fig, use_container_width=True)
