def buscar_livro(acervo, isbn):
    for i, livro in enumerate(acervo):
        if livro["isbn"].replace("-", "") == isbn.replace("-", ""):
            return livro, i
    return None, -1


def buscar_emprestimo(emprestimos, codigo):
    for emprestimo in emprestimos:
        if emprestimo["codigo"] == codigo:
            return emprestimo
    return None


def ler_inteiro(mensagem, minimo=0):
    while True:
        try:
            valor = int(input(mensagem))
            if valor >= minimo:
                return valor
            print(f"Informe um valor maior ou igual a {minimo}.")
        except ValueError:
            print("Entrada invalida, digite um numero inteiro.")


def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip().title()
        if texto:
            return texto
        print("O campo nao pode ficar vazio.")


def ler_isbn():
    while True:
        isbn = input("ISBN (13 digitos): ").strip()
        digitos = isbn.replace("-", "")
        if len(digitos) == 13 and digitos.isdigit():
            return isbn
        print("ISBN invalido. Informe 13 digitos.")


def incluir_livro(acervo):
    isbn = ler_isbn()
    livro, indice = buscar_livro(acervo, isbn)
    if livro is not None:
        print("Erro: livro ja cadastrado.")
        return
    titulo = ler_texto("Titulo: ")
    autor = ler_texto("Autor: ")
    quantidade = ler_inteiro("Quantidade total: ", 1)
    disponivel = ler_inteiro("Quantidade disponível: ")
    if disponivel > quantidade:
        print("Erro: a quantidade disponível não pode superar o acervo.")
        return
    livro = {
        "titulo": titulo,
        "autor": autor,
        "isbn": isbn,
        "quantidade": quantidade,
        "disponivel": disponivel,
    }
    acervo.append(livro)
    print("Inclusao confirmada.")


def realizar_emprestimo(acervo, emprestimos):
    isbn = ler_isbn()
    livro, indice = buscar_livro(acervo, isbn)
    if livro is None:
        print("Erro: livro nao encontrado.")
        return
    if livro["disponivel"] == 0:
        print("Erro: não ha exemplares disponiveis.")
        return
    codigo = ler_inteiro("Codigo do emprestimo: ", 1)
    if buscar_emprestimo(emprestimos, codigo) is not None:
        print("Erro: codigo de emprestimo já cadastrado.")
        return
    matricula = ler_texto("Matricula do usuário (4 dígitos): ")
    if len(matricula) != 4 or not matricula.isdigit():
        print("Erro: a matricula deve ter 4 digitos.")
        return
    data = ler_texto("Data do emprestimo: ")
    prazo = ler_inteiro("Prazo para devolução (dias): ", 1)
    emprestimo = {
        "codigo": codigo,
        "matricula": matricula,
        "isbn": livro["isbn"],
        "data": data,
        "prazo": prazo,
        "devolvido": False,
    }
    emprestimos.append(emprestimo)
    livro["disponivel"] -= 1
    print(f"Emprestimo realizado - codigo {codigo}.")


def devolver_livro(acervo, emprestimos):
    codigo = ler_inteiro("Codigo do emprestimo: ", 1)
    emprestimo = buscar_emprestimo(emprestimos, codigo)
    if emprestimo is None:
        print("Erro: emprestimo nao encontrado.")
        return
    if emprestimo["devolvido"]:
        print("Erro: livro ja devolvido.")
        return
    print("\nDados do emprestimo:")
    print(f"Código: {emprestimo['codigo']}")
    print(f"Matrícula: {emprestimo['matricula']}")
    print(f"ISBN: {emprestimo['isbn']}")
    print(f"Data: {emprestimo['data']}")
    print(f"Prazo: {emprestimo['prazo']} dias")
    confirmacao = input("Confirmar devolucaoo? (S/N): ").strip().upper()
    if confirmacao == "S":
        livro, indice = buscar_livro(acervo, emprestimo["isbn"])
        if livro is not None:
            livro["disponivel"] += 1
            emprestimo["devolvido"] = True
            print("Devolução realizada.")
        else:
            print("Erro: livro não encontrado no acervo.")
    else:
        print("Devolucao cancelada.")


def relatorio_livros(acervo):
    print(f"===== Relatório do Acervo =====")
    if len(acervo) == 0:
        print(f"Nenhum livro encontrado.")
    else:
        for livro in acervo:
            print(f'Titulo: {livro["titulo"]}')
            print(f'Autor: {livro["autor"]}')
            print(f'ISBN: {livro["isbn"]}')
            print(f'Quantidade: {livro["quantidade"]}')
            print(f'Disponivel: {livro["disponivel"]}')
            print(" ")


def relatorio_emprestimos(emprestimos):
    print(f"===== Emprestimos Ativos =====")
    if len(emprestimos) == 0:
        print(f"Nenhum emprestimo ativo no momento.")
    else:
        for emprestimo in emprestimos:
            if not emprestimo["devolvido"]:
                print(f'Codigo: {emprestimo["codigo"]}')
                print(f'Matricula: {emprestimo["matricula"]}')
                print(f'ISBN: {emprestimo["isbn"]}')
                print(f'Data: {emprestimo["data"]}')
                print(f'Prazo: {emprestimo["prazo"]} dias')
                print(" ")


def menu():
    acervo = []
    emprestimos = []
    while True:
        print("\n--- BIBLIOTECA ---")
        print("1 - Incluir livro")
        print("2 - Realizar emprestimo")
        print("3 - Devolver livro")
        print("4 - Relatório de livros")
        print("5 - Relatório de emprestimos ativos")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            incluir_livro(acervo)
        elif opcao == "2":
            realizar_emprestimo(acervo, emprestimos)
        elif opcao == "3":
            devolver_livro(acervo, emprestimos)
        elif opcao == "4":
            relatorio_livros(acervo)
        elif opcao == "5":
            relatorio_emprestimos(emprestimos)
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("Opcao invalida.")


menu()
