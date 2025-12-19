import { HttpClient, HttpStatus } from "./utils.js";
import { MessageManager, MessageType } from "./components.js";

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

    // メッセージマネージャーインスタンス
    const msgMgr = new MessageManager(messageArea);

    // 画像パス取得
    const extractRelativePath = (path) =>
        `/static/${path.split('static/')[1]}`;

    // 生成結果クリック時イベントハンドラ追加
    resultList.addEventListener("click", (e) =>{

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
            const a = document.createElement("a");
            a.href = relative;
            a.download = "";
            a.click();
        }

        // URLコピーボタンクリック時
        if (btn.classList.contains("urlcopy-btn")) {
            navigator.clipboard.writeText(`${location.origin}${relative}`);
        }

    });

    // 生成ボタンクリック時イベントハンドラ追加
    generateBtn.addEventListener("click", async function() {
        overlay.style.display = "flex";
        generateBtn.disabled = true;

        // 入力値を回収
        const payload = Object.fromEntries(new FormData(form));

        try {
            // サーバーにPOSTリクエストを送信して結果を受け取る
            const {status, body} = await HttpClient.post("/get_gen_image", payload);

            // 結果リストをクリア
            msgMgr.clear();

            // Httpリクエストコード判定
            if (status == HttpStatus.OK) {

                body.generated.forEach(path => {
                    
                    // カードテンプレート複製
                    const card = template.content.cloneNode(true);
                    
                    // 画像パス取得
                    const relative = extractRelativePath(path);

                    // 画像設定
                    const img = card.querySelector(".result-img");
                    img.src = relative;

                    // カードにパスを保持
                    const root = card.querySelector(".result-card");
                    root.dataset.path = relative;

                    // DOMに追加
                    resultList.appendChild(card);
                });
                
                // 成功メッセージ表示
                msgMgr.show("画像生成処理が成功しました", MessageType.SUCCESS, "成功");

            } else if (status == HttpStatus.BAD_REQUEST) {
                // プロンプト未入力メッセージ表示
                msgMgr.show(body.error, MessageType.WARNING, "入力エラー", status);
            } else {
                // 内部エラーメッセージ表示
                msgMgr.show(body.error, MessageType.ERROR, "サーバー側でエラーが発生しました", status);
            }
        } catch (err) {
            msgMgr.show(err, MessageType.ERROR, "通信エラーが発生しました");
            console.error(err);
        } finally {
            overlay.style.display = "none";
            generateBtn.disabled = false;
        }
    })
}
