from ofxparse import OfxParser

with open("extrato.ofx", "rb") as arquivo:
    ofx = OfxParser.parse(arquivo)

print("EXTRATO BANCÁRIO")

for t in ofx.account.statement.transactions:

    print(f"""
Data      : {t.date.strftime('%d/%m/%Y')}
Valor     : R$ {t.amount:.2f}
Descrição : {t.memo}
--------------------------------------
""")