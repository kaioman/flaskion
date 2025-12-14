import { HttpClient } from "./utils.js";

/**
 * 送信ボタンクリック時イベント
 * - 入力欄からプロンプトを取得
 * - サーバーにPOSTで送信
 * - 結果を画面に表示する
 */
async function onSendBtnClick() {
    
    // 入力欄からプロンプト取得
    const prompt = document.getElementById("prompt").value;

    try {
        // サーバーにPOSTリクエストを送信して結果を受け取る
        const data = await HttpClient.post("/test", { prompt });

        // 受け取った結果をHTMLに反映
        document.getElementById("result").innerHTML = `
            <strong>Input(Prompt):</strong> ${data.prompt}<br>
            <strong>Output(key1):</strong> ${data.key1}<br>
            <strong>Output(key2):</strong> ${data.key2}
            `;
        
    } catch (error) {
        // エラー発生時は赤字でエラーメッセージを表示する
        document.getElementById("result").innerHTML = 
            `<span style="color:red;">Error: ${error.message}</span>`;
    }
}

// 送信ボタン(#sendBtn)にクリックイベントを登録
document.getElementById("sendBtn").addEventListener("click", onSendBtnClick);
