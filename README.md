# mini-heliodon
Projeto de Heliodon de pequenas dimensões com controle automático para usos educacionais.

Os arquivos STL podem ser baixados e impressos em uma impressora 3D. Alguns elementos como lâmpada LED, acoplamentos, motores de passo e rolamentos devem ser comprados. O projeto deve ser usado como referência. Foi desenvolvido pensando em um dispositivo de pequenas dimensões, que facilite sua fabricação (em impressoras 3D de filamento caseiras, por exemplo) e manuseio. Deve ser adaptado para cada necessidade. 

Na tabela abaixo é dada a lista de materiais básicos necessários para a construção do heliodon na escala proposta.

| DESCRIÇÃO | QUANT. |
| --------- | -----: |
| Motor de passo 28BYJ-48 | 2 |
| Driver de motor de passo ULN2003 | 2 |
| LED branco de alto brilho 5 mm | 1 |
| Resistor 100 &Omega; | 1 |
| Chave liga/desliga (opcional) | 1 |
| Fonte chaveada 5 V 1 A e conector | 1 |
| Arduino Uno (ou outro microcontrolador) | 1 |
| Rolamento 623ZZ | 6 |
| Parafuso M4 x 12 mm | 2 |
| Parafuso M4 x 20 mm | 5 |
| Parafuso M4 x 30 mm | 2 |
| Porca M4 | 9 |
| Arruela M4 | 13 |
| Parafuso M3 x 10 mm | 9 |
| Parafuso M3 x 16 mm | 3 |
| Porca M3 | 12 |
| Chapa de madeira (ou outro material) revestida de branco &empty;150 mm x 3 mm | 1 |
| Filamento de PLA (ou outro material, dependendo da impressora) | &asymp; 150 g |
| | |



## Controle
Para este projeto foram empregados dois motores de passo, um para movimentação do azimute e outro para a movimentação da altura. O controle é feito por meio de um microcontrolador (código na pasta *src*). O esquema básico de ligação é mostrado na figura abaixo.

<img src="/img/heliodon_eletronica.png">

## *Software*

### Pacotes necessários

É necessário possuir python instalado. As bibliotecas necessáriarias são apresentadas abaixo com a última versão testada entre parênteses. Recomenda-se que sua instalação seja feita em ambiente virtual, utilizando o PIP:

```
pip install package_name
```

* numpy (1.26.4)
* pandas (2.2.1)
* pysolar (0.11)
* plotly (5.19.0)
* pyserial (3.5)
* dash (2.15.0)
* waitress (3.0.0)

### Simulações implementadas

* ***onepoint_sim***: simulação de uma posição solar, dada latitude, longitude, data e horário.
* ***oneday_sim***: simulação da posição solar em um dia completo, hora a hora, dada latiture, longitude e data.
* ***month_sim***: simulação da posição solar mês a Mês, para a mesma posição geográfica (latitude e longitude), ano, dia e hora.

As simulações podem ser executadas diretamente a partir da linha de comando. Para isso basta importar o arquivo *heliodon.py*, fazer a conexão, determinar a altitude e o azimute com uma das simulações e utilizar a função *move* para mover o heliodon. Um exemplo de movimentação única e simples é dado abaixo.

```
import heliodon as sun

con = sun.connect('COM1') # modificar de acordo com a porta

# Simulação simples de uma posição
x = sun.onepoint_sim(-23.5, -46.7, 2023, 3, 20, 12, utcdiff=-3)

# Movimentação do heliodon
sun.move(con, float(x.latitude.iloc[0]), float(x.altitude.iloc[0]), float(x.azimuth.iloc[0]))
```

Caso deseje verificar as portas conectadas (com o objetivo de identificar a porta em que o microcontrolador está conectado), utilize a função *serial_ports()*, disponível em *heliodon.py*.

Para facilitar o uso, foi criada uma interface gráfica, que pode ser utilizada carregando diretamente o arquivo *heliodon_app.py*, ou seja, 

```
C:\> python heliodon_app.py
```

A interface gráfica gera diagramas como o apresentado na figura abaixo.

<img src="/img/exemplo_diagrama.png">