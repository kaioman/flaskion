import { ResponseModel } from "./models.js";

/**
 * HTTP通信を行うためのユーティリティクラス
 * GETとPOSTをサポートする
 */
export class HttpClient {

    /**
     * POSTリクエストを送信する
     * @param {*} url  - リクエスト先のURL
     * @param {*} payload  - 送信するデータ(JSON形式)
     * @returns {Promise<ResponseModel>} - サーバーから返却されたJSONレスポンス
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
            const body = await response.json();

            // レスポンスをJSONとして返却
            return new ResponseModel({
                status: response.status,
                body,
                headers: response.headers,
            });

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
            const body = await response.json();

            // レスポンスをJSONとして返却する
            return { status: response.status, body: body };
        } catch (error) {
            // 通信エラーやサーバーエラーを呼び出し元に伝える
            throw error;
        }
    }
}
