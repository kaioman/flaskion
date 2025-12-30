import { HttpClient } from "./utils.js";
import { MessageType } from "./constants.js";
import { MessageManager } from "./components.js";

/**
 * ページロード時処理
 */
document.addEventListener("DOMContentLoaded", function() {
    
    // 入力チェック、リセット処理
    setupValidation();

    // 画像生成ボタンの非同期処理
    setupImageGenerateion();

});

/**
 * 入力チェック、リセット処理
 */
function setupValidation() {
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

}

/**
 * 画像生成ボタンの非同期処理
 */
function setupImageGenerateion() {
    const form = document.querySelector(".gen-form");
    const generateBtn = document.getElementById("generateBtn");
    const overlay = document.getElementById("overlay");
    const messageArea = document.querySelector(".message-area");
    const resultList = document.querySelector(".result-list");
    /** @type {HTMLTemplateElement} */
    const template = document.getElementById("result-card-template");
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");
    const closeModal = document.querySelector(".close-modal");

    // メッセージマネージャーインスタンス
    const msgMgr = new MessageManager(messageArea);

    // 生成結果クリック時イベントハンドラ追加
    resultList.addEventListener("click", async (e) =>{

        // ボタン取得
        const btn = e.target.closest("button");
        if (!btn) return;

        // カード取得
        const card = btn.closest(".result-card");
        if (!card) return;

        // 画像パス取得
        const relative = card.dataset.path;
        if (!relative) return;

        // ダウンロードボタンクリック時
        if (btn.classList.contains("download-btn")) {

            // blob URL生成
            const apiUrl = card.dataset.path;
            const objcetUrl = await HttpClient.getBlobUrl(apiUrl);

            // ダウンロードリンク設定
            const a = document.createElement("a");
            a.href = objcetUrl;
            a.download = apiUrl.split("/").pop();
            a.click();

            // メモリ開放
            URL.revokeObjectURL(objcetUrl);
        }

        // 画像拡大ボタンクリック時
        if (btn.classList.contains("preview-btn")) {

            // blob URL生成
            const objcetUrl = await HttpClient.getBlobUrl(card.dataset.path);

            // 画像拡大モーダル表示
            modal.style.display = "block";
            modalImg.src = objcetUrl;
        }

    });

    // 画像生成ボタンクリック時イベントハンドラ追加
    generateBtn.addEventListener("click", async function() {
        overlay.style.display = "flex";
        generateBtn.disabled = true;

        // 入力値を回収
        const payload = Object.fromEntries(new FormData(form));

        try {
            // サーバーにPOSTリクエストを送信して結果を受け取る
            const response = await HttpClient.post("/api/v1/image_gen", payload);

            // 結果リストをクリア
            msgMgr.clear();

            // Httpリクエストコード判定
            if (response.isSuccess()) {

                response.body.data.generated.forEach(async (path) => {
                    
                    // カードテンプレート複製
                    const card = template.content.cloneNode(true);
                    
                    // 画像パス取得(blob URL生成)
                    const objcetUrl = await HttpClient.getBlobUrl(path);

                    // 画像設定
                    const img = card.querySelector(".result-img");
                    img.src = objcetUrl;

                    // カードにパスを保持
                    const root = card.querySelector(".result-card");
                    root.dataset.path = path;

                    // DOMに追加
                    resultList.appendChild(card);
                });
                
                // 成功メッセージ表示
                msgMgr.show("画像生成処理が成功しました", MessageType.SUCCESS, "成功");

            } else if (response.isBadRequest()) {
                // プロンプト未入力メッセージ表示
                msgMgr.show(response.body.message, MessageType.WARNING, "入力エラー", response.status);
            } else {
                // 内部エラーメッセージ表示
                msgMgr.show(response.body.message, MessageType.ERROR, "サーバー側でエラーが発生しました", response.status);
            }
        } catch (err) {
            msgMgr.show(err, MessageType.ERROR, "通信エラーが発生しました");
            console.error(err);
        } finally {
            overlay.style.display = "none";
            generateBtn.disabled = false;
        }
    });

    // モーダルを閉じる
    closeModal.onclick = () => modal.style.display = "none";
    modal.onclick = () => modal.style.display = "none";
}
