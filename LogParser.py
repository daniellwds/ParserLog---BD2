#http://www.cs.sjsu.edu/faculty/pollett/157b.12.05s/Lec20042005.pdf
#Ler o slide 8 sobre checkpoints em REDO LOG

import os
os.system('cls' if os.name == 'nt' else 'clear')

def parser(log):
    variaveis = {}
    checkpoints = []

    #define as variáveis
    for i in log[0].split():
        if i != '|':
            variaveis[i.split('=')[0]] = i.split('=')[1]

    log.pop(0) #remove a linha das variaveis do log

    print('Valor inicial das variaveis:')
    print(variaveis)

    #define os checkpoints que são inicializados e finalizados
    checkpoints = ckpt_finalizados(log)

    #percorre o log para fazer o redo
    for i in log:
        #se achar o commit da transação, faz o redo dessa transação
        #no caso, atualiza o valor das variáveis finais
        if 'commit' in i:
            lista = i.split()
            lista.pop(0)
            atual = lista[0].split('>')[0]
            
            for j in log:
                if 'write ' + atual in j:
                    lista = j.split()
                    lista = lista[1].split('>')
                    lista = lista[0].split(',')
                    variaveis[lista[1]] = lista[2]

        #se achar escrita de variaveis que estão em transações dentro de checkpoints    
        if checkpoints:
            if 'write' in i:
                lista = i.split()
                lista = lista[1].split('>')
                lista = lista[0].split(',')
                if lista[0] in checkpoints:
                    variaveis[lista[1]] = lista[2]

    print('\nValor final das variaveis:')       
    print(variaveis)

def ckpt_finalizados(log):
    chkpt = []
    retorno = []
    
    for i in log:
        if 'start CKPT' in i:
            lista = i.split('(')
            lista = lista[1].split(')')
            lista.pop(1)
            lista = lista[0].split(',')
            for j in lista:
                chkpt.append(j)
            
        if 'END CKPT' in i:
            retorno = chkpt
    
    return retorno


log1 = open("teste1", "r")
log1String = log1.read() #transforma em string
log1Lista = log1String.split('\n') #quebra sprint em linhas
print("REDO DO TESTE1 \n")
parser(log1Lista)

log2 = open("teste2", "r")
log2String = log2.read()
log2Lista = log2String.split('\n')
print("\nREDO DO TESTE2 \n")
parser(log2Lista)