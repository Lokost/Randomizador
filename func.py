# coding: utf-8
# Usuario: gabri

from io import TextIOWrapper
from json import dump, loads
import sys
from pygame import mixer
from os import listdir, remove, mkdir, environ
from os.path import exists, join, abspath, dirname
from fnmatch import filter
from random import choice
import requests


class Func:
    dados = list()
    escolha = str()
    aux = ''
    recentes = list()
    iniciado = bool()


    mixer.init()
    def bip(self):
        a = mixer.Sound(self.resource_path('./bip.mp3'))
        a.play()
        
    @staticmethod
    def resource_path(relative):
        base_path = getattr(sys, '_MEIPASS', dirname(abspath(__file__)))
        return join(base_path, relative)

    @staticmethod
    def obter_listas() -> list:
        try:
            a = filter(listdir('listas'), '*.txt')
            return a
        except FileNotFoundError:
            mkdir('listas')
            a = filter(listdir('listas'), '*.txt')
            return a

    def gerar_lista(self, lista: str, online = False) -> list | bool:
        if not online:
            try:
                with open(f'listas/{lista}') as arq:
                    self.dados = arq.read().split('\n')
                    return self.dados

            except FileNotFoundError:
                # sg.popup('Não foi encontrada a lista', title='Erro!')
                print('Não foi encontrada a lista')
        
        else:
            try:
                r = requests.get(lista, timeout=5)
                r.encoding = 'utf-8'
                self.dados = r.text.split('\n')
                return self.dados
            except (requests.ConnectionError, requests.Timeout):
                return False

    def ler(self, lista: str):
        self.dados = self.gerar_lista(lista)
        print(self.dados)

    def escolha_random(self) -> list:
        if self.dados:
            while self.escolha == self.aux:
                self.escolha = choice(self.dados)

            if self.iniciado:
                self.recentes.append(self.aux)
                r_recentes = list(self.recentes)
                r_recentes.reverse()
                self.aux = self.escolha
                return [self.escolha, '\n'.join(r_recentes)]

            else:
                self.iniciado = True
                self.aux=self.escolha

        return [self.escolha]

    def resetar(self):
        self.recentes.clear()
        self.aux = ''
        self.escolha = ''
        self.iniciado = False

    def salvar_arq(self, nome, lista):
        texto = str('\n'.join(lista))
        print(texto)
        with open(f'listas/{nome}', 'w') as arq:
            if lista:
                arq.write(texto)
            else:
                arq.write('')
            return True

    def deletar_arq(self, nome):
        try:
            remove(f'listas/{nome}')
        except FileNotFoundError:
            print('Não foi encontrado o arquivo.')

    def add_online(self, apelido: str, url: str) -> bool:
        if not exists('listas'):
            mkdir('listas')
        
        r = ''
        existente = False
        arquivo = TextIOWrapper
        lista = dict()

        if exists('listas/online.json'):
            with open('listas/online.json', encoding='utf-8') as arq:
                lista = loads(arq.read())
        
        else:
            with open('listas/online.json', 'w') as arq:
                arq.write('{\n\n}')
        
        if 'raw' not in url:
            return False
        
        try:
            r = requests.get(url, timeout = 5)
            existente = True
        except (requests.ConnectionError, requests.Timeout):
            existente = False

        if existente:
            lista[apelido] = url
            with open('listas/online.json', 'w') as arq:
                dump(lista, arq, indent=4, separators=(',', ':'))
            return True
        
        else:
            return False
                
    @staticmethod
    def obter_listas_online() -> bool | dict :
        if not exists('listas/online.json'):
            return False
        
        with open('listas/online.json', encoding='utf-8') as arq:
            arq: dict = loads(arq.read())
            return arq

    @staticmethod
    def get_keys(dict: dict) -> list:
        lista = list()
        for i in dict:
            lista.append(i)
        return lista

    @staticmethod
    def remove_online(lista: str):
        with open('listas/online.json', encoding='utf-8') as arq:
            listas = loads(arq.read())
            del listas[lista]
            arq = open('listas/online.json', 'w')
            dump(listas, arq, indent=4, separators=(',',':'))
# Fim
