# coding: utf-8
# Usuario: gabri

from json import dump, loads
import sys
from pygame import mixer
from os import listdir, remove, mkdir
from os.path import join, abspath, dirname
from fnmatch import filter
from random import choice, randint
import requests as req


def resourcePath(relativo) -> str:
    base_path = getattr(sys, '_MEIPASS', dirname(abspath(__file__)))
    return join(base_path, relativo)


class Func:
    # Listas
    dados = list()
    completa = list()
    recentes = list()

    # Escolha
    escolha = str()
    aux = str()

    # Info da classe
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
                    self.dados = list(dados)
                    self.completa = list(dados)
                    print(self.dados, self.completa)
                    return self.dados

            except FileNotFoundError:
                return False

        else:
            try:
                request = req.get(lista, timeout=5)
                request.encoding = 'utf-8'
                dados = request.text.split('\n')
                self.dados = list(dados)
                self.completa = list(dados)

            except (req.ConnectionError, req.Timeout):
                return False

    def escolhaRandom(self, num: bool = False, minimo: int = 0, maximo: int = 0, quantidade: int = 1, repete: bool = False) -> list | str:
        def retorno():
            if self.iniciado:
                self.recentes.append(self.aux)
                r_recentes = list(self.recentes)
                r_recentes.reverse()
                self.aux = self.escolha
                print(f'{"-"*12}\nRepete: {"Sim" if repete else "N??o"}\nItem escolhido: {self.escolha}')
                resultado = [self.escolha, '\n'.join(r_recentes), len(self.dados) if not repete else "???"]
                return resultado
            else:
                self.iniciado = True
                self.aux = self.escolha
                resultado = [self.escolha, len(self.dados) if not repete else "???"]
                print(f'{"-"*12}\nRepete: {"Sim" if repete else "N??o"}\nItem escolhido: {self.escolha}')
                return resultado

        if repete and not num and self.completa:
            self.escolha = choice(self.completa)
            while self.escolha == self.aux:
                self.escolha = choice(self.completa)
                print(self.completa, self.escolha)

        elif not repete and not num and self.dados:
            if len(self.dados) > 0:
                self.escolha = choice(self.dados)
                self.dados.remove(self.escolha)

        elif num:
            self.escolha = self.gerarNumeral(minimo, maximo, quantidade, repete)

        else:
            self.escolha = ''

        return retorno()

    def resetar(self):
        self.recentes.clear()
        self.aux = ''
        self.escolha = ''
        self.iniciado = False

    @staticmethod
    def salvarArq(nome, lista, online=False) -> bool:
        texto = str(''.join(lista) if online else '\n'.join(lista))
        with open(f'listas/{nome}', 'w') as arq:
            if lista:
                arq.write(texto)

            else:
                arq.write('')

            return True

    @staticmethod
    def deletarArq(nome) -> bool:
        try:
            remove(f'listas/{nome}')
            return True

        except FileNotFoundError:
            return False

    @staticmethod
    def addOnline(apelido: str, url: str) -> bool:
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
            request = req.get(url, timeout=4)
            request.encoding = 'utf-8'
            lista[apelido] = url
            with open('listas/online.json', 'w', encoding='utf-8') as arq:
                dump(lista, arq, indent=4, separators=(',', ':'))
                return True

        except(req.ConnectionError, req.Timeout):
            return False

    @staticmethod
    def obterListasOnline() -> bool | dict:
        try:
            with open('listas/online.json', encoding='utf-8') as arq:
                arq = loads(arq.read())
                return arq

        except FileNotFoundError:
            return False

    @staticmethod
    def getKeys(objeto: dict) -> list:
        lista = []
        for i in objeto:
            lista.append(i)
        return lista

    @staticmethod
    def removeOnline(lista: str):
        try:
            with open('listas/online.json', encoding='utf-8') as arq:
                listas = loads(arq.read())
                del listas[lista]
                arq = open('listas/online', 'w', encoding='utf-8')
                dump(listas, arq, indent=4, separators=(',', ':'))

        except FileNotFoundError:
            print('O arquivo de listas online n??o foi encontrado!')

        except KeyError:
            print('A lista online n??o existe ou j?? foi apagada!')

    def obterOpcoes(self):
        try:
            with open('opcoes.config', encoding='utf-8') as arq:
                self.opcoes = loads(arq.read())
                self.som = mixer.Sound(resourcePath('./bip.mp3') if not self.opcoes['som'] else self.opcoes['som'])

        except FileNotFoundError:
            with open('opcoes.config', 'w', encoding='utf-8') as arq:
                opcoes = {
                    "tema": "reddit",
                    "som": ""
                }
                dump(opcoes, arq, indent=4, separators=(',', ':'))

    def salvarOpcoes(self):
        with open('opcoes.config', 'w', encoding='utf-8') as arq:
            dump(self.opcoes, arq, indent=4, separators=(',', ':'))

    @staticmethod
    def gerarNumeral(minimo, maximo, quantidade, repete=False) -> str | None:
        nums = list()
        for i in range(quantidade):
            if not repete:
                if quantidade <= maximo:
                    num = str(randint(minimo, maximo))
                    while num in nums:
                        num = str(randint(minimo, maximo))
                    nums.append(num)

                else:
                    return None

            else:
                nums.append(str(randint(minimo, maximo)))

        return ' '.join(nums)

# Fim
