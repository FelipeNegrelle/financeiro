import pandas as pd
import json
import questionary
from supabase import create_client

def main():    
    keys = json.load(open("keys.json", "r"))
    url = keys.get("url")
    key = keys.get("private_key")
    supabase = create_client(url, key)

    def fetchSaldo():
        data = supabase.table("financeiro").select("saldo").order("created_at").execute()
        saldo = json.loads(data.json())["data"][-1]["saldo"]
        return saldo
    
    def mostraSaldo():
        saldo = fetchSaldo()
        print(f"Seu saldo é {saldo}")
        menu()

    def entrada():
        saldo = fetchSaldo()
        print("Qual o valor da entrada?")
        valor = float(input())
        razao = input("Qual a razão da entrada? ")
        valorFinal = saldo + valor
        print(f"seu saldo é {valorFinal}")
        supabase.table("financeiro").insert({"valor": valor, "tipo": "entrada", "saldo": valorFinal, "razao": razao}).execute()
        print("Entrada registrada com sucesso!")
        menu()

    def saida():
        saldo = fetchSaldo()
        print("Qual o valor da saída?")
        valor = float(input())
        valorFinal = saldo - valor
        razao = input("Qual a razão da saída? ")
        print(f"seu saldo é {valorFinal}")
        supabase.table("financeiro").insert({"valor": valor, "tipo": "saida", "saldo": valorFinal, "razao": razao}).execute()
        print("Saída registrada com sucesso!")
        menu()

    def gerarPlanilha():
        print("Gerando planilha...")
        dados = supabase.table("financeiro").select("*").execute()
        df = pd.DataFrame(dados)
        df.to_csv("planilha.csv")
        print("Planilha gerada com sucesso!")
        menu()

    def sobre():
        print("Sobre o programa...")
        menu()

    def menu():
        escolha = questionary.select(
            "Bem vindo ao gestor de planilhas financeiras o que gostaria de fazer?",
            choices = [
                "Mostrar saldo",
                "Incluir entrada",
                "Incluir saída",
                "Gerar planilha",
                "Sobre",
                "Sair"
            ],
            qmark="💸",
            pointer="->"
        ).ask()

        match escolha:
            case "Mostrar saldo":
                mostraSaldo()
            case "Incluir entrada":
                entrada()
            case "Incluir saída":
                saida()
            case "Gerar planilha":
                gerarPlanilha()
            case "Sobre":
                sobre()
            case "Sair":
                 exit()
            case _: 
                print("Use uma opção válida :)")
    menu()
main()
