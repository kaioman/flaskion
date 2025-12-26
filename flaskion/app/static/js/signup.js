import { HttpClient } from "./utils.js";
import { MessageType } from "./constants.js";
import { MessageManager } from "./components.js";

/**
 * ページロード時処理
 */
document.addEventListener("DOMContentLoaded", function() {
    
    // 入力チェック処理、エラークリア処理
    setupValidation();

    // アカウント作成ボタンの非同期処理
    setupSignup();

});

/**
 * 入力チェック、エラークリア処理
 */
function setupValidation() {
    const form = document.getElementById("auth-form");
    const inputs = form.querySelectorAll("input");
    const messageArea = document.querySelector(".message-area");
    const msgMgr = new MessageManager(messageArea);

    inputs.forEach(input => {
        input.addEventListener("input", ()=> {
            msgMgr.clear();
        })
    });

}

/**
 * サインアップ処理
 */
function setupSignup() {
    const form = document.getElementById("auth-form");
    const createAccountBtn = document.getElementById("create_account");
    const overlay = document.getElementById("overlay");
    const messageArea = document.querySelector(".message-area");
    const msgMgr = new MessageManager(messageArea);

    form.addEventListener("submit", async (e) => {

        // 標準送信の停止
        e.preventDefault();

        // payload取得
        const payload = Object.fromEntries(new FormData(form));

        // パスワード（確認）をDOMから直接取得する
        const passwordConfirm = document.getElementById("password_confirm").value;

        // パスワード一致チェック
        if (payload.password !== passwordConfirm) {
            msgMgr.show(
                "パスワードが一致しません",
                MessageType.WARNING,
                "入力エラー"
            );
            return;
        }
        
        // 処理中スピナー表示・押下ボタン非活性
        overlay.style.display = "flex";
        createAccountBtn.disabled = true;

        try {
            // APIへPOSTする(非同期)
            const response = await HttpClient.post("/api/v1/auth/signup", payload);
            
            // メッセージエリアクリア
            msgMgr.clear();

            // レスポンス判定
            if (response.isSuccess()) {
                msgMgr.show(
                    "サインアップに成功しました。サインインページへ移動します。",
                    MessageType.SUCCESS,
                    "成功"
                );

                // 少し待機してから遷移
                setTimeout(() => {
                    window.location.href = "/signin";
                }, 800);

            } else {
                // エラーメッセージ表示
                msgMgr.show(
                    response.body.message || "サインアップに失敗しました",
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
            createAccountBtn.disabled = false;
        }
    });

}