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
outros_cars = False


# funçao que retorna ha hora que o processo ira parar somado a hora do evento
def hora_final(p_hora_evento):
    while True:
        print('Digite o número limite de horas que o processo ficara ativo no intervalo de 1 a 10 horas: ')
        opcao_data = input()
        res = re.match("^[1-9]$|10$", opcao_data)
        if res is not None:
            hora = res.string
            hora_evento = datetime.strptime(p_hora_evento, '%H:%M')
            hora_final = hora_evento + timedelta(hours=float(hora))
            return hora_final.strftime("%H:%M")
        else:
            print("\nDigite um valor valido entre 1 e 10\n")


# função que retorna a matricula do grupo de cartão selecionado
def grupCard_matri():
    global outros_cars
    while True:
        grupo_card = input('\nDigite o número da opção do grupo de cartões a ser verificado:\n'
              '(1) para Grupo-Card1 | (2) para Grupo-Card2 | (3) para Grupo-Card3 | (4) para Grupo-Card4 | (5) para Grupo-Card5 : (6) para outros cartões :')
        res = re.match('^[1-5]$', grupo_card)
        if res is not None:
            switcher = {
                '1': 'GRUP CARD 1 Convidados',
                '2': 'GRUP CARD 2 Convidados',
                '3': 'GRUP CARD 3 Convidados',
                '4': 'GRUP CARD 4 Convidados',
                '5': 'GRUP CARD 5 Convidados',
            }
            return switcher.get(str(grupo_card))
        elif grupo_card == '6':
            nome_card = input('\nEscreva o nome do cartão:')
            if nome_card != '':
                result = APIs.search_person(nome_card)
                if result:
                    print(f'Nome Card Group: {result[2]}\n')
                    return
                else:
                    print('Não foi encontardo o cartão\n')
            else:
                print("Nome do cartão não pode estar em branco\n")



def update_body(grupo_card_id):
    boby = {
        "personId": "000000",
        "orgIndexCode": "29"
    }
    boby.update({"personId": str(grupo_card_id)})
    return boby


def consultar_acessos_card_DB(p_card_grupo_matri):
    conecao_db = db_query.conexao()
    if conecao_db is not False:
        consulta_card = db_query.consulta_card(p_card_grupo_matri, data_inicio)
        consulta_card = re.sub('[^0-9]', '', consulta_card)
        return consulta_card
    else:
        megs = 'falha ao executar consulta no banco de dados!'
        bot_telegran.send_message(msg=megs)
        return False


def limimando_acesso_card(p_matri):
    acessos_card = int(consultar_acessos_card_DB(p_card_grupo_matri=p_matri))
    print("Acessos: " + str(acessos_card))
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
    if coneccao_api:
        print('Conexão API ok')
        mover_card = APIs.update_person(boby=p_body)
        if mover_card == 'Success':
            print(p_nome_grupo + ' movido com sucesso ao grupo card sem acesso')
            aplicar_alteracao = APIs.applay_person()
            if aplicar_alteracao == 'Success':
                print('Aplicação do bloqueio nos dispositivos realizada com sucesso')
                megs = p_nome_grupo + ' bloqueado com sucesso!'
                bot_telegran.send_message(msg=megs)

            else:
                megs = 'Aplicação do bloqueio nos dispositivos falhou'
                bot_telegran.send_message(msg=megs)
                print('Alteração não foi aplicada')

        else:
            megs = 'Falha ao mover grupo de acesso do ' + p_nome_grupo
            bot_telegran.send_message(msg=megs)
            print('erro ao mover porson card')
            return False
    else:
        megs = 'Falha de comunicação com a API!'
        bot_telegran.send_message(msg=megs)
        print('não foi posssivel se comunicar com a api')
        return False


card_grupo_info_name = grupCard_matri()
card_grupo_id, card_grupo_matri, card_grupo_name = APIs.search_person(card_grupo_info_name)
print(card_grupo_id,card_grupo_matri,card_grupo_name)
body = update_body(card_grupo_id)

limite_acessos = int(input('Entre com limite de acessos dos cartões: '))
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

try:
    print(f'conexão  API: {APIs.connect_api()}')
    print(f'conexão  DB: {db_query.conexao()}')
    print('Processo em execução...\n')
    while True:
        if datetime.now().date() >= date_evento.date():
            cont_acessos = str(consultar_acessos_card_DB(p_card_grupo_matri=card_grupo_matri))
            if datetime.now().strftime("%H:%M") != ultimo_horario and datetime.now().strftime("%H:%M") >= hora_evento:
                if start:
                    mgs = f'Processo de verificação de bloqueio do ({card_grupo_name}) iniciado'
                    bot_telegran.send_message(msg=mgs)
                start = False
                if limimando_acesso_card(p_matri=card_grupo_matri):
                    print('Nùmero de acessos atingido')
                    mgs = f'{card_grupo_name} atingiu o limite de acesso Acesos totais = {cont_acessos} \n processo de bloqueio iniciado:'
                    bot_telegran.send_message(msg=mgs)
                    bloquear_card(p_body=body, p_nome_grupo=card_grupo_name)
                    break
                else:
                    print(f"Processo de contagem sera realizado novamente em {intervalo_repeticao} segundos \n"
                          f"Verificação Nº: {contagen}\n")
                    contagen = contagen + 1
                    time.sleep(intervalo_repeticao)
            elif dif > 0:
                print(f'O processo ficara em espera por : {esprerar}')
                time.sleep(dif)
            if datetime.now().strftime("%H:%M") == ultimo_horario:
                mgs = f'Processo de bloqueio do {card_grupo_name} foi encerrado!\n ' \
                      f'horário limite de execução ({ultimo_horario})\n' \
                    f'Acesso TOTAL de entradas = ({maior_valor}) + \n' \
                    f'Acesso ATUAL  = {cont_acessos }\n' \
                    f'Saidas = {maior_valor - int(cont_acessos)}'
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

print('fim...')
