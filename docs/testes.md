# Guia de Testes — Plataforma OBCON

> Como testamos. Simples para o humano, claro para a IA.
> Stack de testes: **pytest-django** + **model_bakery**.
> Tarefas → [backlog.md](backlog.md) · Convenções (AI) → [CLAUDE.md](../CLAUDE.md) · Setup → [README.md](../README.md)

---

## 1. O ciclo de testes (para humanos)

Para **cada tarefa** do [backlog.md](backlog.md), siga estes 5 passos, sempre na mesma ordem:

```
  ┌─────────────────────────────────────────────────────────┐
  │                                                           │
  ▼                                                           │
1. ESCREVER o critério   →   2. GERAR o teste   →   3. RODAR  │
   (você, Template A)          (IA, Template B)       (falha) │
                                                          │    │
                          5. CONFERIR  ◄── 4. IMPLEMENTAR ◄┘    │
                          o teste          até passar           │
                             │                                  │
                             └──── próxima tarefa ──────────────┘
```

1. **Escrever o critério** — copie [criterios/TEMPLATE.md](criterios/TEMPLATE.md), salve como `criterios/<id-da-tarefa>.md` (ex: `criterios/F1-3.md`) e preencha. *Antes de qualquer código.*
2. **Gerar o teste** — cole o critério no prompt (Template B) e a IA escreve o teste.
3. **Rodar e ver falhar** — `pytest`. O teste **tem que falhar** (a feature ainda não existe). Se passar, está errado.
4. **Implementar** — escreva o mínimo de código até o teste passar.
5. **Conferir o teste** — leia e confirme que ele cobre o critério (não só "o que o código faz").

> **Por que você confere?** Se a IA escrevesse o teste a partir do código, ele só repetiria o código. O **critério** (passo 1, seu) é a fonte da verdade. A IA só faz a digitação.

**Quem faz o quê:**

| Passo | Humano | IA |
|---|---|---|
| 1. Critério | ✅ escreve | — |
| 2. Gerar teste | cola o prompt | ✅ escreve |
| 3. Rodar | ✅ | — |
| 4. Implementar | ✅ (ou IA, com revisão) | apoia |
| 5. Conferir | ✅ valida | — |

---

## 2. Quando escrever os testes

Sempre no **início da tarefa**, antes do código.

| Fase | Testes a escrever |
|---|---|
| 1 — Contas e acesso | cadastro de aluno gera código; admin novo fica pendente e não loga; aprovação libera o login; login/logout |
| 2 — Questões | criar e editar questão; marcar como revisada grava quem e quando |

---

## 3. Templates para preencher

**A** = a regra (humano). **B** = o prompt para a IA (recebe o A). **C** = o formato de saída.

### Template A — Critério de aceitação

> Salve em `docs/criterios/<id-da-tarefa>.md` (ex: `F1-3.md`). Use [criterios/TEMPLATE.md](criterios/TEMPLATE.md) como ponto de partida.

```gherkin
Funcionalidade: <nome curto>
Regra de negócio: <a regra garantida, em uma frase>

  Cenário: <caso feliz>
    Dado <estado inicial / quem age>
    Quando <ação>
    Então <resultado esperado observável>

  Cenário: <caso de erro/borda>
    Dado <estado inicial>
    Quando <ação inválida>
    Então <a operação é rejeitada / status esperado>
```

Exemplo preenchido:
```gherkin
Funcionalidade: Aprovação de administrador
Regra de negócio: admin novo só loga depois de aprovado pelo superuser.

  Cenário: admin pendente não consegue logar
    Dado um administrador recém-cadastrado e ainda não aprovado
    Quando ele tenta fazer login
    Então o acesso é negado

  Cenário: após aprovação, o admin loga
    Dado um administrador aprovado pelo superuser
    Quando ele faz login
    Então o acesso é concedido
```

### Template B — Prompt para a IA (cole e preencha)

```
Gere testes automatizados para o projeto OBCON (Django + pytest-django).

Regras obrigatórias:
- Gere os testes A PARTIR dos critérios de aceitação abaixo, NÃO a partir de
  nenhuma implementação. Não invente comportamento que não esteja nos critérios.
- Um cenário = um teste. Nomeie a função test_<cenário em snake_case>.
- Use pytest-django. Marque com @pytest.mark.django_db quando tocar o banco.
- Crie dados com model_bakery: baker.make("app.Modelo", campo=valor).
- Estrutura AAA (Arrange, Act, Assert). Um assert principal por teste.
- Para views, use o Django test client (client.post/get); verifique
  response.status_code e o efeito no banco (obj.refresh_from_db()).
- NÃO teste detalhes internos; teste comportamento observável.

Camada do teste: <unitário (modelo/serviço) | integração (view)>
Arquivo alvo: apps/<app>/tests/test_<algo>.py
Sob teste: <ex.: apps.contas.services / view 'contas:cadastro_aluno'>

Critérios de aceitação:
<cole aqui o Template A preenchido>

Saída: apenas o código do arquivo de teste, com os imports.
```

### Template C — Formato de saída esperado

```python
import pytest
from model_bakery import baker

@pytest.mark.django_db
def test_<nome_do_cenario>():
    # Arrange
    ...
    # Act
    ...
    # Assert
    ...
```

---

## 4. Como rodar

```bash
pytest -q                         # roda tudo
pytest apps/contas -q             # roda um app
pytest -k revisada -q             # por palavra-chave
coverage run -m pytest && coverage report -m
```

Meta: ~80% geral; **100% nas regras de cadastro/aprovação e na marca de revisão**.

---

## 5. Exemplos prontos

**Cadastro de aluno gera código (integração):**
```python
import pytest
from django.urls import reverse
from apps.contas.models import Aluno

@pytest.mark.django_db
def test_cadastro_de_aluno_gera_codigo(client):
    resp = client.post(reverse("contas:cadastro_aluno"), {
        "nome": "Ana", "email": "ana@exemplo.com", "senha": "senha-forte-123",
        "genero": "F", "serie": "1EM", "escola": "Escola X", "tipo_escola": "PUBLICA",
    })
    aluno = Aluno.objects.get(usuario__email="ana@exemplo.com")
    assert aluno.codigo.startswith("E")
```

**Admin pendente não loga; aprovado loga (integração):**
```python
import pytest
from django.urls import reverse
from model_bakery import baker

@pytest.mark.django_db
def test_admin_pendente_nao_loga(client):
    baker.make("contas.Administrador", aprovado=False,
               usuario__email="novo@exemplo.com")
    resp = client.post(reverse("contas:login"),
                       {"email": "novo@exemplo.com", "senha": "x"})
    assert resp.status_code in (200, 403)        # não autenticou
```

**Marcar questão como revisada (integração):**
```python
import pytest
from django.urls import reverse
from model_bakery import baker

@pytest.mark.django_db
def test_marcar_questao_como_revisada(client):
    admin = baker.make("contas.Administrador", aprovado=True)
    questao = baker.make("questoes.Questao")
    client.force_login(admin.usuario)

    resp = client.post(reverse("questoes:revisar", args=[questao.id]))

    questao.refresh_from_db()
    assert questao.revisado_por_id == admin.usuario_id
    assert questao.revisado_em is not None
```

---

## 6. Opcional (só se sobrar tempo)

- **Hypothesis** para gerar entradas variadas de cadastro e checar que o código gerado é sempre único e no formato `Exxxxxx`.
- **mutmut** nas regras de aprovação/revisão: mutante sobrevivente = teste faltando.
