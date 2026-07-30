function inicializarPreviewLatex(input) {
    const previewId = input.dataset.preview;
    const preview = document.getElementById(previewId);

    if (!preview) {
        return;
    }

    function atualizar() {
        preview.innerHTML = input.value;

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

    input.addEventListener("input", atualizar);

    atualizar();
}

document
    .querySelectorAll(".latex-input")
    .forEach(inicializarPreviewLatex);
    
window.inicializarPreviewLatex = inicializarPreviewLatex;