document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector(".gen-form");
    const promptInput = form.querySelector("#prompt");
    const errorEl = form.querySelector(".error-message");

    // リセット時にエラーをクリアする
    form.addEventListener("reset", function() {
        if (errorEl) {
            errorEl.textContent = "";
        }
    });

    // 入力時にエラーをクリアする
    promptInput.addEventListener("input", function() {
        if (errorEl && promptInput.value.trim() != "") {
            errorEl.textContent = "";
        }
    });

});
