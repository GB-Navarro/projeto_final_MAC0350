function configurarPreview(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);

    if (!input || !preview) {
        return;
    }

    function atualizarPreview() {
        try {
            katex.render(
                input.value,
                preview,
                {
                    throwOnError: false,
                    displayMode: true,
                },
            );
        } catch {
            preview.textContent = input.value;
        }
    }

    input.addEventListener(
        "input",
        atualizarPreview,
    );

    atualizarPreview();
}

configurarPreview(
    "enunciado",
    "preview-enunciado",
);

configurarPreview(
    "solucao",
    "preview-solucao",
);