import { MessageType } from "./constants.js";

/**
 * メッセージマネージャー
 */
export class MessageManager {

    /**
     * コンストラクタ
     * @param {HTMLElment} container - メッセージを表示するDOM
     */
    constructor(container) {
        // コンテナの設定
        if (!container) {
            throw new Error("MessageManager: container が指定されていません");
        }
        this.container = container;
        
        // デフォルトタイトル設定
        this.defaultTitles = {
            [MessageType.ERROR]: "エラーが発生しました",
            [MessageType.WARNING]: "警告",
            [MessageType.SUCCESS]: "成功しました",
            [MessageType.INFO]: "お知らせ",
        }
    }

    /**
     * メッセージを表示する
     * @param {*} msg - 詳細メッセージ
     * @param {*} type - メッセージタイプ
     * @param {*} title - メッセージタイトル(省略可)
     * @param {*} status - HTTPステータス(省略可)
     */
    show(msg, type= MessageType.INFO, title = null, status = null) {

        // メッセージタイトル（左から優先）
        const resolvedTitle = 
            title || this.defaultTitles[type] || "メッセージ";

        // メッセージを表示する
        this.container.innerHTML = 
            `<div class="message-box ${type}">
                <div class="title">
                    ${resolvedTitle}
                    ${status ? `(${status})` : ""}
                </div>
                <div class="message">${msg}</div>
            </div>
        `;
    }

    /**
     * メッセージをクリアする
     */
    clear() {
        this.container.innerHTML = "";
    }
}
