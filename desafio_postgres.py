import psycopg2
from ofxparse import OfxParser

with open("extrato.ofx", "rb") as arquivo:
    ofx = OfxParser.parse(arquivo)

transacoes = ofx.account.statement.transactions


conexao = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="snow2(+!DDFSWIC"
)
cursor = conexao.cursor()

inseridas = 0
duplicadas = 0

for t in transacoes:
    data = t.date.date()
    valor = t.amount
    descricao = (t.memo or "")[:255]

    cursor.execute(
        "SELECT 1 FROM movimentacoes "
        "WHERE data_movimentacao = %s AND valor = %s AND descricao = %s",
        (data, valor, descricao)
    )

    if cursor.fetchone():
        duplicadas += 1
        print(f"Duplicada, ignorada: {data} | {valor} | {descricao}")
        continue

    cursor.execute(
        "INSERT INTO movimentacoes (data_movimentacao, valor, descricao) "
        "VALUES (%s, %s, %s)",
        (data, valor, descricao)
    )
    inseridas += 1

conexao.commit()
print(f"Inseridas: {inseridas} | Duplicadas: {duplicadas}")
cursor.close()
print("Conectado com sucesso!")
conexao.close()

