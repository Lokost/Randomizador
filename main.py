# Coding: UTF - 8
from time import sleep
from PySimpleGUI import *
from func import Func
from os.path import exists

Func = Func()

class Janela:
    recentes = list()
    dados = list()
    iniciado = False
    reiniciar = False
    mini = int()
    maxi = int()
    num = False
    quant = int()
    
    def abrir(self):
        Func.obterOpcoes()
        theme(Func.opcoes['tema'])
        self.reiniciar = False
        self.principal()
        return self.reiniciar

    def principal(self):
        Func.escolha = str()
        Func.aux = str()

        menu = [['Arquivo', ['Editor','Adicionar lista online', 'Carregar lista online', 'Sorteio numérico','---','Opções','---', 'Sobre']]]

        menu_func = {
            'Editor': lambda : self.editor(),
            'Sobre': lambda : [self.sobre()],
            'Adicionar lista online': lambda: [self.add_online()],
            'Opções': lambda: self.opcoes()
        }

        layout1 = [[Text('Randomizador', font=(None, 15))],
                   [Text('Selecione uma lista (Local):')],
                   [Combo(Func.obter_listas(), k='lista', enable_events=True, expand_x=True, readonly=True)],
                   [Button('Usar listas locais', k='local', expand_x=True, visible=False)],
                   [Multiline('<b>\n</b>'.join(self.recentes), disabled=True, expand_x=True, expand_y=True, k='recentes', font=(None, 15), justification='center')],
                   [Button('Limpar histórico', k='clear', expand_x=True)],
                   [Checkbox('Som', k='som', default=True), Checkbox('Resultados repetidos', k='rept', default=True)]]

        layout2 = [[Text('Resultado:')],
                   [Multiline('', font=(None, 45), k='result', expand_x=True, justification='center', disabled=True, expand_y=True, no_scrollbar=True)],
                   [Button('Randomizar', k='random', expand_x=True, font=(None, 30), disabled=True)]]

        layout = [[Menu(menu)],
                  [Frame('Configurações', layout1, size=(300, 500)), Frame('Saída', layout2, size=(450, 500))]]

        janela = Window('Randomizador', layout, element_justification='center', auto_size_text=True, resizable=False, size=(800, 500))

        while True:
            evt, val = janela.read()

            if evt == WIN_CLOSED:
                break

            elif evt == 'random':
                result = Func.escolha_random(self.num, self.mini, self.maxi, self.quant, val['rept'])
                if result == None:
                    popup('A lista está vazia!')
                
                else:

                    janela['result'].update(result[0])

                    if len(result) > 1:
                        janela['recentes'].update(result[1])

                    if val['som']:
                        Func.bip()

            elif evt == 'lista':
                try:
                    self.dados = Func.gerar_lista(val['lista'])
                    janela['result'].update('')
                    Func.resetar()
                    janela['recentes'].update('')
                    janela.set_title(f'{val["lista"].replace(".txt","")} - Randomizador')
                    popup('Lista carregada')
                    janela['random'].update(disabled=False)
                    self.num = False
                except Exception as e:
                    popup(f'Não foi possível carregar a lista!\n{e}')

            elif evt == 'Carregar lista online':
                lista = self.load_online()
                if lista:
                    janela['result'].update('')
                    Func.resetar()
                    janela['recentes'].update('')
                    janela.set_title(f'lista online - {lista} - Randomizador')
                    janela['lista'].update(visible=False)
                    janela['local'].update(visible=True)
                    janela['random'].update(disabled=False)

            elif evt == 'local':
                janela['lista'].update(visible=True)
                janela['local'].update(visible=False)

            elif evt == 'clear':
                Func.resetar()
                janela['recentes'].update('')
            
            elif evt == 'Sorteio numérico':
                if self.numeral():
                    janela['result'].update('')
                    Func.resetar()
                    janela['recentes'].update('')
                    janela.set_title(f'Sorteio numérico - Randomizador')
                    janela['lista'].update(visible=False)
                    janela['local'].update(visible=True)
                    janela['random'].update(disabled=False)

            else:
                if evt in menu_func:
                    mOp = menu_func[evt]()
                    if mOp not in [None, '']:
                        if mOp == 'OK':
                            janela.close()
                            self.reiniciar = True
                    
                    else:
                        janela['lista'].update(values=Func.obter_listas())

    def editor(self):

        selecionada = []

        layout = [[Combo(Func.obter_listas(), enable_events=True, expand_x=True, k='listas'), Button('Nova Lista', k='nl'), Button('Apagar lista', k='apagar')],
                  [Text('Pesquisar: '), Input(k="pesquisa", enable_events=True, expand_x=True)],
                  [Listbox(selecionada, size=(80, 20), disabled=True, k='itens', select_mode='multiple')],
                  [Button('Adicionar', k='add', expand_x=True), Button('Remover', k='rem', expand_x=True)],
                  [Button('Limpar lista', expand_x=True, k='limpar')],
                  [Button('Salvar', k='salvar', expand_x=True)]]

        janela = Window('Editor', layout, resizable=False, modal=True, font=(None, 12))

        while True:
            evt, val = janela.read()

            if evt == 'listas':
                selecionada = Func.gerar_lista(val['listas'])
                janela['itens'].update(disabled=False)
                janela['itens'].update(values=selecionada)
                janela.set_title(f'Editando: {val["listas"]}')
                janela['pesquisa'].update('')

            elif evt == 'rem':
                if val['itens']:
                    resposta = popup_ok_cancel('Deseja realmente deletar esses itens?')
                    sel = val['itens']
                    if resposta == 'OK':
                        print(f'removendo {sel}')
                        for i in sel:
                            selecionada.pop(selecionada.index(i))

                janela['itens'].update(values=selecionada)
                janela['pesquisa'].update('')

            elif evt == 'add':
                item = popup_get_text('Digite o que será adicionado!')
                if item:
                    selecionada.append(item)
                    janela['pesquisa'].update('')
                else:
                    popup('Não foi digitado um valor válido!')
                janela['itens'].update(values=selecionada)

            elif evt == 'salvar':
                if selecionada and val['listas']:
                    if Func.salvar_arq(val['listas'], selecionada) and selecionada:
                        popup('Lista salva!')

                elif not selecionada and val['listas']:
                    Func.deletar_arq(val['listas'])
                    janela['listas'].update(value='', values=Func.obter_listas())
                    selecionada.clear()
                    janela['itens'].update(selecionada)

                else:
                    popup('Não foi selecionada uma lista!')

            elif evt == WIN_CLOSED:
                break

            elif evt == 'limpar':
                if popup_ok_cancel(f'Deseja limpar a lista {val["listas"]}?') == 'OK':
                    selecionada.clear()
                    janela['itens'].update(selecionada)

            elif evt == 'pesquisa':
                resultado = list()
                if val['pesquisa']:
                    for i in selecionada:
                        if val['pesquisa'].lower() in i.lower():
                            resultado.append(i)

                    janela['itens'].update(resultado)

                else:
                    janela['itens'].update(selecionada)

            elif evt == 'nl':
                nome = popup_get_text('Nome da lista:')

                if nome:
                    if '.txt' not in nome:
                        nome += '.txt'

                    if nome in Func.obter_listas():
                        popup('A lista já existe!')

                    selecionada = []
                    Func.salvar_arq(nome, selecionada)
                    janela['listas'].update(value=nome, values=Func.obter_listas())
                    janela['itens'].update(selecionada, disabled=False)

            elif evt == 'apagar':
                if popup_yes_no(f'Deseja apagar a lista {val["listas"]}?').lower() == "yes":
                    Func.deletar_arq(val['listas'])
                    janela['listas'].update(value='', values=Func.obter_listas())
                    selecionada.clear()
                    janela['itens'].update(selecionada)

    def sobre(self):
        layout = [[Text('Ramdomizador', font=(None, 20))],
                  [Text('Aplicação simples feita por Gabriel Gomes', font=(None, 15))],
                  [Text('AKA Lokost Games', font=(None, 10))],
                  [Text('Versão: 0.6', font=(None, 8))],
                  [Button('Fechar', k='close')]]

        janela = Window('Sobre', layout, disable_minimize=True, resizable=False, modal=True, element_justification='center')

        while True:
            evt = janela.read()[0]
            if evt in ['close', WIN_CLOSED]:
                janela.close()
                break

    def add_online(self):
        layout = [
            [Text('Apelido: '), Input(k='apelido', expand_x=True)],
            [Text('URL: '), Input(k='url', expand_x=True)],
            [Checkbox('Baixar Lista', k='download')],
            [Button('Adicionar', k='add',expand_x=True), Button('Cancelar', k='cancel', expand_x=True)]
        ]

        janela = Window('Adicionar lista online', layout, size=(350, 130), modal=True)

        while True:
            evt, val = janela.read()

            if evt == 'add':
                if val['apelido'] and val['url']:
                    if Func.add_online(val['apelido'], val['url']):
                        if val['download']:
                            try:
                                Func.salvar_arq(f"{val['apelido']}.txt", Func.gerar_lista(val['url'], True), True)
                                popup('A lista foi salva e baixada!')
                            except Exception as e:
                                popup(f'Não foi possível baixar a lista!\n{e}')
                        else:
                            popup('Lista adicionada com sucesso!')
                            janela.close()
                            break
                    else:
                        popup('Não foi possível encontrar a lista!\nVerifique se a lista é um raw!\nOu sua conexão à internet!')

                else:
                    popup('Verifique as informações adicionadas!')
                
                
            
            elif evt in ['cancel', WIN_CLOSED]:
                janela.close()
                break

    def load_online(self):
        online = Func.obterListasOnline()
        listas = Func.getKeys(online)
        existente = True
        if not online:
            existente = False

        layout = [
            [Text('Selecione uma lista para carregá-la:')],
            [Combo(listas, k='lista', expand_x=True, default_value=listas[0])],
            [Checkbox('Baixar lista', k='download')],
            [Button('Carregar', k='load', expand_x=True), Button('Cancelar', k='cancel', expand_x=True), Button('Remover', k='remove', expand_x=True)]
        ]

        janela = Window('Carregar Online', layout, size=(350, 130), modal=True)

        while True:
            if not existente:
                popup('Não foram encontradas listas online!')
                break
            else:
                evt, val = janela.read()
                
                if evt == 'load':
                    lista = Func.gerar_lista(lista=online[val['lista']], online=True)
                    if lista:
                        if val['download']:
                            Func.salvar_arq(f"{val['lista']}.txt", lista, True)

                        self.dados = lista
                        popup('Lista carregada' if not val['download'] else 'lista carregada e baixada!')
                        janela.close()
                        return val['lista']
                    else:
                        popup('Não foi possível carregar a lista')
                        janela.close()
                        break

                elif evt == 'remove':
                    if popup_ok_cancel(f'Deseja realmente deletar a lista "{val["lista"]}"?') == 'OK':
                        Func.removeOnline(val['lista'])
                        online = Func.obterListasOnline()
                        listas = Func.getKeys(online)
                        janela['lista'].update(values=listas)


                elif evt in ['cancel', WIN_CLOSED]:
                    janela.close()
                    break

    def opcoes(self):
        tipos = (
            ('Tipos suportados', '*.mp3 *.ogg *.wav'),
            ('MP3', '*.mp3'),
            ('Ogg', '*.ogg'),
            ('WAV', '*.wav')
        ,)

        layout = [
            [Text('Opções', font=(None, 20))],
            [Text('Tema'), Combo(theme_list(), expand_x=True, k='tema', default_value=Func.opcoes['tema'])],
            [Text('Som personalizado: '), Input(Func.opcoes['som'],k='som', expand_x=True, readonly=True), FileBrowse('Procurar', file_types=tipos), Button('Padrão', k='default')],
            [Button('Aplicar', k='apply', expand_x=True), Button('Cancelar', k='cancel', expand_x=True)]
            ]

        janela = Window('Opções', layout, size=(650, 150), modal=True, finalize=True)

        while True:
            evt, val = janela.read()

            if evt == 'apply':
                Func.opcoes['tema'] = val['tema']
                Func.opcoes['som'] = val['som']
                Func.salvarOpcoes()
                janela.close()
                return popup_ok_cancel('Algumas opções foram atualizadas, reinicitar o aplicativo?')
            
            elif evt == 'default':
                janela['som'].update('')
            
            elif evt in ['cancel', WIN_CLOSED]:
                janela.close()
                break

    def numeral(self):
        layout = [
            [Text('Mínimo'), Input(k='min', expand_x=True)],
            [Text('Máximo'), Input(k='max', expand_x=True)],
            [Text('Quantidade'), Input(k='quant', expand_x=True)],
            [Button('Gerar', k='gen', expand_x=True, bind_return_key=True), Button('Cancelar', k='cancel', expand_x=True)]
        ]

        janela = Window('Numeral', layout, size=(300, 130), modal=True, finalize=True)

        while True:
            evt, val = janela.read()

            if evt in [WIN_CLOSED, 'cancel']:
                janela.close()
                return False

            elif evt == 'gen':
                try:
                    self.mini = int(val['min'])
                    self.maxi = int(val['max'])
                    self.quant = int(val['quant'])
                    self.num = True
                    print(f'{self.mini} {self.maxi} {self.quant}')
                    janela.close()
                    return True
                
                except ValueError:
                    popup('Os valores devem ser inteiros e sem espaços!')


if __name__ == '__main__':
    j = Janela()
    abrir = True
    while abrir:
        abrir = j.abrir()

# Fim
