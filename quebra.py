# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from md5 import MD5
from sqlite import sql
from Algoritimo import verifica
import argparse
import string
import os.path

__author__ = "victor"
__date__ = "$26/04/2015 05:38:0$"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Programa para quebrar HASHs usando algoritimo genetico, eu sei eu sei ... isso parece mais um brutal force um pouco mais lento se voce concorda com isso me mande um email para como deixar mais rapido :)',
        epilog='Author : Victor Gerin de Lacerda, Email : gerinlacerda@gmail.com'
    )
    parser.add_argument('hash', help='MD5 a tentar quebrar')
    parser.add_argument('-min', dest='min', default=1, type=int, help='Tamanho minimo que uma senha gerada pode ter')
    parser.add_argument('-max', dest='max', default=10, type=int, help='Tamanho maximo que uma senha gerada pode ter')
    parser.add_argument('-fixSize', default=0, type=int, help='Fixar o tamnho das senhas geradas')
    parser.add_argument('-seed', dest='seed' , default=None, help='Pai de todas as senhas geradas')
    parser.add_argument('-filhos', default=10000, type=int, help='Numero de filhos esperado por geracao')
    parser.add_argument('-genMax', default=10, type=int, help='Numero maximo de geracoes que um pai pode ter antes de ser descartado')
    parser.add_argument('-genMaxEspecial', default=100, type=int, help='Quando uma senha e considereda especial por seu alto valor de semelhanca entao o numero maximo de geracoes deve ser maior antes dele ser descartado')
    parser.add_argument('-numCommit -num', dest='numCommit', default=-1, type=int, help='Numero de filhos gerados antes de fazer o commit para o banco de dados')
    parser.add_argument('-getDbToMemory -get', dest='getDbToMemory', help='Pega o banco de dados e copia para a memoria podendo almentar a velocidade')
    parser.add_argument('-useSeomenteSeed', action='store_true', help='Usar somente a primeira seed ou a seed passada como pai')
    parser.add_argument('-addChar', default=3, type=int, help='Numero maximo de caracteres adicionado numa senha filho')
    parser.add_argument('-pula', action='store_true' ,help='Puta a verificacao com o banco de dados')
    parser.add_argument('-db', default=':memory:', help='Seta o banco de dados para armazenar as senhas, default = :memory:')
    parser.add_argument('-n', action='store_true', help='Seta para procurar usando numeros')
    parser.add_argument('-l', action='store_true', help='Seta para procurar usando letra minuscula')
    parser.add_argument('-L', action='store_true', help='Seta para procurar usando letra maiuscula')
    parser.add_argument('-e', action='store_true', help='Seta para procurar usando caracteres de pontuacao')

    args = parser.parse_args()
#Seta a lista de caracteres que sera usado nos filhos e nas geracoes
    if args.n or (not args.l and not args.L and not args.e):
        verifica.caracteresAUsar += string.digits
    if args.l:
        verifica.caracteresAUsar += string.ascii_lowercase
    if args.L:
        verifica.caracteresAUsar += string.ascii_uppercase
    if args.e:
        verifica.caracteresAUsar += string.punctuation
#Seta o valor padrao para o numero de chaves encontradas antes de dar commit
    if args.numCommit == -1:
        args.numCommit = 5 * args.filhos

#Seta algumas variaveis que o usuario passou
    hashAverificar = args.hash
    verifica.quantidadeDeFilhos = args.filhos
    if args.fixSize:
        args.max = args.min = args.fixSize
    verifica.tamanhoMaxDoFilho = args.max
    verifica.tamanhoMinDoFilho = args.min
    verifica.numeroMaxParaAcresentar = args.addChar
    try:
#inicializa o banco de dados padrao e na memoria mas ele pode ser usado direto no hd
        if not args.getDbToMemory:
            sql.getDbToMemory = args.getDbToMemory
            sql.startCon(args.db)
        else:
            sql.getDbToMemory = args.getDbToMemory
            sql.startCon(':memory:')
            sql.loadFrom(args.getDbToMemory)
#seta o numero de insert antes de dar commit
        sql.numInsertToCommit = args.numCommit
#cria as tabelas caso elas nao existam
        sql.createTables()
        print 'procurando no banco de dados se ja existe'
#procura no banco se a hash passada ja nao consta la
        row = sql.verificaKey(hashAverificar)
        if row:
            print 'Chave encontrada :', row
            sql.close()
            exit()

        print 'a procura nao retornou resultado ...'
        print 'iniciando algoritimo'

#Variaveis usadas no codigo
        init = MD5(args.seed) if args.seed else verifica.geraRandomSeed() #Melhor filho encontrado ou valor inicial
        count = 0 #Contagem da geracao atual do filho atual
        atual = None #Filho Atual
        proximidadeMaxAlcancada = 0 #Valor mais proximo alcansado do objetivo
        #100% de proximidade significa que os dois hash sao iguais e por tanto a senha foi encontrada
        ultimaQuantidade = 0 #Quantidade de filhos ja percorrido ate o ultimo commit
        atualQuantidade = 0

        printTemplate = '{:^34}|{:^34}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|'
        def printHeader():
            _40 = '{:-^34}'.format('')
            _10 = '{:-^10}'.format('')
            print printTemplate.format(_40, _40, _10, _10, _10, _10, _10)
            print printTemplate.format('Goal', 'Atual', 'Prox', 'Filho', 'Pai', 'Esper.', 'Conseg.')
            print printTemplate.format(_40, _40, _10, _10, _10, _10, _10)

        def exitCode():
            print '\n\rfinalizando ... '
            sql.close()
            print 'bye bye'
            exit()

        seedPai = init

        printHeader()
        while proximidadeMaxAlcancada < 1.0:
            filhos = verifica.geraFilhos(init)
            atualQuantidade += len(filhos)
            pai = init
            init = verifica.pegaOMaisParecido(hashAverificar, filhos)
            levenshtein = verifica.levenshtein(hashAverificar, init.calc())
            proximidade = (1.0 - (levenshtein / float(len(init.calc()))))
            print printTemplate.format(hashAverificar, 
                                       init.calc(), 
                                       '{:.2%}'.format(proximidade), 
                                       init.key, 
                                       pai.key, 
                                       '{:d}'.format(verifica.quantidadeDeFilhos), 
                                       '{:d}'.format(len(filhos))
                                      )
            if (atualQuantidade - ultimaQuantidade) / args.numCommit:
                ultimaQuantidade = atualQuantidade
                printHeader()
            if not atual or atual == init:
                count += 1
            else:
                count = 0
            if count >= args.genMax and proximidadeMaxAlcancada > proximidade and not args.useSeomenteSeed:
                init = verifica.geraRandomSeed()
            elif count >= args.genMaxEspecial and proximidadeMaxAlcancada <= proximidade and not args.useSeomenteSeed:
                init = verifica.geraRandomSeed()
            if proximidadeMaxAlcancada <= proximidade:
                proximidadeMaxAlcancada = proximidade
            if args.useSeomenteSeed:
                init = seedPai
            atual = init
        else :
            exitCode()
    except KeyboardInterrupt:
        exitCode()
