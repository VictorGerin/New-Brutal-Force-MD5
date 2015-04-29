# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import random
from md5 import MD5
from sqlite import sql

__author__ = "victor"
__date__ = "$26/04/2015 06:15:38$"

class verifica(object):

    caracteresAUsar = ''
    
    numeroMaxParaAcresentar = 3
    
    quantidadeDeFilhos = 10000

    tamanhoMaxDoFilho = 6
    tamanhoMinDoFilho = 6

    @classmethod
    def geraFilho(cls, md5):
        k = md5.key
        if cls.tamanhoMinDoFilho == cls.tamanhoMaxDoFilho:
            return cls.geraFilhoMantendoOTamanho(md5)
        a = random.randint(0, len(k))
        if len(k) - a < cls.tamanhoMinDoFilho:
           a = len(k) - cls.tamanhoMinDoFilho
        if a > 0:
            while a > 0:
                pos = random.randint(0, len(k) - 1)
                k = k[:pos] + k[pos+1:]
                a -= 1
        a = random.randint(0, cls.numeroMaxParaAcresentar)
        if a + len(k) > cls.tamanhoMaxDoFilho:
            a = cls.tamanhoMaxDoFilho - len(k)
        if a > 0:
            while a > 0:
                if len(k) == 0:
                    k = cls.pegaCaractere()
                    continue
                pos = random.randint(0, len(k))
                k = k[0:pos:] + cls.pegaCaractere() + k[pos:]
                a -= 1
        return MD5(k)

    @classmethod
    def geraFilhoMantendoOTamanho(cls, md5):
        k = md5.key
        aFixo = random.randint(1, len(k))
        a = aFixo
        while a > 0:
            pos = random.randint(0, len(k) - 1)
            k = k[:pos] + k[pos+1:]
            a -= 1
        a = aFixo
        while a > 0:
            if len(k) == 0:
                k = cls.pegaCaractere()
                continue
            pos = random.randint(1, len(k) + 1)
            k = k[0:pos:] + cls.pegaCaractere() + k[pos:]
            a -= 1
        return MD5(k)



    @classmethod
    def geraFilhos(cls, md5):
        import sqlite3
        filhos = []
        filhos.append(md5)
        numeroDeErradosGerados = 0
        quantidade = cls.quantidadeDeFilhos
        while len(filhos) < quantidade:
            md = cls.geraFilho(md5)
#            if md in filhos:
#                continue
            try:
                sql.addDataBase(md)
            except sqlite3.IntegrityError, err:
                numeroDeErradosGerados += 1
                if numeroDeErradosGerados >= cls.quantidadeDeFilhos * 10:
                    quantidade -= 1
                    numeroDeErradosGerados = 0
                continue
            filhos.append(md)
#            numeroDeErradosGerados = 0
        return filhos
    
    @classmethod
    def pegaOMaisParecido(cls, key, filhos):
        parentesco = -1
        md5Key = MD5(key).calc()
        levenshteinDuploNoEspecial = len(key) + 1
        especial = None
        for filho in filhos:
            i = cls.levenshtein(key, filho.calc())
            if parentesco == -1 or i < parentesco:
                parentesco = i
                especial = filho
            elif i == parentesco:
                i2 = cls.levenshtein(md5Key , MD5(filho.calc()).calc())
                if levenshteinDuploNoEspecial > i2:
                    levenshteinDuploNoEspecial = cls.levenshtein(md5Key , MD5(especial.calc()).calc())
                    parentesco = i
                    especial = filho
                
        return especial
    
    @classmethod
    def geraRandomSeed(cls):
        size = random.randint(cls.tamanhoMinDoFilho, cls.tamanhoMaxDoFilho)
        Seed = ''
        while len(Seed) < size:
            Seed += cls.pegaCaractere()
        Seed = MD5(Seed)
        try:
            sql.addDataBase(Seed)
        except lite.IntegrityError, err:
            return cls.geraRandomSeed()
        return Seed

    @classmethod
    def pegaCaractere(cls):
        a = random.randint(0, len(cls.caracteresAUsar))
        return cls.caracteresAUsar[a:a+1:1]
    
    @classmethod
    def levenshtein(self,s1, s2):
        if len(s1) < len(s2):
            return levenshtein(s2, s1)
        
    # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)
    
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1       # than s2
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]
