import { HttpClient } from "./utils.js";
import { MessageType } from "./constants.js";
import { MessageManager } from "./components.js";

/**
 * ページロード時処理
 */
document.addEventListener("DOMContentLoaded", function() {
    
    // 再発行ボタンの非同期処理
    setupRegenerate();

    // 保存ボタンの非同期処理
    setupSaveSettings();

});

/**
 * Uwgen APIキー再発行処理
 */
function setupRegenerate() {
    const regenerateApiKeyBtn = document.getElementById("regenerate-api-key-btn");
    const warning = document.getElementById("uwgen-api-key-warning");
    const messageArea = document.querySelector(".message-area");
    const msgMgr = new MessageManager(messageArea);

    regenerateApiKeyBtn.addEventListener("click", async () => {

        // 処理中スピナー表示・押下ボタン非活性
        overlay.style.display = "flex";
        regenerateApiKeyBtn.disabled = true;

        try {
            // 追加ヘッダー
            const appendHeader = {
                "Authorization": "Bearer " + localStorage.getItem("access_token")
            }

            // APIキー再発行処理(非同期)
            const response = await HttpClient.post(
                "/api/v1/settings/api-key/regenerate", 
                {},
                appendHeader);

            // メッセージエリアクリア
            msgMgr.clear();

            // レスポンス判定
            if (response.isSuccess()) {

                // 発行したAPIキーを取得
                const uwgn_gen_api_key = response.body.data;

                // 発行したAPIキーを画面に表示
                document.getElementById("uwgen-api-key-display").textContent = uwgn_gen_api_key;
                document.getElementById("uwgen-api-key").value = uwgn_gen_api_key;

                // API発行注意メッセージを表示
                warning.textContent = "APIを発行しました。保存ボタンを押して確定してください";
                warning.style.display = "block";

            } else {
                // エラーメッセージ表示
                msgMgr.show(
                    response.body.message || "APIキーの発行に失敗しました",
                    MessageType.ERROR,
                    "エラー",
                    response.status
                );
            }
        } catch (err) {
            // エラーメッセージ表示
            msgMgr.show(
                "通信エラーが発生しました", 
                MessageType.ERROR, 
                "通信エラー"
            );
            console.error(err);
        } finally {
            // 処理中スピナー非表示・押下ボタン活性
            overlay.style.display = "none";
            regenerateApiKeyBtn.disabled = false;
        }
    });
}

/**
 * 保存処理
 */
function setupSaveSettings() {
    const saveSettingsBtn = document.getElementById("save-settings-btn");
    const uwgenHidden = document.getElementById("uwgen-api-key");
    const uwgenOrigin = document.getElementById("original-uwgen-api-key");
    const geminiInput = document.getElementById("gemini-api-key");
    const warning = document.getElementById("uwgen-api-key-warning");
    const messageArea = document.querySelector(".message-area");
    const msgMgr = new MessageManager(messageArea);

    saveSettingsBtn.addEventListener("click", async () => {

        // 処理中スピナー表示・押下ボタン非活性
        overlay.style.display = "flex";
        saveSettingsBtn.disabled = true;

        // 注意メッセージを消す
        warning.style.display = "none";
        
        try {
            // payload
            const payload = {
                uwgen_api_key: uwgenHidden.value || null,
                uwgen_api_key_changed: uwgenHidden.value !== uwgenOrigin.value,
                gemini_api_key_encrypted: geminiInput.value || null,
                gemini_api_key_changed: geminiInput.value.trim() !== "",
            }

            // 追加ヘッダー
            const appendHeader = {
                "Authorization": "Bearer " + localStorage.getItem("access_token")
            }

            // 保存処理(非同期)
            const response = await HttpClient.patch("/api/v1/settings", payload, appendHeader);

            // メッセージエリアクリア
            msgMgr.clear();

            // レスポンス判定
            if (response.isSuccess()) {

                // 成功メッセージ表示
                msgMgr.show("設定の保存に成功しました", MessageType.SUCCESS, "成功");

                // ルートページに遷移する
                setTimeout(() => {
                    window.location.href = "/";
                }, 800);

            } else {
                // エラーメッセージ表示
                msgMgr.show(
                    response.body.message || "設定内容の保存に失敗しました",
                    MessageType.ERROR,
                    "エラー",
                    response.status
                );
            }
        } catch (err) {
            // エラーメッセージ表示
            msgMgr.show(
                "通信エラーが発生しました", 
                MessageType.ERROR, 
                "通信エラー"
            );
            console.error(err);
        } finally {
            // 処理中スピナー非表示・押下ボタン活性
            overlay.style.display = "none";
            saveSettingsBtn.disabled = false;
        }
    });
}