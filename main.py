# Importando as bibliotecas
import time
import requests
import json
import telegram
import telebot

ultimos_resultados = []
check_resultados = []

dados = []


# função par puxar os dados da roledta
def puxar_dados():
    global ultimos_resultados
    # Faz uma requisição GET para o url especifico
    resposta = requests.get(url, headers=headers)
    dic_resposta = resposta.json()
    dados = dic_resposta['gameTables']
    for i in dados:
        roletas = i['gameTableId']
        # puxando os ultimos resultados apenas da roleta brasileira
        if '103910' in roletas:
            chaves = i.keys()
            if 'lastNumbers' in chaves:
                ultimos_resultados = i['lastNumbers']
    return ultimos_resultados


# função para obter os vizinhos esquerdo e direito de um numero
def obter_vizinhos(ultimos_resultados):
    # Lista numero na roda europeia
    numeros_da_roda = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14,
                       31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
    # encontra a posição do numero na lista
    for numero in ultimos_resultados:
        numero = int(numero)
        indice_numero = numeros_da_roda.index(numero)

        # obtem os vizinhos esquerda e direita
        vizinho_esquerdo = numeros_da_roda[(indice_numero - 2) % 37]
        vizinho_esquerdo1 = numeros_da_roda[(indice_numero - 1) % 37]
        vizinho_direito = numeros_da_roda[(indice_numero + 1) % 37]
        vizinho_direito1 = numeros_da_roda[(indice_numero + 2) % 37]
    return [vizinho_esquerdo, vizinho_esquerdo1, vizinho_direito, vizinho_direito1]


# função para analizar um numero
def analisar_numero(ultimos_resultados):
    caracteristicas = []
    for numero in ultimos_resultados:
        try:
            numero = int(numero)
        except ValueError:
            return "Erro: o valor de entrada deve ser um numero inteiro"

        paridade = 'par' if numero % 2 == 0 else 'ímpar'
        cor = 'vermelho' if numero in (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23,25,27, 30, 32, 34, 36) else 'preto'
        #elif numero in (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35):

        duzia = 1 if numero in range(1, 13) else 2 if numero in range(13, 25) else 3 if numero in range(25, 37) else 0
        coluna = 1 if numero in range(1, 35, 3) else 2 if numero in range(2, 36, 3) else 3 if numero in range(3, 37, 3) else 0
        numeros_terminal = [i for i in range(0, 37) if int(str(i)[-1]) == int(str(numero)[-1])]
        vizinhos = obter_vizinhos(ultimos_resultados)
        caracteristicas.append(
            {'numero': numero, 'coluna': coluna, 'duzia': duzia, 'paridade': paridade, 'cor': cor, 'vizinhos': vizinhos,
             'numeros_terminal': numeros_terminal})
    dados.append(caracteristicas)
    return caracteristicas


def create_message(indicacao, ultimo_numero, emensagem ):
    alerta = f'''⚠️ENTRADA CONFIRMADA - ROLETA BRASILEIRA
    🖥ACESSE:: http://abrir.link/L83BV/
    🎯Estratégia: {indicacao}    
    ✅Entrar: {emensagem}
    👍🏻Entrar após: {ultimo_numero}
    COBRIR O ZERO 🟢
    🚨Aplicar até 2 gales'''
    enviar_alerta(alerta)
    return alerta


def enviar_alerta(alerta):
    token = '6939716089:AAGvR9FV143qEyl42JF845v200Cdjk2gC9M'
    chat_id = '-1002039685069'
    bot = telebot.TeleBot(token=token)
    bot.send_message(chat_id=chat_id, text=alerta, disable_web_page_preview = True)#, parse_mode=telegram.ParseMode.HTML)



def enviar_e_apagar_msg():
    token = '6939716089:AAGvR9FV143qEyl42JF845v200Cdjk2gC9M'
    chat_id = '-1002039685069'
    bot = telebot.TeleBot(token=token)#telegram.Bot(token=token)
    text = f'''⚠️🚨️Atenção: Possivel entrada!
    👉🏻Entre no jogo e aguarde a confiramação!⚠⚠🚨️
    🚀Site: https://bit.ly/rolet-brasileria'''
    mensagem = bot.send_message(chat_id=chat_id, text=text, disable_web_page_preview = True)
    time.sleep(3)
    disable_web_page_preview = True
    bot.delete_message(chat_id=chat_id, message_id=mensagem.message_id)



# função para executar estratégias
def estrategias():
    global dados
    dados = dados[0]

    try:
        # estrategia de repetição de caracteristicas 1 e 2
        numero1 = dados[0]['numero']
        numero2 = dados[1]['numero']
        numero3 = dados[2]['numero']

        coluna1 = dados[0]['coluna']
        coluna2 = dados[1]['coluna']
        coluna3 = dados[2]['coluna']
        if coluna1 == 1:  #!= (2) and (3):
            mensagem1 = f'ENTRAR NA 2º e 3º COLUNAS'
        elif coluna1 == 2: #!= (1) and (3):
             mensagem1 = f'ENTRAR NA 1º e 3º COLUNAS'
        else:
             coluna1 == 3 #!= (1) and (2)
             mensagem1 = f'ENTRAR NA na 1º e 2º COLUNAS'
        if coluna1 == coluna2 == coluna3:
            indicacao = f'Quebra de repetição de coluna {coluna1}'
            emensagem = mensagem1
            ultimo_numero = f'{numero1}'
            create_message(indicacao, ultimo_numero, emensagem)

        duzia1 = dados[0]['duzia']
        duzia2 = dados[1]['duzia']
        duzia3 = dados[2]['duzia']
        if duzia1 == 1: #!= (2) and (3):
            mensagem1 = f'ENTRAR NA 2º e 3º DÚZIAS'
        elif duzia1 == 2: #!= (1) and (3):
             mensagem1 = f'ENTRAR NA 1º e 3º DÚZIAS'
        else:
            duzia1 == 3 #!= (1) and (2)
            mensagem1 = f'ENTRAR NA 1º e 2º DÚZIAS'
        if duzia1 == duzia2 == duzia3:
            indicacao = f'Quebra de repetição de duzia {duzia1}'
            emensagem = mensagem1
            ultimo_numero = f'{numero1}'
            create_message(indicacao, ultimo_numero, emensagem)

        cor1 = dados[0]['cor']
        cor2 = dados[1]['cor']
        cor3 = dados[2]['cor']
        cor4 = dados[3]['cor']
        if cor1 == cor2 == cor3 == cor4:
            indicacao = f'Quebra da repeticao de cor {cor1}'
            emensagem = f''
            ultimo_numero = f'{numero1}'
            create_message(indicacao, ultimo_numero, emensagem)


        else:
            pass

    except:
        raise Exception("erro")


url = "https://casino.betfair.com/api/tables-details"
headers = {"cookie": "vid=8ab7daa7-57f7-4196-8285-943390594163"}


while True:
    dados.clear()
    puxar_dados()

    if ultimos_resultados != check_resultados:
        #enviar_e_apagar_msg()
        check_resultados = ultimos_resultados
        caracteristicas = analisar_numero(ultimos_resultados)
        estrategias()
        print(ultimos_resultados)
        print(dados[0])
        print(dados[1])
        print(dados[2])
    time.sleep(5)















