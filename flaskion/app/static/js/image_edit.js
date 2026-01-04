import { HttpClient } from "./utils.js";
import { MessageType } from "./constants.js";
import { MessageManager } from "./components.js";

/**
 * ページロード時処理
 */
document.addEventListener("DOMContentLoaded", function() {
    
    // 遷移元から送られてきた画像をプレビューにセットする
    loadEditImage();

    // 入力チェック、リセット処理
    setupValidation();

    // アップロード画像のプレビュー処理
    setupImagePreview();

    // 画像編集ボタンの非同期処理
    setupImageEdit();

});

/**
 * 遷移元から送られてきた画像をプレビューにセットする
 */
async function loadEditImage() {
    const params = new URLSearchParams(window.location.search);
    const src = params.get("src");

    // ギャラリー経由でない場合は処理を抜ける
    if (!src) {
        return;
    }

    // Blob URLを取得
    const blobUrl = await HttpClient.getBlobUrl(src);

    // DOM要素取得
    const previewImage = document.getElementById("previewImage");
    const previewPlaceholder = document.getElementById("previewPlaceholder");
    const fileNameInline = document.getElementById("fileNameInline");
    const fileName = document.getElementById("fileName");
    const sourceImageUrl = document.getElementById("sourceImageUrl");
    const sourceImage = document.getElementById("sourceImage");

    // プレビュー画像を表示
    previewImage.src = blobUrl;
    previewImage.style.display = "block";
    previewPlaceholder.style.display = "none";

    // ファイル名を抽出して表示
    const extractedName = extractedFileName(src);
    fileNameInline.textContent = extractedName;
    fileName.textContent = extractedName;

    // 画像をhiddenフィールドにセットする
    sourceImageUrl.value = src;
    const blob = await HttpClient.getBlob(src);
    const file = new File([blob], extractedFileName(src), { type: blob.type });

    // FormDataに入れるためにinput.filesを差し替える
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    sourceImage.files = dataTransfer.files;
}

/**
 * API URLからファイル名を抽出する
 * @param {string} path ファイルパス
 * @returns ファイル名
 */
function extractedFileName(path) {
    return path.split("/").pop();
}

/**
 * 入力チェック、リセット処理
 */
function setupValidation() {
    const form = document.querySelector(".edit-form");
    const promptInput = form.querySelector("#prompt");
    const errorEl = form.querySelector(".error-message");
    
    // リセット時にエラーをクリアする
    form.addEventListener("reset", function() {
        if (errorEl) {
            errorEl.textContent = "";
        }
    });

    // 入力時にエラーをクリアする
    promptInput.addEventListener("input", function() {
        if (errorEl && promptInput.value.trim() != "") {
            errorEl.textContent = "";
        }
    });

}

/**
 * アップロード画像のプレビュー表示
 */
function setupImagePreview() {
    const input = document.querySelector("#sourceImage");
    const img = document.querySelector("#previewImage");
    const palceholder = document.querySelector("#previewPlaceholder");
    const fileSelectBtn = document.querySelector("#fileSelectBtn");
    const fileNameInline = document.querySelector("#fileNameInline");

    // ファイル選択ボタン -> inputクリック
    fileSelectBtn.addEventListener("click", () => {
        input.click();
    });

    // ファイル選択時
    input.addEventListener("change", () => {

        // ファイル選択
        const file = input.files[0];
        if (!file) {
            img.style.display = "none";
            palceholder.style.display = "block";
            img.src = "";
            fileNameInline.textContent = "";
            return;
        }

        // ファイル名表示
        fileNameInline.textContent = `ファイル名: ${file.name}`;

        // プレビュー表示
        const reader = new FileReader();
        reader.onload = e => {
            img.src = e.target.result;
            img.style.display = "block";
            palceholder.style.display = "none";
        };
        reader.readAsDataURL(file);

    });
}

/**
 * 画像生成ボタンの非同期処理
 */
function setupImageEdit() {
    const form = document.querySelector(".edit-form");
    const editBtn = document.getElementById("editBtn");
    const overlay = document.getElementById("overlay");
    const messageArea = document.querySelector(".message-area");
    const resultList = document.querySelector(".result-list");
    /** @type {HTMLTemplateElement} */
    const template = document.getElementById("result-card-template");
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");
    const closeModal = document.querySelector(".close-modal");

    // メッセージマネージャーインスタンス
    const msgMgr = new MessageManager(messageArea);

    // 生成結果クリック時イベントハンドラ追加
    resultList.addEventListener("click", async (e) =>{

        // ボタン取得
        const btn = e.target.closest("button");
        if (!btn) return;

        // カード取得
        const card = btn.closest(".result-card");
        if (!card) return;

        // 画像パス取得
        const relative = card.dataset.path;
        if (!relative) return;

        // ダウンロードボタンクリック時
        if (btn.classList.contains("download-btn")) {

            // blob URL生成
            const apiUrl = card.dataset.path;
            const objcetUrl = await HttpClient.getBlobUrl(apiUrl);

            // ダウンロードリンク設定
            const a = document.createElement("a");
            a.href = objcetUrl;
            a.download = apiUrl.split("/").pop();
            a.click();

            // メモリ開放
            URL.revokeObjectURL(objcetUrl);
        }

        // 画像拡大ボタンクリック時
        if (btn.classList.contains("preview-btn")) {

            // blob URL生成
            const objcetUrl = await HttpClient.getBlobUrl(card.dataset.path);

            // 画像拡大モーダル表示
            modal.style.display = "block";
            modalImg.src = objcetUrl;
        }

    });

    // 画像編集ボタンクリック時イベントハンドラ追加
    editBtn.addEventListener("click", async function(e) {

        // フォームの通常送信を止める
        e.preventDefault();

        overlay.style.display = "flex";
        editBtn.disabled = true;

        // 入力値を回収
        const formData = new FormData(form);

        try {
            // サーバーにPOSTリクエストを送信して結果を受け取る
            const response = await HttpClient.post("/api/v1/image_edit", formData);

            // メッセージをクリア
            msgMgr.clear();

            // Httpリクエストコード判定
            if (response.isSuccess()) {

                response.body.data.generated.forEach(async (path) => {
                    
                    // カードテンプレート複製
                    const card = template.content.cloneNode(true);
                    
                    // 画像パス取得(blob URL生成)
                    const objcetUrl = await HttpClient.getBlobUrl(path);

                    // 画像設定
                    const img = card.querySelector(".result-img");
                    img.src = objcetUrl;

                    // カードにパスを保持
                    const root = card.querySelector(".result-card");
                    root.dataset.path = path;

                    // DOMに追加
                    resultList.appendChild(card);
                });
                
                // 成功メッセージ表示
                msgMgr.show("画像編集処理が成功しました", MessageType.SUCCESS, "成功");

            } else if (response.isBadRequest()) {
                // プロンプト未入力メッセージ表示
                msgMgr.show(response.body.message, MessageType.WARNING, "入力エラー", response.status);
            } else if (response.isUnauthorized()) {
                // 未認証であることを通知するメッセージ表示
                msgMgr.show(response.body.message, MessageType.WARNING, "認証エラー", response.status);
                // 未認証の場合はログインページへ遷移する
                setTimeout(() => {
                    window.location.href = "/signin";
                }, 800);
            } else {
                // 内部エラーメッセージ表示
                msgMgr.show(response.body.message, MessageType.ERROR, "サーバー側でエラーが発生しました", response.status);
            }
        } catch (err) {
            msgMgr.show(err, MessageType.ERROR, "通信エラーが発生しました");
            console.error(err);
        } finally {
            overlay.style.display = "none";
            editBtn.disabled = false;
        }
    });

    // モーダルを閉じる
    closeModal.onclick = () => modal.style.display = "none";
    modal.onclick = () => modal.style.display = "none";
}
