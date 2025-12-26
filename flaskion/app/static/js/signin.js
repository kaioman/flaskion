import { HttpClient } from "./utils.js";
import { MessageType } from "./constants.js";
import { MessageManager } from "./components.js";

/**
 * ページロード時処理
 */
document.addEventListener("DOMContentLoaded", function() {
    
    // 入力チェック処理、エラークリア処理
    setupValidation();

    // 続行ボタンの非同期処理
    setupSignin();

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
 * サインイン処理
 */
function setupSignin() {
    const form = document.getElementById("auth-form");
    const messageArea = document.querySelector(".message-area");
    const msgMgr = new MessageManager(messageArea);

    form.addEventListener("submit", async (e) => {

        // 標準送信の停止
        e.preventDefault();

        // payload取得
        const payload = Object.fromEntries(new FormData(form));

        try {
            // サインイン処理(非同期)
            const response = await HttpClient.post("/api/v1/auth/signin", payload);

            // メッセージエリアクリア
            msgMgr.clear();

            // レスポンス判定
            if (response.isSuccess()) {

                // アクセストークン取得
                const token = response.body.data.access_token;
                localStorage.setItem("access_token", token);
                
                // 成功メッセージ表示
                msgMgr.show("サインインに成功しました", MessageType.SUCCESS, "成功");

                // ルートページに遷移する
                window.location.href = "/";
            } else {
                // エラーメッセージ表示
                msgMgr.show(
                    response.body.message || "サインインに失敗しました",
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
        }
    });
}