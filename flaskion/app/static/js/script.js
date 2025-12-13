import { HttpClient } from "./utils.js";

async function onSendBtnClick() {
    
    // プロンプト取得
    const prompt = document.getElementById("prompt").value;

    try {
        const data = await HttpClient.post("/test", { prompt });

        // 結果をHTMLに反映
        document.getElementById("result").innerHTML = `
            <strong>Input(Prompt):</strong> ${data.prompt}<br>
            <strong>Output(key1):</strong> ${data.key1}<br>
            <strong>Output(key2):</strong> ${data.key2}
            `;
        
    } catch (error) {
        document.getElementById("result").innerHTML = 
            `<span style="color:red;">Error: ${error.message}</span>`;
    }
}

document.getElementById("sendBtn").addEventListener("click", onSendBtnClick);
