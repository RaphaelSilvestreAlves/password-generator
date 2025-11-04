import re
from password_generator.generator import generate_password, evaluate_strength
from password_generator.storage import Storage, Entry


def test_storage_save_and_load(tmp_path):
    """Testa se o armazenamento salva e carrega corretamente."""
    p = tmp_path / "pw.json"
    s = Storage(path=p)
    entry = Entry.create(password="abc123")  # 🔹 Agora só aceita 'password'
    s.save(entry)

    loaded = s.load()
    assert len(loaded) == 1
    assert loaded[0].password == "abc123"
    assert "T" in loaded[0].created_at  # Confere formato ISO (ex: '2025-11-04T15:30:00...')


def test_gerar_senha_tamanho():
    """Garante que o tamanho da senha gerada é o solicitado."""
    s = generate_password(length=12)
    assert len(s) == 12


def test_gerar_senha_contem_tipos():
    """Verifica se a senha contém todos os tipos de caracteres habilitados."""
    s = generate_password(length=10, use_upper=True, use_lower=True, use_digits=True, use_symbols=True)
    assert any(c.islower() for c in s)
    assert any(c.isupper() for c in s)
    assert any(c.isdigit() for c in s)
    assert re.search(r"[!@#$%^&*()\-_=+\[\]{}<>?/~]", s)


def test_avaliar_forca():
    """Confere se a função de avaliação de força funciona como esperado."""
    weak = evaluate_strength("abc")
    assert weak["score"] < 3

    strong = evaluate_strength("Aa1!Aa1!Bb2@")
    assert strong["score"] >= 4
