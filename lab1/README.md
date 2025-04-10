# Laboratório 1

Este repositório contém os arquivos para a prática de laboratório da disciplina ELE-32.

## Descrição

Neste laboratório, implementamos um canal binário simétrico (BSC) e codificadores/decodificadores para simular a transmissão de bits através de um canal ruidoso. O objetivo é estudar o comportamento do canal e a eficácia do código de correção de erros.

## Arquivos

- `main.py`: Script principal que executa a simulação.
- `modules/Encoder.py`: Implementação de codificadores (Hamming e personalizado).
- `modules/Decoder.py`: Implementação de decodificadores (Hamming e personalizado).
- `modules/Channel.py`: Implementação de um canal binário simétrico (BSC).
- `modules/System.py`: Representação de um sistema de comunicação completo.

## Como executar

1. Certifique-se de ter o Python instalado.
2. Instale as dependências necessárias:
    ```bash
    pip install numpy matplotlib
    ```
3. Execute o script principal:
    ```bash
    python main.py
    ```

## Estrutura do Código

### `main.py`

- Gera uma sequência de bits aleatórios.
- Codifica os bits usando o codificador.
- Transmite os bits codificados através do canal binário simétrico.
- Decodifica os bits recebidos.
- Calcula a taxa de erro de bit (Pb) e plota o gráfico de Pb vs P.

### `modules/Encoder.py`

- Define a classe `Encoder` com métodos para codificação de bits.

### `modules/Decoder.py`

- Define a classe `Decoder` com métodos para cálculo de síndrome, detecção de erro e decodificação.

### `modules/Channel.py`

- Define a classe `Channel` com um método para transmitir bits através do canal com uma probabilidade de erro `p`.

### `modules/System.py`

- Define a classe `System` que integra o codificador, canal e decodificador para simular o sistema completo.
