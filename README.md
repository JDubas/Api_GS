# Api com Flask e OracleDB

Este é um projeto que utiliza Flask e OracleDB para criar um Restful API simples.

## Requisitos

Para rodar este projeto, você precisará dos seguintes requisitos:

- **Python**: Certifique-se de ter a versão mais atual do Python 3 instalada.
- **Bibliotecas do Flask e OracleDB**: instale as bibliotecas necessárias utilizando pip.

```bash
pip install flask
pip install flask-cors
pip install oracledb
```

## Portas necessárias
- **Porta de entrada 80**: Deve estar aberta no grupo de segurança do Azure e no firewall do Windows.
- **Porta de saída 1521**: Também deve estar aberta no grupo de segurança do Azure e no firewall do Windows.

## Para testar
Abra um cmd na pasta aonde o api.py esta localizada e rode o comando
```bash
python api.py
```
Utilize **http://ipPublicoDaMaquina/comentarios**

## Observação
Caso após instalado o Python o Windows não reconheça tanto o comando Python como o pip, certifique que as variáveis globais do Windows estão com os paths configurados corretamente para ambos.
