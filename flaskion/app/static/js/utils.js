import { ResponseModel } from "./models.js";

/**
 * HTTP通信を行うためのユーティリティクラス
 * GETとPOSTをサポートする
 */
export class HttpClient {

    /**
     * 共通ヘッダー定義
     */
    static defaultHeaders() {
        const token = localStorage.getItem("access_token");
        return token ? { "Authorization": `Bearer ${token}` } : {};
    }

    /**
     * POSTリクエストを送信する
     * @param {string} url  - リクエスト先のURL
     * @param {object} payload  - 送信するデータ(JSON形式)
     * @param {boolean} [options.auth=true] - 認証ヘッダーを付与するかどうか
     * @param {object} [options.headers={}] - 追加ヘッダー(任意)
     * @returns {Promise<ResponseModel>} - サーバーから返却されたJSONレスポンス
     */
    static async post(url, payload, { auth = true, headers = {} } = {}) {
        try {
            // payload判定
            const isFormData = payload instanceof FormData;

            // ヘッダー作成
            const finalHeaders = isFormData
                ? {
                    ...(auth ? HttpClient.defaultHeaders() : {}), 
                    ...headers 
                }
                : {
                    "Content-Type":  "application/json",
                    ...(auth ? HttpClient.defaultHeaders() : {}), 
                    ...headers
                };

            // fetch APIでPOSTリスエストを送信
            const response = await fetch(url, {
                method : "POST",
                headers: finalHeaders,
                body: isFormData ? payload : JSON.stringify(payload)
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
     * @param {string} url - リクエスト先のURL
     * @param {boolean} [options.auth=true] - 認証ヘッダーを付与するかどうか
     * @param {object} [options.headers={}] - 追加ヘッダー(任意)
     * @returns {Promise<object>} - サーバーから返却されたJSONレスポンス
     */
    static async get(url, { auth = true, headers = {} } = {}) {
        try {
            // ヘッダー作成
            const finalHeaders = auth
                ? {
                    ...HttpClient.defaultHeaders(), 
                    ...headers 
                }
                : headers;

            // fetch APIでGETリクエストを送信
            const response = await fetch(url, { 
                method: "GET",
                headers: finalHeaders
            });
            
            // レスポンスチェック
            const body = await response.json();

            // レスポンスをJSONとして返却する
            return { status: response.status, body: body };
        } catch (error) {
            // 通信エラーやサーバーエラーを呼び出し元に伝える
            throw error;
        }
    }

    /**
     * PATCHリクエストを送信する
     * @param {string} url  - リクエスト先のURL
     * @param {object} payload  - 送信するデータ(JSON形式)
     * @param {boolean} [options.auth=true] - 認証ヘッダーを付与するかどうか
     * @param {object} [options.headers={}] - 追加ヘッダー(任意)
     * @returns {Promise<ResponseModel>} - サーバーから返却されたJSONレスポンス
     */
    static async patch(url, payload, { auth = true, headers = {} } = {}) {
        try {
            // ヘッダー作成
            const finalHeaders = auth
                ? {
                    "Content-Type":  "application/json",
                    ...HttpClient.defaultHeaders(), 
                    ...headers 
                }
                : {
                    "Content-Type":  "application/json",
                    ...headers
                };

            // fetch APIでPATCHリスエストを送信
            const response = await fetch(url, {
                method : "PATCH",
                headers: finalHeaders,
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
     * Blob URLを取得する
     * @param {string} url - リクエスト先のURL
     * @param {boolean} [options.auth=true] - 認証ヘッダーを付与するかどうか
     * @param {object} [options.headers={}] - 追加ヘッダー(任意)
     * @returns {Promise<string>} - Blob URL
     */
    static async getBlobUrl(url, { auth = true, headers = {} } = {}) {
        try {
            // ヘッダー作成
            const finalHeaders = auth
                ? {
                    ...HttpClient.defaultHeaders(), 
                    ...headers 
                }
                : headers;

            // Blob URLの生成
            const response = await fetch(url, {
                method: "GET",
                headers: finalHeaders
            });
            const blob = await response.blob();

            // Blob URLを返す
            return URL.createObjectURL(blob);
        } catch (error) {
            // 通信エラーやサーバーエラーを呼び出し元に伝える
            throw error;
        }
    }
}
