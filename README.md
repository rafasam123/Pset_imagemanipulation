# ling_prog_cc6n

Aluno: Antonio Rafael Andrade Mateus

Disciplina: Linguagens de programação

Professor: Abrantes Araújo Silva Filho

# PSET1

## Questões:
> Vamos começar com uma imagem 4×1 que é definida com os seguintes parâmetros: \
> altura: 1 \
>• largura: 4 \
>• pixels: [29, 89, 136, 200] \
>
> **QUESTÃO 01:** se você passar essa imagem pelo filtro de inversão, qual seria o output esperado? Justifique sua resposta.

R: Sabendo que os pixels podem ser representados em cores nos valores de 0 até 255, sendo o 0 preto e o 255 o branco, e que o inverso de branco é preto (isto é, se invertermos o branco (valor 0) teremos o valor invertido como preto (valor 255), e vice versa). Podemos deduzir que o inverso de preto é o valor máximo que um pixel pode ter, menos o valor da cor preta:

: 255 [valor maximo] - 0 [preto] = 255 => Branco.

Portanto, os valores inversos da imagem 4x1 dada no enunciado são, respectivamente:

• pixels: [226, 166, 119, 55]

-------------

> QUESTÃO 02: faça a depuração e, quando terminar, seu código deve conseguir passar em todos os testes do grupo de teste TestInvertido (incluindo especificamente o que você acabou de criar). Execute seu filtro de inversão na imagem imagens_teste/peixe.png, salve o resultado como uma imagem PNG e salve a imagem.

No arquivo pset1.py, é possível encontrar no final do arquivo o código que executa esta tarefa. E, na pasta resultadosimg é possível ver a imagem peixeinvertidoQuestao2.png com o filtro invertido aplicado.
Codigo:
```python
def invertida(self):
    return self.aplicar_por_pixel(lambda c: 255 - c)
#__________________________main______________________________
peixe = Imagem.carregar('test_images/bluegill.png')
peixeinvertido = peixe.invertida()
Imagem.salvar(peixeinvertido, 'resultadosimg/peixeinvertidoQuestao2.png')
```
| Imagem Original | Imagem Invertida |
| --------------- | ---------------- |
| ![Peixe](./test_images/bluegill.png "Peixe") | ![Peixe Invertido](./resultadosimg/peixeinvertidoQuestao2.png) |

-------------

> QUESTÃO 3: Considere uma etapa de correlacionar uma imagem com o seguinte kernel: \
[ 0.00 -0.07 0.00 \
-0.45 1.20 -0.25 \
0.00 -0.12  0.00 ]  
Aqui está uma parte de uma imagem de amostra, com as luminosidades específicas de alguns pixels:

![ImageQuestion 3](https://i.imgur.com/tOPa0FJ.png)

> Qual será o valor do pixel na imagem de saída no local indicado pelo destaque vermelho? Observe que neste ponto ainda não arredondamos ou recortamos o valor, informe exatamente como você calculou. Observação: demonstre passo a passo os cálculos realizados.

Para calcularmos a imagem resultande dessa correlação, basta somarmos as multiplicações dos respectivos pixels do kernel com a imagem. Por exemplo, sendo o kernel K[x,y] e a Imagem I[x,y], multiplicaremos K[0,0] com I[0,0], e assim sucessivamente. E por fim teremos:

1) (80 * 0,00) + (53 * (-0,07)) + (99 * 0) + (129 * (-0,45)) + (127 * 1,2) + (148 * (-0,25)) + (175 * 0) + (174 * (-0,12)) + (193 * 0)

2) = 0 + (-3.71) + (0) + (-58.05) + (152.4) + (-37) + 0 + (-20.88) + 0 

3) **= 32.76**

-------------

> QUESTÃO 4: quando você tiver implementado seu código, tente executá-lo em imagens_teste/porco.png com o seguinte kernel 9 ×9:
> 
>[ 0 0 0 0 0 0 0 0 0 \
>0 0 0 0 0 0 0 0 0 \
>1 0 0 0 0 0 0 0 0 \
>0 0 0 0 0 0 0 0 0 \
>0 0 0 0 0 0 0 0 0 \
>0 0 0 0 0 0 0 0 0 \
>0 0 0 0 0 0 0 0 0 \
>0 0 0 0 0 0 0 0 0 \
>0 0 0 0 0 0 0 0 0 ]

No arquivo pset1.py, é possível encontrar no final do arquivo o código que executa esta tarefa. E, na pasta resultadosimg é possível ver a imagem porcorrelacaoQuestão4.png correlacionada, de acordo com o kernel acima.
Codigo:
```python
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
#__________________________main______________________________
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
```
| Imagem Original | Imagem Correlação |
| --------------- | ---------------- |
| ![Porco](./test_images/pigbird.png "Porco e passaro") | ![Porco Correlação](./resultadosimg/porcorrelacaoQuestão4.png) |

-----

> QUESTÃO 5: se quisermos usar uma versão desfocada B que foi feita com um kernel de desfoque de caixa de 3 × 3, que kernel k poderíamos usar para calcular toda a imagem nítida com uma única correlação? Justifique sua resposta mostrando os cálculos

Sim, é possível utilizando uma única correlação. Sendo a operação de nitidez definida por:

S x,y = round( 2 * Ix,y - Bx,y )

Temos por definição que o kernel de identidade é aquele que retorna na saída a mesma imagem da entrada. Então, como temos na fórmula acima o dobro da imagem em que queremos aplicar a nitidez, temos:

2 * Ix,y :\
[ 0 0 0 \
0 2 0 \
0 0 0 ] 

e, sabemos que o kernel 3 x 3 tem como valores definidos: 

[ 1/9, 1/9, 1/9 \
1/9, 1/9, 1/9 \
1/9, 1/9, 1/9 ]

A subtração de 2Ix,y com Bx,y resulta em:

[ -1/9, -1/9, -1/9 \
-1/9, -17/9, -1/9 \
-1/9, -1/9, -1/9 ].

No arquivo pset1.py, é possível encontrar no final do arquivo o código que executa esta tarefa. E, na pasta resultadosimg é possível ver a imagem cobrafocadaQuestão5.png com a nitidez aplicada. Também no mesmo local, é possível encontrar o código que executa a tarefa da seção 5.1, na pasta resultadosimg está salvo o resultado da aplicação do blur com raio 5 na imagem teste.
Codigo:

```python
def montar_kernel(n):
    valor_kernel = 1/(n**2)
    kernel = []
    for _ in range(n):
        linha = [valor_kernel for _ in range(n)]
        kernel.append(linha)
    return kernel

def pixel_normalizado(self):
    def normalizar_valor(valor):
        return max(0, min(255, round(valor)))
    for x in range(self.largura):
        for y in range(self.altura):
            pixelanalise = normalizar_valor(self.get_pixel(x, y))
            self.set_pixel(x, y, pixelanalise)

def borrada(self, n):
    kernel = self.correlacao(montar_kernel(n))# Aplica a correlação com o kernel
    kernel.pixel_normalizado() # Normaliza os pixels da nova imagem borrada
    return kernel

def focada(self, n):
    imagemborrada = self.borrada(n) # Aplica o desfoque
    imagemfocada = Imagem.nova(self.largura, self.altura)
    for x in range(self.largura):
        for y in range(self.altura):
            valor_pixel_original = self.get_pixel(x, y)
            valor_pixel_focada = round(2 * valor_pixel_original - imagemborrada.get_pixel(x,y))
            imagemfocada.set_pixel(x, y, valor_pixel_focada)
    imagemfocada.pixel_normalizado()
    return imagemfocada
#__________________________main______________________________
gato = Imagem.carregar('test_images/cat.png')
gatoborrado = gato.borrada(5)
Imagem.salvar(gatoborrado, 'resultadosimg/gatoborradoQuestão5.png')

cobra = Imagem.carregar('test_images/python.png')
cobrafocada = cobra.focada(11)
Imagem.salvar(cobrafocada, 'resultadosimg/cobrafocadaQuestão5.png')
```

| Imagem Original | Imagem Focada |
| --------------- | ---------------- |
| ![Cobra](./test_images/python.png "cobra") | ![Cobra focada](./resultadosimg/cobrafocadaQuestão5.png) |

<br>

| Imagem Original | Imagem Borrada |
| --------------- | ---------------- |
| ![Gato](./test_images/cat.png "gato") | ![Gato borrado](./resultadosimg/gatoborradoQuestão5.png) |

> QUESTÃO 6: explique o que cada um dos kernels acima, por si só, está fazendo. Tente executar mostrar nos resultados dessas correlações intermediárias para ter uma noção do que está acontecendo aqui.

Cada um dos kernels apresentados é responsável por derivar a imagem com as bordas destacadas, sendo um deles pelo eixo x e outro pelo eixo y.
Codigo:
```python
def bordas(self):
    imagemborda = Imagem.nova(self.largura, self.altura)
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
            sobelOperation = round(math.sqrt(valor_sobel_X ** 2 + valor_sobel_Y ** 2))
            imagemborda.set_pixel(x, y, sobelOperation)
    imagemborda.pixel_normalizado()
    return imagemborda
#__________________________main______________________________
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
```

| Kernel Sobel no eixo X | Kernel Sobel no eixo Y |
| --------------- | ---------------- |
| ![SobelX](./resultadosimg/construcaosobelXQuestão6.png "Kernel Sobel X") | ![SobelY](./resultadosimg/construcaosobelYQuestão6.png "Kernel Sobel Y") |


Aplicação da Operação de Sobel completa, segundo a fórmula:

Ox,y = round (√Ox²x,y + Oy² x,y)

| Imagem Original | imagem com Bordas |
| --------------- | ---------------- |
| ![construção](./test_images/construct.png) | ![SobelOperation](./resultadosimg/construcaobordaQuestão6.png "Operação Sobel") |
