import re
from password_generator.generator import generate_password, evaluate_strength

def test_gerar_senha_tamanho():
    s = generate_password(length=12)
    assert len(s) == 12

def test_gerar_senha_contem_tipos():
    s = generate_password(length=10, use_upper=True, use_lower=True, use_digits=True, use_symbols=True)
    assert any(c.islower() for c in s)
    assert any(c.isupper() for c in s)
    assert any(c.isdigit() for c in s)
    assert re.search(r"[!@#$%^&*()\-_=+\[\]{}<>?/~]", s)

def test_avaliar_forca():
    weak = evaluate_strength("abc")
    assert weak["score"] < 3
    strong = evaluate_strength("Aa1!Aa1!Bb2@")
    assert strong["score"] >= 4
