# coding: UTF-8
# Arquivo: main_n

from PySimpleGUI import *

from func import Func

Func = Func()


class Janela:
    recentes = list()
    dados = list()
    iniciado = False
    reiniciar = False
    minimo = int()
    maximo = int()
    num = False
    quant = int()

    def abrir(self) -> bool:
        Func.obterOpcoes()
        theme(Func.opcoes['tema'])
        self.reiniciar = False
        self.principal()
        return self.reiniciar

    def principal(self) -> None:
        Func.escolha = str()
        Func.aux = str()

        menu = [
            [
                'Arquivo', [
                    'Editor',
                    'Adicionar lista online',
                    'Carregar lista online',
                    'Sorteio numérico',
                    '---',
                    'Opções',
                    '---',
                    'Sair'
                ],
            ],
            ['Sobre', [
                'GitHub',
                'Sobre'
            ]]
        ]

        menu_func = {
            'Editor': lambda: self.editor(),
            'Sobre': lambda: self.sobre(),
            'Adicionar lista online': lambda: self.addOnline(),
            'Opções': lambda: self.opcoes(),
            'GitHub': lambda: webbrowser.open('https://github.com/Lokost/Randomizador')
        }

        layout1 = [
            [
                Text(
                    'Randomizador',
                    font=(None, 15)
                )
            ],
            [
                Text(
                    'Selecione uma lista (local):'
                )
            ],
            [
                Combo(
                    Func.obter_listas(),
                    k='lista',
                    enable_events=True,
                    expand_x=True,
                    readonly=True
                )
            ],
            [
                Button(
                    'Usar listas locais',
                    k='local',
                    expand_x=True,
                    disabled=True
                )
            ],
            [
                Text(
                    text ='Itens restantes da lista: 0',
                    k='restantes'
                )
            ],
            [
                Multiline(
                    '<b>\n</b>'.join(self.recentes),
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    k='recentes',
                    font=(None, 15),
                    justification='center',
                    auto_size_text=True
                )
            ],
            [
                Button(
                    'Limpar histórico',
                    k='clear',
                    expand_x=True
                )
            ],
            [
                Checkbox(
                    'Som',
                    k='som',
                    default=True
                ),
                Checkbox(
                    'Resultados repetidos',
                    k='rept',
                    default=False
                )
            ]
        ]

        layout2 = [
            [
                Text(
                    'Resultado:'
                )
            ],
            [
                Multiline(
                    '',
                    font=(None, 45),
                    k='result',
                    expand_x=True,
                    expand_y=True,
                    disabled=True,
                    no_scrollbar=True
                )
            ],
            [
                Button(
                    'Randomizar',
                    k='random',
                    expand_x=True,
                    font=(None, 30),
                    disabled=True
                )
            ]
        ]

        layout = [
            [
                Menu(menu)
            ],
            [
                Frame(
                    'Configurações',
                    layout1,
                    size=(300, 500),
                    expand_x=True,
                    expand_y=True,
                    element_justification='center'
                ),
                Frame(
                    'Saída',
                    layout2,
                    size=(450, 500),
                    expand_y=True,
                    expand_x=True,
                    element_justification='center'
                )
            ]
        ]

        janela = Window(
            'Randomizador',
            layout,
            element_justification='center',
            auto_size_text=True,
            resizable=True,
            size=(800, 500)
        )

        while True:
            evt, val = janela.read()

            if evt in ['Sair', WIN_CLOSED]:
                janela.close()
                break

            elif evt == 'random':
                result = Func.escolhaRandom(
                    self.num,
                    self.minimo,
                    self.maximo,
                    self.quant,
                    val['rept']
                )

                if result is None or result[0] == '':
                    popup('A lista está vazia! Ou o item é incorreto!')

                else:
                    janela['result'].update(result[0])
                    janela['restantes'].update(f'Itens restantes da lista: {result[1]}')

                    if len(result) > 2:
                        janela['recentes'].update(result[1])
                        janela['restantes'].update(f'Itens restantes da lista: {result[2]}')

                    if val['som']:
                        Func.bip()

            elif evt == 'lista':
                try:
                    Func.resetar()
                    self.dados = Func.gerar_lista(val['lista'])
                    janela['result'].update('')
                    janela['recentes'].update('')
                    janela['restantes'].update(f'Itens restantes da lista: {len(Func.dados)}')
                    janela.set_title(f'{val["lista"].replace(".txt", "")} - Randomizador')
                    popup('lista carregada')
                    janela['random'].update(disabled=False)
                    self.num = False

                except Exception as e:
                    popup(f'Não foi possível carregar a lista!\n{e}')

            elif evt == 'Carregar lista online':
                lista = self.loadOnline()
                if lista:
                    janela['result'].update('')
                    janela.set_title(f'lista online - {lista} - Randomizador')
                    janela['lista'].update(disabled=True)
                    janela['local'].update(disabled=False)
                    janela['random'].update(disabled=False)

            elif evt == 'local':
                janela['lista'].update(disabled=False)
                janela['local'].update(disabled=True)

            elif evt == 'clear':
                Func.resetar()
                janela['recentes'].update('')

            elif evt == 'Sorteio numérico':
                if self.numeral():
                    janela['result'].update('')
                    Func.resetar()
                    janela['recentes'].update('')
                    janela.set_title(f'Sorteio numérico - Randomizador')
                    janela['lista'].update(disabled=True)
                    janela['local'].update(disabled=False)
                    janela['random'].update(disabled=False)

            else:
                if evt in menu_func:
                    opcao = menu_func[evt]()
                    if opcao not in [None, '']:
                        if opcao == 'OK':
                            janela.close()
                            self.reiniciar = True

                    else:
                        janela['lista'].update(values=Func.obter_listas())

    @staticmethod
    def editor():
        selecionada = []

        layout = [
            [
                Combo(
                    Func.obter_listas(),
                    enable_events=True,
                    expand_x=True,
                    k='listas'
                ),
                Button(
                    'Nova Lista',
                    k='nl'
                ),
                Button(
                    'Apagar lista',
                    k='apagar'
                )
            ],
            [
                Text(
                    'Pesquisar: '
                ),
                Input(
                    k='pesquisa',
                    enable_events=True,
                    expand_x=True
                )
            ],
            [
                Listbox(
                    selecionada,
                    size=(80, 20),
                    disabled=True,
                    k='itens',
                    select_mode='multiple'
                )
            ],
            [
                Button(
                    'Adicionar',
                    k='add',
                    expand_x=True
                ),
                Button(
                    'Remover',
                    k='rem',
                    expand_x=True
                )
            ],
            [
                Button(
                    'Limpar lista',
                    expand_x=True
                )
            ],
            [
                Button(
                    button_text='Salvar',
                    k='salvar',
                    expand_x=True
                )
            ]
        ]

        janela = Window(
            'Editor',
            layout,
            resizable=False,
            modal=True,
            font=(None, 12)
        )

        while True:
            evt, val = janela.read()
            if evt == 'listas':
                selecionada = Func.gerar_lista(val['listas'])
                janela['itens'].update(
                    values=selecionada,
                    disabled=False
                )
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
                    if Func.salvarArq(val['listas'], selecionada) and selecionada:
                        popup('Lista salva!')

                elif not selecionada and val['listas']:
                    Func.deletarArq(val['listas'])
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
                    if nome[:-4] != '.txt':
                        nome += '.txt'

                    if nome in Func.obter_listas():
                        popup('A lista já existe!')

                    selecionada = []
                    Func.salvarArq(nome, selecionada)
                    janela['listas'].update(value=nome, values=Func.obter_listas())
                    janela['itens'].update(selecionada, disable=False)
                    janela.set_title(f'Editando: {nome}')

            elif evt == 'apagar':
                if popup_yes_no(f'Deseja apagar a lista {val["listas"]}?').lower() == "yes":
                    Func.deletarArq(val['listas'])
                    janela['listas'].update(value='', values=Func.obter_listas())
                    selecionada.clear()
                    janela['itens'].update(selecionada)

    @staticmethod
    def sobre():
        layout = [
            [
                Text(
                    'Randomizador',
                    font=(None, 20)
                )
            ],
            [
                Text(
                    'Aplicação simples feita por Gabriel Gomes',
                    font=(None, 15)
                )
            ],
            [
                Text(
                    'AKA Lokost Games',
                    font=(None, 10)
                )
            ],
            [
                Text(
                    'Versão: 0.6',
                    font=(None, 10)
                )
            ],
            [
                Button(
                    'Fechar',
                    k='close',
                    expand_x=True
                )
            ]
        ]

        janela = Window(
            'Sobre',
            layout,
            disable_minimize=True,
            resizable=False,
            modal=True,
            element_justification='center'
        )

        while True:
            evt = janela.read()[0]

            if evt in ['close', WIN_CLOSED]:
                janela.close()
                break

    @staticmethod
    def addOnline():
        layout = [
            [
                Text('Apelido: '),
                Input(
                    k='apelido',
                    expand_x=True
                )
            ],
            [
                Text('URL: '),
                Input(
                    k='url',
                    expand_x=True
                )
            ],
            [
                Checkbox(
                    'Baixar Lista',
                    k='download'
                )
            ],
            [
                Button(
                    'Adicionar',
                    k='add',
                    expand_x=True
                ),
                Button(
                    'Cancelar',
                    k='cancel',
                    expand_x=True
                )
            ]
        ]

        janela = Window(
            'Adicionar lista online',
            layout,
            size=(350, 130),
            modal=True
        )

        while True:
            evt, val = janela.read()

            if evt == 'add':
                if not val['apelido'] or not val['url']:
                    popup('Verifique as informações adicionadas!')

                elif not Func.addOnline(val['apelido'], val['url']):
                    popup(
                        'Não foi possível encontrar a lista!\nVerifique se a lista é um raw!\nOu sua conexão à internet!'
                    )

                else:
                    if val['download']:
                        try:
                            Func.salvarArq(
                                nome=f"{val['apelido']}.txt",
                                lista=Func.gerar_lista(lista=val['url'], online=True),
                                online=True
                            )

                        except Exception as e:
                            popup(f'Não foi possível baixar a lista!\n{e}')

                    else:
                        popup('Lista adicionada com sucesso!')
                        janela.close()
                        break

            elif evt in ['cancel', WIN_CLOSED]:
                janela.close()
                break

    def loadOnline(self):
        online = Func.obterListasOnline()
        listas = Func.getKeys(online)
        existente = True
        if not online:
            existente = False

        layout = [
            [
                Text(
                    text='Selecione uma lista para carregá-la:'
                )
            ],
            [
                Combo(
                    values=listas,
                    k='lista',
                    expand_x=True,
                    default_value=listas[0]
                )
            ],
            [
                Checkbox(
                    text='Baixar lista',
                    k='download'
                )
            ],
            [
                Button(
                    button_text='Carregar',
                    k='load',
                    expand_x=True
                ),
                Button(
                    button_text='Cancelar',
                    k='cancel',
                    expand_x=True
                ),
                Button(
                    button_text='Remover',
                    k='remover',
                    expand_x=True
                )
            ]
        ]

        janela = Window(
            title='Carregar Online',
            layout=layout,
            size=(350, 130),
            modal=True
        )

        while True:
            if existente:
                evt, val = janela.read()
            else:
                break

            if evt == 'load':
                lista = Func.gerar_lista(
                    lista=online[val['lista']],
                    online=True
                )

                if lista:
                    if val['download']:
                        Func.salvarArq(
                            nome=f"{val['lista']}.txt",
                            lista=lista,
                            online=True
                        )

                    self.dados = lista
                    popup(
                        'Lista carregada' if not val['download'] else 'Lista carregada e baixada!'
                    )
                    janela.close()
                    return val['lista']

                else:
                    popup('Não foi possível carregar a lista!')
                    janela.close()
                    break

            elif evt == 'remove':
                if popup_ok_cancel(f'deseja realmente deletar a lista "{val["lista"]}"?') == 'OK':
                    Func.removeOnline(val['lista'])
                    online = Func.obterListasOnline()
                    listas = Func.getKeys(online)
                    janela['lista'].update(values=listas)

            elif evt in ['cancel', WIN_CLOSED]:
                janela.close()
                break

    @staticmethod
    def opcoes():
        tipos = (
            ('Tipos suportados', '*.mp3 *.ogg *.wav'),
            ('MP3', '*.mp3'),
            ('Ogg', '*.ogg'),
            ('WAV', '*.wav'),
        )

        layout = [
            [
                Text(
                    text='Opções',
                    font=(None, 20)
                )
            ],
            [
                Text(
                    text='tema'
                ),
                Combo(
                    values=theme_list(),
                    expand_x=True,
                    k='tema',
                    default_value=Func.opcoes['tema']
                )
            ],
            [
                Text(
                    text='Som personalizado: '
                ),
                Input(
                    default_text=Func.opcoes['som'],
                    k='som',
                    expand_x=True,
                    readonly=True
                ),
                FileBrowse(
                    button_text='Procurar',
                    file_types=tipos
                ),
                Button(
                    button_text='Padrão',
                    k='default'
                )
            ],
            [
                Button(
                    button_text='Aplicar',
                    k='apply',
                    expand_x=True
                ),
                Button(
                    button_text='Cancelar',
                    k='cancel',
                    expand_x=True
                )
            ]
        ]

        janela = Window(
            title='Opções',
            layout=layout,
            size=(650, 150),
            modal=True,
            finalize=True
        )

        while True:
            evt, val = janela.read()

            if evt == 'apply':
                for i in ['tema', 'som']:
                    Func.opcoes[i] = val[i]
                Func.salvarOpcoes()
                janela.close()
                return popup_ok_cancel('Algumas opções foram atualizadas, reiniar o aplicativo?')

            elif evt == 'default':
                janela['som'].update('')

            elif evt in ['cancel', WIN_CLOSED]:
                janela.close()
                break

    def numeral(self):
        layout = [
            [
                Text(
                    text='Mínimo: '
                ),
                Input(
                    k='min',
                    expand_x=True
                )
            ],
            [
                Text(
                    text='Máximo'
                ),
                Input(
                    k='max',
                    expand_x=True
                )
            ],
            [
                Text(
                    text='Quantidade'
                ),
                Input(
                    k='quant',
                    expand_x=True,
                )
            ],
            [
                Button(
                    button_text='Gerar',
                    k='gen',
                    expand_x=True,
                    bind_return_key=True
                ),
                Button(
                    button_text='Cancelar',
                    k='cancel',
                    expand_x=True
                )
            ]
        ]

        janela = Window(
            title='Numeral',
            layout=layout,
            size=(300, 130),
            modal=True,
            finalize=True
        )

        while True:
            evt, val = janela.read()

            if evt in [WIN_CLOSED, 'cancel']:
                janela.close()
                return False

            elif evt == 'gen':
                try:
                    self.minimo = int(val['min'])
                    self.maximo = int(val['max'])
                    self.quant = int(val['quant'])
                    self.num = True
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
