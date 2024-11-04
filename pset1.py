# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Antonio Rafael Andrade Mateus
#    Matrícula: 202201713
#    Turma: CC6N
#    Email: rafasam123@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage

def montar_kernel(n):
    valor_kernel = 1/(n**2)
    kernel = []
    for _ in range(n):
        linha = [valor_kernel for _ in range(n)]
        kernel.append(linha)
    return kernel
    
# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):   
        def limitar(valor, minimo, maximo): #função auxilair para deixar modular
            return max(minimo, min(valor, maximo))
        
        x = limitar(x, 0, self.largura - 1)
        y = limitar(y, 0, self.altura - 1)

        return self.pixels[y * self.largura + x]   #Tinha uma tupla(corrigido). Retorna o pixel na posição (x, y) da imagem.

    def set_pixel(self, x, y, c):             
        self.pixels[y * self.largura + x] = c #Tinha uma tupla(corrigido). Define o pixel na posição (x, y) da imagem com a cor c

    def aplicar_por_pixel(self, func):
        resultado = Imagem.nova(self.largura, self.altura)
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor) #Estava fora do loop(corrigido)
        return resultado
    
    def correlacao(self, kernel):
        tamanho_kernel = len(kernel)
        delocamento = tamanho_kernel // 2
        imagem_resultado = Imagem.nova(self.largura, self.altura)
        for x in range(self.largura):
            for y in range(self.altura):
                soma_correlacao = 0
                for w in range(tamanho_kernel):
                    for z in range(tamanho_kernel):
                        pixel = self.get_pixel(x - delocamento + w, y - delocamento + z)
                        soma_correlacao += pixel * kernel[w][z]
                imagem_resultado.set_pixel(x, y, soma_correlacao)
        return imagem_resultado
    
    def pixel_normalizado(self):
        def normalizar_valor(valor):
            return max(0, min(255, round(valor)))
        for x in range(self.largura):
            for y in range(self.altura):
                # Obter o valor do pixel e limitar entre 0 e 255
                pixelanalise = normalizar_valor(self.get_pixel(x, y))
                # Definir o valor do pixel na imagem
                self.set_pixel(x, y, pixelanalise)
        

    def invertida(self):                                 #Estava 256(corrigido) 
        return self.aplicar_por_pixel(lambda c: 255 - c) # Aplica uma função que inverte a cor de cada pixel e retorna o resultado

    def borrada(self, n):
        kernel = self.correlacao(montar_kernel(n))
        kernel.pixel_normalizado()
        return kernel

    def focada(self, n):
        imagemborrada = self.borrada(n)
        imagemfocada = Imagem.nova(self.largura, self.altura)
        for x in range(self.largura):
            for y in range(self.altura):
                valor_pixel_original = self.get_pixel(x, y)
                valor_pixel_focada = round(2 * valor_pixel_original - imagemborrada.get_pixel(x,y))
                imagemfocada.set_pixel(x, y, valor_pixel_focada)
        imagemfocada.pixel_normalizado()
        return imagemfocada

    def bordas(self):
        imagemborda = Imagem.nova(self.largura, self.altura)
        KernelX =   [[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]]
        KernelY =   [[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]]
        SobelXaplicar = self.correlacao(KernelX)
        SobelYaplicar = self.correlacao(KernelY)
        for x in range(self.largura):
            for y in range(self.altura):
                valor_sobel_X = SobelXaplicar.get_pixel(x, y)
                valor_sobel_Y = SobelYaplicar.get_pixel(x, y)
                sobelOperation = round(math.sqrt(valor_sobel_X ** 2 + valor_sobel_Y ** 2))
                imagemborda.set_pixel(x, y, sobelOperation)
        imagemborda.pixel_normalizado()
        return imagemborda
    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    
    #Questão2
    peixe = Imagem.carregar('test_images/bluegill.png')
    peixeinvertido = peixe.invertida()
    Imagem.salvar(peixeinvertido, 'resultadosimg/peixeinvertidoQuestao2.png')

    #Questão4

    kernel = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0], 
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    porco = Imagem.carregar('test_images/pigbird.png')
    porcorrelacao = porco.correlacao(kernel)
    Imagem.salvar(porcorrelacao, 'resultadosimg/porcorrelacaoQuestão4.png')

    #Questão 5 (borrada)
    gato = Imagem.carregar('test_images/cat.png')
    gatoborrado = gato.borrada(5)
    Imagem.salvar(gatoborrado, 'resultadosimg/gatoborradoQuestão5.png')

    #Questão5 (focada)
    cobra = Imagem.carregar('test_images/python.png')
    cobrafocada = cobra.focada(11)
    Imagem.salvar(cobrafocada, 'resultadosimg/cobrafocadaQuestão5.png')

    #Questão6
    KernelX =   [[-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1]]
    KernelY =   [[-1, -2, -1],
                [0, 0, 0],
                [1, 2, 1]]
    construcao = Imagem.carregar('test_images/construct.png')
    construcaosobelX = construcao.correlacao(KernelX) 
    Imagem.salvar(construcaosobelX, 'resultadosimg/construcaosobelXQuestão6.png')
    construcaosobelY = construcao.correlacao(KernelY) 
    Imagem.salvar(construcaosobelY, 'resultadosimg/construcaosobelYQuestão6.png')
    construcaoborda = construcao.bordas()
    Imagem.salvar(construcaoborda, 'resultadosimg/construcaobordaQuestão6.png')
    pass
    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    Imagem.mostrar(peixeinvertido)
    Imagem.mostrar(porcorrelacao)
    Imagem.mostrar(gatoborrado)
    Imagem.mostrar(cobrafocada)
    Imagem.mostrar(construcaoborda)
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
