# Laboratório 1

Este repositório contém os arquivos para a prática de laboratório da disciplina ELE-32.

## Descrição

Neste laboratório, implementamos um canal binário simétrico (BSC) e um codificador/decodificador para simular a transmissão de bits através de um canal ruidoso. O objetivo é estudar o comportamento do canal e a eficácia do código de correção de erros.

## Arquivos

- `main.py`: Script principal que executa a simulação.
- `encoder.py`: Implementação do codificador e do decodificador.
- `BinarySymmetricChannel.py`: Implementação de um *Binary Symmetric Channel* (Canal Binário Simétrico).

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

### `encoder.py`

- Define a classe `Encoder` com métodos para codificação, cálculo de síndrome, detecção de erro e decodificação.

### `BinarySymmetricChannel.py`

- Define a classe `BinarySymmetricChannel` com um método para transmitir bits através do canal com uma probabilidade de erro `p`.
