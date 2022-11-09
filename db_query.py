from datetime import datetime, timedelta, date
import pyodbc
import re
import os
from dotenv import load_dotenv
load_dotenv()
# Função de retornar a conexão

def conexao():
    HOST = os.getenv('HOST') # or "domain.com"
    # database name, if you want just to connect to MySQL server, leave it empty
    DATABASE = os.getenv('DATABASE')
    # this is the user you create
    USER = os.getenv('USER')
    # user password
    PASSWORD = os.getenv('PASSWORD')
    try:
        string_conexao = 'Driver={SQL Server Native Client 11.0};Server=' + HOST + ';Database=' + DATABASE + ';UID=' + USER + ';PWD=' + PASSWORD
        # string_conexao = 'Driver={SQL Server Native Client 11.0};Server='+HOST+';Database='+DATABASE+';Trusted_Connection=yes;'
        conection = pyodbc.connect(string_conexao)
        return conection.cursor()
    except:
        return False


# Função de retornar valor acesso card
def consulta_card(p_matri, p_data_inicio):
    data_inicial = p_data_inicio
    data_final = (data_inicial + timedelta(1))
    data_inicial = data_inicial.strftime("%Y-%m-%d") #FORMATO DATA '2022-06-25'
    data_final = data_final.strftime("%Y-%m-%d")
    cursor = conexao()
    sql = "SELECT ((SELECT COUNT(MATR)AS quantidade FROM dbo.EVENTOS WHERE DATA >= '" + data_inicial + \
          "' AND DATA <= '" + data_final + "' AND MATR = '" + str(p_matri) + \
          "' AND LEITOR_NOME LIKE '%Entrada%')" \
          + "- (SELECT COUNT(MATR)AS quantidade FROM dbo.EVENTOS WHERE DATA >= '" + data_inicial +\
          "' AND DATA <= '" + data_final + "' AND MATR = '" + str(p_matri) + \
          "' AND LEITOR_NOME LIKE '%SAIDA%')) AS TOTAL;"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row:
        return str(row)
