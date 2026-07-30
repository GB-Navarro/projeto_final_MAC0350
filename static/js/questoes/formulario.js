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