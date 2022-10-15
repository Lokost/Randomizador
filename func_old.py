# coding: UTF-8
# Arquivo: func

from io import TextIOWrapper
from json import dump, loads
import sys
from pygame import mixer
from os import listdir, remove, mkdir
from os.path import join, abspath, dirname
from fnmatch import filter
from random import choice, randint
import requests as r

def resourcePath(relative):
    base_path = getattr(sys, '_MEIPASS', dirname(abspath(__file__)))
    return join(base_path, relative)

class Func:
    dados = list()
    Completa = list()
    escolha = str()
    aux = ''
    recentes = list()
    iniciado = bool()
    opcoes = dict()
    mixer.init()
    som = mixer.Sound(resourcePath('./bip.mp3'))

    def bip(self):
        self.som.stop()
        self.som.play()

    @staticmethod
    def obter_listas() -> list:
        try:
            a = filter(listdir('listas'), '*.txt')
            return a
        except FileNotFoundError:
            mkdir('listas')
            return []

    def gerar_lista(self, lista: str, online: bool = False) -> list | bool:
        if not online:
            try:
                with open(f'listas/{lista}') as arq:
                    dados = arq.read().split('\n')
                    self.dados = dados
                    self.Completa = dados
                    print(self.dados, self.Completa)
                    return self.dados
            except FileNotFoundError:
                print('Não foi encontrada a lista!')
                return False
    
        else:
            try:
                request = r.get(lista, timeout=5)
                r.encoding = 'utf-8'
                dados = request.text.split('\n')
                self.dados = dados
                self.Completa = dados
                return self.dados
            except (r.ConnectionError, r.Timeout):
                return False

    def escolha_random(self, num: bool = False, mini: int = 0, maxi: int = 0, quanti: int = 1, rept = False) -> list | str:
        print(rept, self.dados, self.Completa)
        def retorno():
            if self.iniciado:
                self.recentes.append(self.aux)
                r_recentes = list(self.recentes)
                r_recentes.reverse()
                self.aux = self.escolha
                resultado = [ self.escolha, '\n'.join(r_recentes)]
                return resultado
            
            else:
                self.iniciado = True
                self.aux = self.escolha
                resultado = [self.escolha]
                print(resultado)
                return resultado

        
        if rept and not num and self.Completa:
            self.escolha = choice(self.Completa)
            while self.escolha == self.aux:
                self.escolha = choice(self.Completa)
                print(self.Completa, self.escolha)
        
        elif not rept and not num and self.dados:
            if len(self.dados) > 0:
                self.escolha = choice(self.dados)
                self.dados.remove(self.escolha)

        elif num:
            self.escolha = self.gerarNumeral(mini, maxi, quanti, rept)

        else:
            self.escolha = ''
            
        return retorno()

    def resetar(self):
        self.recentes.clear()
        self.aux = ''
        self.escolha = ''
        self.iniciado = False

    def salvar_arq(self, nome, lista, online = False) -> bool:
        texto = str(''.join(lista)if online else '\n'.join(lista))
        with open(f'listas/{nome}', 'w') as arq:
            if lista:
                arq.write(texto)
            else:
                arq.write('')
            return True

    def deletar_arq(self, nome) -> bool:
        try:
            remove(f'listas/{nome}')
            return True
        except FileNotFoundError:
            return False
        
    def add_online(self, apelido: str, url: str) -> bool:
        arquivo = TextIOWrapper
        lista = dict()

        try:
            with open('listas/online.json', encoding='utf-8') as arq:
                lista = loads(arq.read())

        except FileNotFoundError:
            with open('listas/online.json', 'w', encoding='utf-8') as arq:
                arq.write('{\n\n}')
        
        if 'raw' not in url:
            return False
        
        try:
            request = r.get(url, timeout=5)
            lista[apelido] = url
            with open('listas/online.json', 'w', encoding='utf-8') as arq:
                dump(lista, arq, indent=4, separators = (',',':'))
            return True
            
        except (r.ConnectionError, r.Timeout):
            return False

    @staticmethod
    def obterListasOnline() -> bool | dict:
        try:
            with open('listas/online.json', encoding='utf-8') as arq:
                arq: dict = loads(arq.read())
                return arq
        
        except FileNotFoundError:
            return False

    @staticmethod
    def getKeys(dict: dict) -> list:
        lista = []
        for i in dict:
            lista.append(i)
        return lista

    @staticmethod
    def removeOnline(lista: str):
        try:
            with open('listas/online.json', encoding='utf-8') as arq:
                listas = loads(arq.read())
                del listas[lista]
                arq = open('listas/online.json', 'w', encoding='utf-8')
                dump(listas, arq, indent=4, separators=(',', ':'))

        except FileNotFoundError:
            print('O arquivo de listas online não foi encontrado!')
        
        except KeyError:
            print('A lista online não existe ou já foi apagada!')
        
    def obterOpcoes(self):
        try:
            with open('opcoes.config', encoding='utf-8') as arq:
                self.opcoes = loads(arq.read())
                self.som = mixer.Sound(resourcePath('./bip.mp3') if not self.opcoes['som'] else self.opcoes['som'])
        
        except FileNotFoundError:
            with open('opcoes.config', 'w', encoding = 'utf-8') as arq:
                opcoes = {
                    "tema": "reddit",
                    "som": ""
                }
                dump(opcoes, arq, indent=4, separators=(',',':'))

    def salvarOpcoes(self):
        with open('opcoes.config', 'w', encoding='utf-8') as arq:
            dump(self.opcoes, arq, indent=4, separators=(',', ':'))
            self.obterOpcoes()
    
    def gerarNumeral(self, mini, maxi, quanti, rept = False) -> str | None:
        nums = list()
        for i in range(quanti):
            if rept:
                if quanti <= maxi:
                    num = str(randint(mini, maxi))
                    while num in nums:
                        num = str(randint(mini, maxi))
                    nums.append(num)
                
                else:
                    return None
            else:
                nums.append(str(randint(mini, maxi)))
        return ' '.join(nums)

# Fim