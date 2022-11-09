import datetime
import APIs
import db_query
import bot_telegran
import time
from datetime import datetime, timedelta, date
import re
global points
contagen = 0
date_now = (datetime.now())
maior_valor = 0

# funçao que retorna ha hora que o processo ira parar somado a hora do evento
def hora_final(p_hora_evento):
    while True:
        print('Digite o número limite de horas que o processo ficara ativo no intervalo de 1 a 10 horas: ')
        opcao_data = input()
        res = re.match("^[1-9]$|10$", opcao_data)
        if res!= None:
            hora = res.string
            hora_evento = datetime.strptime(p_hora_evento, '%H:%M')
            hora_final = hora_evento + timedelta(hours=float(hora))
            return hora_final.strftime("%H:%M")
        else:
            print("\nDigite um valor valido entre 1 e 10\n")

#função que retorna a matricula do grupo de cartão selecionado
def grupCard_matri():
    while True:
        print('Digite o número da opção do grupo de cartões a ser verificado:\n'
              '(1) para Grupo-Card1 | (2) para Grupo-Card2 | (3) para Grupo-Card3 | (4) para Grupo-Card4 | (5) para Grupo-Card5 : ')
        grupo_card = input()
        res = re.match('^[1-5]$', grupo_card)
        if res!= None:
            switcher = {
                '1': '3225853398',  # Grupo_card 1 152953
                '2': '3226166457',  # Grupo_card 2 152955
                '3': '3226072457',  # Grupo_card 3 152954
                '4': '3226260457',  # Grupo_card 4 152956
                '5': '3226369457',  # Grupo_card 5 152957
            }
            return switcher.get(str(grupo_card))
        else:
            print("\nDigite uma opção valida\n")

#função que retorna o id  do grupo de cartão com base na matricula
def grupCard_id(p_matricula):
    switcher = {
        '3225853398': '152953',  # Grupo_card 1 matricula 3225853398 : id Grupo_card '152953'
        '3226166457': '152955',  # Grupo_card 2 matricula 3226166457 : id Grupo_card '152955'
        '3226072457': '152954',  # Grupo_card 3 matricula 3226072457 : id Grupo_card '152953'
        '3226260457': '152956',  # Grupo_card 4 matricula 3226260457 : id Grupo_card '152954'
        '3226369457': '152957',  # Grupo_card 5 matricula 3226369457 : id Grupo_card '152957'
    }
    return switcher.get(str(p_matricula))

#função que retorna o nome do grupo de cartão com base na matricula

def nome_grupo(p_matricula):
    switcher = {
        '3225853398': 'Grupo_card 1',
        '3226166457': 'Grupo_card 2',
        '3226072457': 'Grupo_card 3',
        '3226260457': 'Grupo_card 4',
        '3226369457': 'Grupo_card 5',
    }
    return str(switcher.get(str(p_matricula)))

#função que retorna o boby atualizado  com id do grupo de cartões selecionado posteriormente

def update_body(grupo_card_id):
    boby = {
        "personId": "000000",
        "orgIndexCode": "88"
    }
    boby.update({"personId": str(grupo_card_id)})
    return boby



def consultar_acessos_card_DB():
    conecao_db = db_query.conexao()
    if (conecao_db != False):
        consulta_card = db_query.consulta_card(card_grupo_matri, data_inicio)
        consulta_card = re.sub('[^0-9]', '', consulta_card)
        return consulta_card
    else:
        mgs = 'falha ao executar consulta no banco de dados!'
        bot_telegran.send_message(msg=mgs)
        return False

def limimando_acesso_card():
    acessos_card = int(consultar_acessos_card_DB())
    print("Acessos: "+str(acessos_card))
    limiti = limite_acessos
    global maior_valor
    if acessos_card >= maior_valor:
        maior_valor = acessos_card
    if acessos_card >= limiti:
        return True
    else:
        return False

def bloquear_card(p_body, p_nome_grupo):
        coneccao_api = APIs.connect_api()
        if coneccao_api == True:
            print('Conexão API ok')
            mover_card = APIs.update_person(boby=p_body)
            if mover_card == 'Success':
                print(p_nome_grupo+' movido com sucesso ao grupo card sem acesso')
                aplicar_alteracao = APIs.applay_person()
                if aplicar_alteracao == 'Success':
                    print('Aplicação do bloqueio nos dispositivos realizada com sucesso')
                    mgs = p_nome_grupo+' bloqueado com sucesso!'
                    bot_telegran.send_message(msg=mgs)

                else:
                    mgs = 'Aplicação do bloqueio nos dispositivos falhou'
                    bot_telegran.send_message(msg=mgs)
                    print('Alteração não foi aplicada')

            else:
                mgs = 'Falha ao mover grupo de acesso do '+ p_nome_grupo
                bot_telegran.send_message(msg=mgs)
                print('erro ao mover porson card')
                return False
        else:
            mgs = 'Falha de comunicação com a API!'
            bot_telegran.send_message(msg=mgs)
            print('não foi posssivel se comunicar com a api')
            return False



card_grupo_matri = grupCard_matri()
card_grupo_id = grupCard_id(p_matricula=card_grupo_matri)
card_grupo_name = nome_grupo(p_matricula=card_grupo_matri)
body = update_body(grupo_card_id=card_grupo_id)
limite_acessos = int(input ('Entre com limite de acessos dos cartões: '))
while True:
    try:
        hora_evento = str(input('Entre com horario(no formato = HH:mm) do inicio do evento: '))
        dia_d = int(input('Em quantos dias é o evento: '))
        ultimo_horario = hora_final(p_hora_evento=hora_evento)
        date_evento = (datetime.now() + timedelta(days=dia_d))
        break
    except:
        print("\nHora ou dia esta no formato errado\n")

intervalo_repeticao = int(input('Entre com valor de quanto em quanto tempo o scritp de contagem sera executado: '))

date_hora_evento = date_evento.strftime("%Y-%m-%d ") + hora_evento + datetime.now().strftime(":%S.%f")
date_hora_evento = datetime.strptime(date_hora_evento, '%Y-%m-%d %H:%M:%S.%f')
data_inicio = date_hora_evento
dif = (date_hora_evento - date_now).total_seconds()
esprerar = (date_hora_evento - date_now)
start = True

print('conexão  API:'+ str(APIs.connect_api()))
print('conexão  API:'+ str(db_query.conexao())+'\n')
print('Processo em execução...\n')

try:

    while True:
        if datetime.now().date() >= date_evento.date():
            cont_acessos = str (consultar_acessos_card_DB())
            if datetime.now().strftime("%H:%M") != ultimo_horario and datetime.now().strftime("%H:%M") >= hora_evento:
                if start:
                    mgs = 'Processo de verificação de bloqueio do ('\
                          +card_grupo_name+') iniciado '
                    bot_telegran.send_message(msg=mgs)
                start = False
                if limimando_acesso_card():
                    print('Nùmero de acessos atingido')
                    mgs = card_grupo_name+' atingiu o limite de acesso '\
                          'Acesos totais ='+cont_acessos+'\n'\
                          'processo de bloqueio iniciado:'
                    bot_telegran.send_message(msg=mgs)
                    bloquear_card(p_body=body)
                    break
                else:
                    print("Processo de contagem sera realizado novamente em "+str(intervalo_repeticao)+" segundos \nVerificação Nº:" + str(
                        contagen)+"\n")
                    contagen = contagen + 1
                    time.sleep(intervalo_repeticao)
            elif dif > 0:
                print('O processo ficara em espera por : '+str(esprerar))
                time.sleep(dif)
            if datetime.now().strftime("%H:%M") == ultimo_horario:
                mgs = 'Processo de bloqueio do '+card_grupo_name+' foi encerrado!\n\n ' \
                      'horário limite de execução (' + ultimo_horario + ')\n' \
                      'Acesso TOTAL de entradas = ' + str(maior_valor) + '\n'\
                      'Acesso ATUAL  = '+cont_acessos+'\n'\
                      'Saidas = '+str(maior_valor - int(cont_acessos))
                bot_telegran.send_message(msg=mgs)
                break
        elif dif > 0:
            print('O processo ficara em espera por : ' + str(esprerar))
            time.sleep(dif)

except Exception as e:
    mgs = 'Ocorreu erros ao executar,\n' \
          'o processo de verificação e bloqueio do cartão'
    bot_telegran.send_message(msg=mgs)
    print(e)
    mgs = str(e)
    bot_telegran.send_message(msg=mgs)

