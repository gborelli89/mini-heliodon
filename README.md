# mini-heliodon
Projeto de Heliodon de pequenas dimensões com controle automático para usos educacionais.

Os arquivos STL podem ser baixados e impressos em uma impressora 3D. Alguns elementos como lâmpada LED, acoplamentos, motores de passo e rolamentos devem ser comprados. O projeto deve ser usado como referência. Foi desenvolvido pensando em um dispositivo de pequenas dimensões, que facilite sua fabricação (em impressoras caseiras) e manuseio. Deve ser adaptado para cada necessidade.

## Controle
Para este projeto foram empregados dois motores de passo, um para movimentação do azimute e outro para a movimentação da altura. O controle é feito por meio de microcontrolador (código na pasta *src*).


## Algoritmos de posicionamento solar e APP
Para a determinação da posição do sol foi utilizado o pacote pysolar, da linguagem Python.

Python também foi utilizado para o desenvolvimento de um aplicativo simples que, dadas das coordenadas geográficas, o horário e dia do ano, posiciona o LED na posição do sol (no modelo físico do heliodon), bem como plota a posição em uma carta solar simplificada, com linhas de referência, como solstícios e equinócio.