import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["dados_abertos"]
mycol = mydb["pda-prouni"]

dados = open('pda-prouni-2019-test.csv', mode='r', encoding='utf-8-sig')
separator = ';'
headers = dados.readline().replace('\n', '').split(separator)

while True:

    print("Escolha uma opção: ")

    print("[1] Inserir dados dados manualmente")
    print("[2] Inserir arquivo .CSV no MongoDB")
    print("[3] Baixar Arquivo .TXT com os dados")
    print("[4] Sair")

    opcao = input("---> ")

    if opcao == '1':
        data = {}
        for header in headers:
            data[header] = input(f"{header}: ")
        print("Inserindo...")
        mycol.insert_one(data)
        print("Dado Inserido!")

    elif opcao == '2':
        lines = dados.readlines()

        blocks = []
        for line in lines:
            current_line = line.replace('\n', '').strip().replace('"', '').split(separator)
            current_index = len(blocks)
            blocks.append({})
            for index, header in enumerate(headers):
                blocks[current_index][header] = current_line[index]
        print("Inserindo...")
        mycol.insert_many(blocks)
        print("Dados Inseridos!")

    elif opcao == '3':
        consults_txt = open('resultados.txt', mode='w+', encoding="utf8")
        consults_txt.write("_id," + separator.join(headers) + '\n')

        print("Baixando Dados...")

        results = mycol.find({})

        for result in results:
            line = f"{result['_id']}{separator}"
            for header in headers:
                line += f"{result[header]}{separator}"
            consults_txt.write(line[:-1] + '\n')
        consults_txt.close()

        print("Dados Baixados!")

    elif opcao == '4':
        dados.close()
        break

    else:
        print("Opção inválida!")
