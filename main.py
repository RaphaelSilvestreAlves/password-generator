from src.password_generator import generate_password, evaluate_strength, Storage, Entry

def main():
    print("🔐 Gerador e Armazenador de Senhas Seguras\n")

    while True:
        length_input = input("Qual o comprimento de senha a ser gerada? (padrão: 12): ").strip()
        if not length_input:
            length = 12
            break
        if length_input.isdigit():
            length = int(length_input)
            if length < 4:
                print("⚠️  O comprimento mínimo recomendado é 4 caracteres.")
            elif length > 128:
                print("⚠️  O comprimento máximo recomendado é 128 caracteres.")
            else:
                break
        else:
            print("❌ Digite apenas números, por favor.")

    senha = generate_password(length=length)
    print(f"\nSenha gerada: {senha}")

    resultado = evaluate_strength(senha)
    print(f"Força: {resultado['label']}")
    if resultado['tips']:
        print("Dicas:", ", ".join(resultado['tips']))

    storage = Storage()
    entry = Entry.create(password=senha)
    storage.save(entry)
    print("\n✅ Senha salva com sucesso!")

if __name__ == "__main__":
    main()
