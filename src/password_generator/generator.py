"""
Gerador de senhas seguras.
Funções principais:
- generate_password(...) -> str
- evaluate_strength(senha) -> dict (pontuação simples)
"""
from __future__ import annotations
import string
import secrets
from typing import Dict


DEFAULT_LENGTH = 16


def generate_password(length: int = DEFAULT_LENGTH,
                 use_upper: bool = True,
                 use_lower: bool = True,
                 use_digits: bool = True,
                 use_symbols: bool = True) -> str:
    """
    Gera uma senha aleatória segura usando o módulo `secrets`.

    Args:
        length: comprimento da senha (>=4 recomendado).
        use_upper, use_lower, use_digits, use_symbols: flags para incluir tipos de caracteres.

    Returns:
        senha gerada como string.
    """
    if length < 1:
        raise ValueError("length must be >= 1")

    pool = ""
    if use_lower:
        pool += string.ascii_lowercase
    if use_upper:
        pool += string.ascii_uppercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        # escolha de símbolos "seguros" - evita espaços e alguns que quebram shells por padrão
        pool += "!@#$%^&*()-_=+[]{}<>?/~"

    if not pool:
        raise ValueError("At least one character set must be enabled")

    # Garantir que pelo menos um de cada tipo habilitado apareça na senha
    password_chars = []
    required_sets = []
    if use_lower:
        required_sets.append(secrets.choice(string.ascii_lowercase))
    if use_upper:
        required_sets.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        required_sets.append(secrets.choice(string.digits))
    if use_symbols:
        required_sets.append(secrets.choice("!@#$%^&*()-_=+[]{}<>?/~"))

    # preencher senha com required chars
    password_chars.extend(required_sets)

    # preencher o restante randomicamente
    remaining = length - len(password_chars)
    for _ in range(max(0, remaining)):
        password_chars.append(secrets.choice(pool))

    # embaralhar de forma segura
    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)


def evaluate_strength(senha: str) -> Dict[str, object]:
    """
    Avalia a 'força' da senha com regras simples:
    - presença de tipos de caracteres
    - comprimento
    Retorna um dict com pontuação e dicas.
    """
    score = 0
    tips = []

    length = len(senha)
    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1
    else:
        tips.append("Use pelo menos 8 caracteres (12+ é melhor).")

    # tipos
    if any(c.islower() for c in senha):
        score += 1
    else:
        tips.append("Adicione letras minúsculas.")

    if any(c.isupper() for c in senha):
        score += 1
    else:
        tips.append("Adicione letras maiúsculas.")

    if any(c.isdigit() for c in senha):
        score += 1
    else:
        tips.append("Adicione números.")

    if any(c in "!@#$%^&*()-_=+[]{}<>?/~" for c in senha):
        score += 1
    else:
        tips.append("Adicione símbolos (ex: !@#$%).")

    strength = {0: "Muito fraca", 1: "Fraca", 2: "Razoável", 3: "Boa", 4: "Forte", 5: "Muito forte"}
    # normalizar score em 0..5
    score = max(0, min(5, score))
    return {"score": score, "label": strength.get(score, "Desconhecida"), "tips": tips}
