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
        """
        Retorna o valor do pixel na posição (x, y) da imagem.
        Caso as coordenadas fornecidas estejam fora dos limites da imagem,
        utiliza o valor mais próximo dentro dos limites.
        """
        def limitar(valor, minimo, maximo): #função auxilair
            return max(minimo, min(valor, maximo))
        
        x = limitar(x, 0, self.largura - 1)
        y = limitar(y, 0, self.altura - 1)

        return self.pixels[y * self.largura + x]   #Tinha uma tupla(corrigido). Retorna o pixel na posição (x, y) da imagem.
        

    def set_pixel(self, x, y, c): 
        """
        Define o valor do pixel na posição (x, y) da imagem com a cor (intensidade) fornecida.
        """            
        self.pixels[y * self.largura + x] = c #Tinha uma tupla(corrigido). Define o pixel na posição (x, y) da imagem com a cor c

    def aplicar_por_pixel(self, func):
        """
        Aplica uma função a cada pixel da imagem, criando uma nova imagem resultante.
        Retorna a imagem resultante após a aplicação da função a cada pixel.
        """
        resultado = Imagem.nova(self.largura, self.altura)
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor) #Estava fora do loop(corrigido)
        return resultado
    
    def correlacao(self, kernel):
        """
        Aplica uma operação de correlação na imagem usando o kernel fornecido.
        Cada pixel da imagem resultante é calculado com base nos valores de intensidade
        dos pixels vizinhos na imagem original e nos pesos definidos pelo kernel.
        Retorna uma nova imagem com o resultado da correlação.
        """
        tamanho_kernel = len(kernel)
        delocamento = tamanho_kernel // 2
        imagem_resultado = Imagem.nova(self.largura, self.altura)
        for x in range(self.largura):
            for y in range(self.altura):
                soma_correlacao = 0
                # Percorre o kernel e soma os produtos dos pixels adjacentes
                for w in range(tamanho_kernel):
                    for z in range(tamanho_kernel):
                        pixel = self.get_pixel(x - delocamento + w, y - delocamento + z) # Obtém o pixel adjacente
                        soma_correlacao += pixel * kernel[w][z] # Multiplica pelo valor do kernel
                imagem_resultado.set_pixel(x, y, soma_correlacao) # Armazena o resultado na nova imagem
        return imagem_resultado
    
    def pixel_normalizado(self):
        """
        Normaliza os valores dos pixels da imagem, limitando-os entre 0 e 255.
        Esta função é útil após operações como correlação, onde os valores dos
        pixels podem exceder esses limites.
        """
        def normalizar_valor(valor):
            return max(0, min(255, round(valor)))
        for x in range(self.largura):
            for y in range(self.altura):
                # Obter o valor do pixel e limitar entre 0 e 255
                pixelanalise = normalizar_valor(self.get_pixel(x, y))
                # Definir o valor do pixel na imagem
                self.set_pixel(x, y, pixelanalise)
        

    def invertida(self):                                 #Estava 256(corrigido) 
        """
        Cria uma nova imagem onde cada pixel é a inversão do pixel correspondente
        na imagem original (255 - valor do pixel).
        """
        return self.aplicar_por_pixel(lambda c: 255 - c) # Aplica uma função que inverte a cor de cada pixel e retorna o resultado

    def borrada(self, n):
        """
        Aplica um efeito de desfoque na imagem com base em um kernel de média de tamanho n.
        Retorna uma nova imagem com o efeito de desfoque.
        """
        kernel = self.correlacao(montar_kernel(n))# Aplica a correlação com o kernel
        kernel.pixel_normalizado() # Normaliza os pixels da nova imagem borrada
        return kernel

    def focada(self, n):
        """
        Aplica um efeito de foco na imagem ao subtrair uma imagem desfocada (obtida com o kernel de média de tamanho n)
        da imagem original. Normaliza os valores de pixel da imagem focada.
        """
        imagemborrada = self.borrada(n) # Aplica o desfoque
        imagemfocada = Imagem.nova(self.largura, self.altura)
        for x in range(self.largura):
            for y in range(self.altura):
                valor_pixel_original = self.get_pixel(x, y)
                # Calcula a diferença entre os pixels da imagem original e a imagem borrada
                valor_pixel_focada = round(2 * valor_pixel_original - imagemborrada.get_pixel(x,y))
                imagemfocada.set_pixel(x, y, valor_pixel_focada)
        imagemfocada.pixel_normalizado()
        return imagemfocada

    def bordas(self):
        """
        Detecta as bordas da imagem usando o operador Sobel. Calcula a magnitude do gradiente
        para cada pixel, aplicando as matrizes de kernel Sobel nos eixos X e Y.
        Retorna uma nova imagem com as bordas detectadas.
        """
        imagemborda = Imagem.nova(self.largura, self.altura)
        # Detecta bordas usando o operador de Sobel.
        KernelX =   [[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]]
        KernelY =   [[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]]
        SobelXaplicar = self.correlacao(KernelX) # Aplica o kernel para o eixo X
        SobelYaplicar = self.correlacao(KernelY) # Aplica o kernel para o eixo Y
        for x in range(self.largura):
            for y in range(self.altura):
                valor_sobel_X = SobelXaplicar.get_pixel(x, y)
                valor_sobel_Y = SobelYaplicar.get_pixel(x, y)
                # Calcula a magnitude do gradiente utilizando a raiz quadrada da soma dos quadrados
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

    imagem_teste = Imagem.nova(100, 100)  # Cria uma imagem em branco 100x100
    imagem_teste.mostrar()
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
