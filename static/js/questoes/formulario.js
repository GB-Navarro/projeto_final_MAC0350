const container = document.getElementById("alternativas-container");
const hidden = document.getElementById("alternativas");

const botaoAdicionar = document.getElementById("adicionar-alternativa");
const botaoRemover = document.getElementById("remover-alternativa");

const tipo = document.getElementById("tipo");
const camposMultiplaEscolha = document.getElementById(
    "campos-multipla-escolha"
);

if (tipo && camposMultiplaEscolha) {
    function atualizarCampos() {
        if (tipo.value === "MULTIPLA_ESCOLHA") {
            camposMultiplaEscolha.style.display = "block";
        } else {
            camposMultiplaEscolha.style.display = "none";
        }
    }

    tipo.addEventListener("change", atualizarCampos);

    atualizarCampos();
}

function atualizarAlternativas() {
    if (!container) return;

    const alternativas =
        container.querySelectorAll(".alternativa-item");

    alternativas.forEach((item, indice) => {
        item.querySelector(".alternativa-label").textContent =
            String.fromCharCode(65 + indice) + ")";
    });

    const lista = [];

    container
        .querySelectorAll(".alternativa-input")
        .forEach((campo) => {
            lista.push(campo.value);
        });
        
    hidden.value = JSON.stringify(lista);
    atualizarPreviewAlternativas();
}

function atualizarPreviewAlternativas() {
    const preview = document.getElementById("preview-alternativas");

    if (!preview) {
        return;
    }

    preview.innerHTML = "";

    const campos =
        container.querySelectorAll(".alternativa-input");

    campos.forEach((campo, indice) => {
        const letra = String.fromCharCode(65 + indice);

        const linha = document.createElement("div");
        linha.classList.add("mb-2");

        linha.innerHTML = `
            <strong>${letra})</strong> ${campo.value}
        `;

        preview.appendChild(linha);
    });

    renderMathInElement(preview, {
        delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "\\[", right: "\\]", display: true },
            { left: "$", right: "$", display: false },
            { left: "\\(", right: "\\)", display: false },
        ],
        throwOnError: false,
    });
}

container
    ?.querySelectorAll(".alternativa-input")
    .forEach((campo) => {
        campo.addEventListener("input", atualizarAlternativas);
    });

atualizarAlternativas();

if (botaoAdicionar) {
    botaoAdicionar.addEventListener("click", () => {
        const item = document.createElement("div");
        item.className = "alternativa-item mb-2";

        item.innerHTML = `
            <label class="alternativa-label"></label>
            <textarea
                class="alternativa-input"
                rows="2"
            ></textarea>
        `;

        container.appendChild(item);

        item
            .querySelector(".alternativa-input")
            .addEventListener("input", atualizarAlternativas);

        atualizarAlternativas();
    });
}

if (botaoRemover) {
    botaoRemover.addEventListener("click", () => {
        const alternativas =
            container.querySelectorAll(".alternativa-item");

        if (alternativas.length <= 2)
            return;

        alternativas[alternativas.length - 1].remove();

        atualizarAlternativas();
    });
}