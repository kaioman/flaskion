import { HttpStatus } from "./constants.js";

/**
 * APIレスポンスモデルクラス
 * 
 * - HttpClientが返すレスポンスを統一フォーマットで保持する
 * - フィールドは拡張前提の設計
 * - ステータスコードに応じた判定メソッドにて処理結果を判定する
 */
export class ResponseModel {

    /**
     * コンストラクタ
     * @param {Object} param0 - レスポンス情報をまとめたオブジェクト
     * @param {number} param0.status - HTTP ステータスコード
     * @param {*} param0.body - レスポンスボディ（JSON パース済み）
     * @param {Headers|null} [param0.headers=null] - fetch の Headers オブジェクト
     * @param {number|null} [param0.timestamp=null] - レスポンス受信時刻（ミリ秒）。未指定なら現在時刻
     */
    constructor({ status, body, headers = null, timestamp = null}) {
        this.status = status;
        this.body = body;
        this.headers = headers;
        this.timestamp = timestamp || Date.now();
    }

    /**
     * レスポンスが HTTP 200（成功）かどうかを判定する。
     * 
     * @returns {boolean} 成功なら true
     */
    isOk() {
        return this.status == HttpStatus.OK;
    }

    /**
     * レスポンスが HTTP 400（クライアント入力エラー）かどうかを判定する。
     * 
     * @returns {boolean} BAD_REQUEST なら true
     */
    isBadRequest() {
        return this.status == HttpStatus.BAD_REQUEST;
    }

    /**
     * レスポンスがサーバーエラー（500 以上）かどうかを判定する。
     * 
     * @returns {boolean} サーバーエラーなら true
     */
    isServerError() {
        return this.status >= HttpStatus.INTERNAL_SERVER_ERROR;
    }
}