### ChatGPT Agente

## Instalação

Basta instalar o pacote via pip
```
pip install GPTAgent
```

Gerar uma Key no site da OpenAI para desenvolvedores e colocar no arquivo **chat_key.json**

```
{"api_key": "coloque_aqui_sua_api_key_da_OpenAI"}
```

Exemplo:

```
from GPTAgent_img import GPTAgent

agente = GPTAgent.GPTAgent(name="Bob", estilo="Você é engraçado e positivo.")

print(agente.perguntar("Bom dia!"))
```
