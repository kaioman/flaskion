
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

/**
 * メッセージタイプ
 */
export const MessageType = {

    // エラー
    ERROR: "error",

    // 警告
    WARNING: "warning",

    // 成功
    SUCCESS: "success",

    // 情報
    INFO: "info",

};
