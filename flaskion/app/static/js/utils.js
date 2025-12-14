
/**
 * HTTP通信を行うためのユーティリティクラス
 * GETとPOSTをサポートする
 */
export class HttpClient {

    /**
     * POSTリクエストを送信する
     * @param {*} url  - リクエスト先のURL
     * @param {*} payload  - 送信するデータ(JSON形式)
     * @returns {Promise<object>} - サーバーから返却されたJSONレスポンス
     */
    static async post(url, payload) {
        try {
            // fetch APIでPOSTリスエストを送信
            const response = await fetch(url, {
                method : "POST",
                headers: { "Content-Type":  "application/json" },
                body: JSON.stringify(payload)
            });
            
            // レスポンスチェック。正常でない場合はエラーを投げる
            if (!response.ok) {
                throw new Error("Server Error: " + response.status);
            }
            
            // レスポンスをJSONとして返却
            return await response.json();
        } catch (error) {
            // 通信エラーやサーバーエラーを呼び出し元に伝える
            throw error;
        }
    }

    /**
     * GETリクエストを送信する
     * @param {*} url - リクエスト先のURL
     * @returns {Promise<object>} - サーバーから返却されたJSONレスポンス
     */
    static async get(url) {
        // fetch APIでGETリクエストを送信
        const response = await fetch(url, { method: "GET" });
        
        // レスポンスチェック。正常でない場合はエラーを投げる
        if (!response.ok) {
            throw new Error("Server Error: " + response.status);
        }

        // レスポンスをJSONとして返却する
        return await response.json();
    }
}
