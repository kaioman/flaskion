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
            
            // レスポンスチェック
            const data = await response.json();

            // レスポンスをJSONとして返却
            return { status: response.status, body: data };
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
        try {
            // fetch APIでGETリクエストを送信
            const response = await fetch(url, { method: "GET" });
            
            // レスポンスチェック
            const data = await response.json();

            // レスポンスをJSONとして返却する
            return { status: response.status, body: data };
        } catch (error) {
            // 通信エラーやサーバーエラーを呼び出し元に伝える
            throw error;
        }
    }
}

/**
 * HTTP ステータスコード
 */
export const HttpStatus = {

    // リクエスト成功
    OK: 200,

    // クライアント側の入力エラー（バリデーションエラーなど）
    BAD_REQUEST: 400,

    // 認証が必要（ログインしていない）
    UNAUTHORIZED: 401,

    // 認可エラー（ログインしていても権限が足りない）
    FORBIDDEN: 403,

    // リソースが存在しない
    NOT_FOUND: 404,

    // サーバー内部エラー（予期しない例外など）
    INTERNAL_SERVER_ERROR: 500,

}