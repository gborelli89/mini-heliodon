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

## Algoritmos de posicionamento solar e APP
Para a determinação da posição do sol foi utilizado o pacote pysolar, da linguagem Python.

Python também foi utilizado para o desenvolvimento de um aplicativo simples que, dadas das coordenadas geográficas, o horário e dia do ano, posiciona o LED na posição do sol (no modelo físico do heliodon), bem como plota a posição em uma carta solar simplificada, com linhas de referência, como solstícios e equinócio.