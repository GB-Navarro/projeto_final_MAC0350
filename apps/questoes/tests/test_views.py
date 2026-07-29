import pytest
from django.urls import reverse
from model_bakery import baker
from django.utils import timezone
from bs4 import BeautifulSoup

from apps.questoes.models import Questao


@pytest.mark.django_db
class TestCriarQuestaoView:

    def test_admin_logado_cria_questao_dissertativa(
        self,
        client_admin,
    ):
        # Arrange
        dados = {
            "tipo": "DISSERTATIVA",
            "enunciado": "Explique a fotossíntese.",
            "solucao": "Processo realizado pelas plantas.",
        }

        # Act
        response = client_admin.client.post(
            reverse("questoes:criar_questao"),
            dados,
        )

        # Assert
        assert response.status_code == 302

        questao = Questao.objects.get(
            enunciado=dados["enunciado"]
        )

        assert questao.criado_por == client_admin.usuario

@pytest.mark.django_db
class TestListarQuestoesView:

    def test_admin_logado_consulta_questoes(
        self,
        client_admin,
    ):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
        )

        # Act
        response = client_admin.client.get(
            reverse("questoes:lista")
        )

        # Assert
        assert response.status_code == 200
        assert questao in response.context["questoes"]
    
    def test_listagem_exibe_dados_de_revisao(
        self,
        client_admin,
    ):
        # Arrange
        revisor = baker.make(
            "contas.Usuario",
            tipo="ADM",
        )

        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
            revisado_por=revisor,
            revisado_em=timezone.now(),
        )

        # Act
        response = client_admin.client.get(
            reverse("questoes:lista")
        )

        # Assert
        assert response.status_code == 200

        questao_listada = response.context["questoes"].get(
            id=questao.id
        )

        assert questao_listada.revisado_por == revisor
        assert questao_listada.revisado_em is not None

@pytest.mark.django_db
class TestTelaListagemQuestoes:

    def test_tela_exibe_questoes(
        self,
        client_admin,
    ):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
            enunciado="Qual é a capital do Brasil?",
        )

        # Act
        response = client_admin.client.get(
            reverse("questoes:lista")
        )

        # Assert
        assert response.status_code == 200
        assert questao.enunciado.encode() in response.content
    
    def test_tela_exibe_informacoes_de_revisao(
        self,
        client_admin,
    ):
        # Arrange
        revisor = baker.make(
            "contas.Usuario",
            tipo="ADM",
            first_name="João",
        )

        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
            enunciado="Questão revisada",
            revisado_por=revisor,
            revisado_em=timezone.now(),
        )

        # Act
        response = client_admin.client.get(
            reverse("questoes:lista")
        )

        # Assert
        html = response.content.decode()

        assert "Revisada por" in html
        assert "João" in html

@pytest.mark.django_db
class TestEditarQuestaoView:

    def test_admin_edita_questao_de_outro_admin(
        self,
        client_admin,
        outro_admin_aprovado,
    ):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=outro_admin_aprovado.usuario,
            tipo="DISSERTATIVA",
            enunciado="Enunciado antigo",
            solucao="Solução antiga",
        )

        dados = {
            "tipo": "DISSERTATIVA",
            "enunciado": "Enunciado atualizado",
            "solucao": "Solução atualizada",
        }

        # Act
        response = client_admin.client.post(
            reverse("questoes:editar_questao", args=[questao.id]),
            dados,
        )

        # Assert
        assert response.status_code == 302

        questao.refresh_from_db()

        assert questao.enunciado == "Enunciado atualizado"
        assert questao.solucao == "Solução atualizada"

@pytest.mark.django_db
class TestRevisarQuestaoTela:

    def test_tela_exibe_status_da_revisao(
        self,
        client_admin,
    ):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
        )

        # Antes da revisão
        response = client_admin.client.get(
            reverse("questoes:lista")
        )

        html = response.content.decode()

        assert "Não revisada" in html
        assert "Revisada por" not in html
        assert "Marcar como revisada" in html

        # Act
        client_admin.client.post(
            reverse("questoes:revisar", args=[questao.id]),
        )

        # Depois da revisão
        response = client_admin.client.get(
            reverse("questoes:lista")
        )

        html = response.content.decode()

        questao.refresh_from_db()

        # Assert
        assert "Não revisada" not in html
        assert "Revisada por" in html
        assert "Marcar como revisada" not in html

        nome_ou_email = (
            client_admin.usuario.first_name
            or client_admin.usuario.email
        )

        assert nome_ou_email in html
        assert str(questao.revisado_em.year) in html

@pytest.mark.django_db
class TestFormularioCriarQuestao:

    def test_formulario_exibe_campos_basicos(
        self,
        client_admin,
    ):
        # Act
        response = client_admin.client.get(
            reverse("questoes:criar_questao")
        )

        # Assert
        assert response.status_code == 200

        html = response.content.decode()

        assert "enunciado" in html
        assert "solucao" in html
        assert "tipo" in html

    def test_formulario_exibe_campos_de_multipla_escolha(
        self,
        client_admin,
    ):
        # Act
        response = client_admin.client.get(
            reverse("questoes:criar_questao")
        )

        # Assert
        assert response.status_code == 200

        html = response.content.decode()

        assert "alternativas" in html
        assert "gabarito" in html

    def test_formulario_inicia_campos_de_multipla_escolha_ocultos(
        self,
        client_admin,
    ):
        # Act
        response = client_admin.client.get(
            reverse("questoes:criar_questao")
        )

        # Assert
        assert response.status_code == 200

        html = response.content.decode()

        assert 'id="alternativas"' in html
        assert 'id="gabarito"' in html
        assert 'oculto' in html

    def test_admin_logado_cria_questao_multipla_escolha_pelo_formulario(
        self,
        client_admin,
    ):
        response = client_admin.client.post(
            reverse("questoes:criar_questao"),
            {
                "tipo": "MULTIPLA_ESCOLHA",
                "enunciado": "Pergunta",
                "solucao": "Resposta",
                "alternativas": '{"A":"x","B":"y"}',
                "gabarito": "A",
            },
        )

        assert response.status_code == 302

        questao = Questao.objects.get(
            enunciado="Pergunta"
        )

        assert questao.alternativas["A"] == "x"

@pytest.mark.django_db
class TestFormularioEditarQuestao:

    def test_formulario_edicao_carrega_valores_atuais(
        self,
        client_admin,
    ):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
            tipo="DISSERTATIVA",
            enunciado="Enunciado antigo",
            solucao="Solução antiga",
        )

        # Act
        response = client_admin.client.get(
            reverse(
                "questoes:editar_questao",
                args=[questao.id],
            )
        )

        # Assert
        assert response.status_code == 200

        html = response.content.decode()

        assert "Enunciado antigo" in html
        assert "Solução antiga" in html
    
    def test_formulario_edicao_carrega_alternativas_atuais(
        self,
        client_admin,
    ):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
            tipo="MULTIPLA_ESCOLHA",
            alternativas={
                "A": "Primeira alternativa",
                "B": "Segunda alternativa",
            },
            gabarito="A",
        )

        # Act
        response = client_admin.client.get(
            reverse(
                "questoes:editar_questao",
                args=[questao.id],
            )
        )

        # Assert
        assert response.status_code == 200

        soup = BeautifulSoup(
            response.content,
            "html.parser",
        )

        alternativas = soup.find(
            "textarea",
            {"name": "alternativas"},
        )

        assert alternativas is not None
        assert "Primeira alternativa" in alternativas.text
        assert "Segunda alternativa" in alternativas.text

    def test_formulario_edicao_salva_alteracoes(
        self,
        client_admin,
    ):
        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
            enunciado="Antigo",
        )

        response = client_admin.client.post(
            reverse(
                "questoes:editar_questao",
                args=[questao.id],
            ),
            {
                "tipo": "DISSERTATIVA",
                "enunciado": "Novo",
                "solucao": "Nova solução",
            },
        )

        assert response.status_code == 302

        questao.refresh_from_db()

        assert questao.enunciado == "Novo"

    def test_edicao_altera_questao_dissertativa_para_multipla_escolha(
        self,
        client_admin,
    ):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
            tipo="DISSERTATIVA",
            enunciado="Qual é a capital do Brasil?",
            solucao="Brasília.",
        )

        # Act
        response = client_admin.client.post(
            reverse(
                "questoes:editar_questao",
                args=[questao.id],
            ),
            {
                "tipo": "MULTIPLA_ESCOLHA",
                "enunciado": "Qual é a capital do Brasil?",
                "solucao": "Brasília.",
                "alternativas": '{"A": "São Paulo", "B": "Brasília", "C": "Rio de Janeiro"}',
                "gabarito": "B",
            },
        )

        assert response.status_code == 302

        response = client_admin.client.get(
            reverse(
                "questoes:editar_questao",
                args=[questao.id],
            )
        )

        # Assert
        assert response.status_code == 200

        soup = BeautifulSoup(
            response.content,
            "html.parser",
        )

        # Verifica tipo selecionado
        tipo = soup.find(
            "select",
            {"name": "tipo"},
        )

        opcao_selecionada = tipo.find(
            "option",
            selected=True,
        )

        assert opcao_selecionada["value"] == "MULTIPLA_ESCOLHA"

        # Verifica campos preenchidos
        alternativas = soup.find(
            "textarea",
            {"name": "alternativas"},
        )

        assert "São Paulo" in alternativas.text
        assert "Brasília" in alternativas.text
        assert "Rio de Janeiro" in alternativas.text

        gabarito = soup.find(
            "input",
            {"name": "gabarito"},
        )

        assert gabarito["value"] == "B"

    def test_edicao_altera_questao_multipla_escolha_para_dissertativa(
        self,
        client_admin,
    ):
        # Arrange
        questao = baker.make(
            "questoes.Questao",
            criado_por=client_admin.usuario,
            tipo="MULTIPLA_ESCOLHA",
            enunciado="Qual é a capital do Brasil?",
            alternativas={
                "A": "São Paulo",
                "B": "Brasília",
                "C": "Rio de Janeiro",
            },
            gabarito="B",
        )

        # Act
        response = client_admin.client.post(
            reverse(
                "questoes:editar_questao",
                args=[questao.id],
            ),
            {
                "tipo": "DISSERTATIVA",
                "enunciado": "Qual é a capital do Brasil?",
                "solucao": "Brasília.",
            },
        )

        assert response.status_code == 302

        response = client_admin.client.get(
            reverse(
                "questoes:editar_questao",
                args=[questao.id],
            )
        )

        # Assert
        assert response.status_code == 200

        soup = BeautifulSoup(
            response.content,
            "html.parser",
        )

        # Verifica tipo selecionado
        tipo = soup.find(
            "select",
            {"name": "tipo"},
        )

        opcao_selecionada = tipo.find(
            "option",
            selected=True,
        )

        assert opcao_selecionada["value"] == "DISSERTATIVA"

        # Verifica solução carregada
        solucao = soup.find(
            "textarea",
            {"name": "solucao"},
        )

        assert solucao.text.strip() == "Brasília."

        # Verifica que campos específicos de múltipla escolha não estão ativos
        campos_multipla = soup.find(
            "div",
            {"id": "campos-multipla-escolha"},
        )

        assert "oculto" in campos_multipla["class"]

@pytest.mark.django_db
class TestPreviewLatex:
    def test_formulario_possui_preview_do_enunciado(
        self,
        client_admin,
    ):
        response = client_admin.client.get(
            reverse("questoes:criar_questao")
        )

        assert response.status_code == 200

        html = response.content.decode()

        assert 'id="preview-enunciado"' in html

    def test_formulario_possui_preview_da_solucao(
        self,
        client_admin,
    ):
        response = client_admin.client.get(
            reverse("questoes:criar_questao")
        )

        assert response.status_code == 200

        html = response.content.decode()

        assert 'id="preview-solucao"' in html

    def test_formulario_carrega_script_de_preview_latex(
        self,
        client_admin,
    ):
        response = client_admin.client.get(
            reverse("questoes:criar_questao")
        )

        assert response.status_code == 200

        html = response.content.decode()

        assert "latex_preview.js" in html

class TestAutorizacaoQuestoes:

    def test_aluno_nao_pode_acessar_lista(
        self,
        client_aluno,
    ):
        response = client_aluno.client.get(
            reverse("questoes:lista")
        )

        assert response.status_code == 403


    def test_aluno_nao_pode_acessar_formulario_criar(
        self,
        client_aluno,
    ):
        response = client_aluno.client.get(
            reverse("questoes:criar_questao")
        )

        assert response.status_code == 403


    def test_aluno_nao_pode_editar_questao(
        self,
        client_aluno,
    ):
        questao = baker.make(
            "questoes.Questao",
        )

        response = client_aluno.client.get(
            reverse(
                "questoes:editar_questao",
                args=[questao.id],
            )
        )

        assert response.status_code == 403


    def test_aluno_nao_pode_revisar_questao(
        self,
        client_aluno,
    ):
        questao = baker.make(
            "questoes.Questao",
        )

        response = client_aluno.client.post(
            reverse(
                "questoes:revisar",
                args=[questao.id],
            )
        )

        assert response.status_code == 403