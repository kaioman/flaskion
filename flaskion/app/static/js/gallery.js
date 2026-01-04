import { HttpClient } from "./utils.js";
import { MessageType } from "./constants.js";
import { MessageManager } from "./components.js";

/**
 * ページロード時処理
 */
document.addEventListener("DOMContentLoaded", function() {
    
    // ギャラリーのセットアップ
    setupGallery();

});

/**
 * ギャラリーのセットアップ
 */
function setupGallery() {
    const grid = document.getElementById("galleryGrid");
    const filterBtns = document.querySelectorAll(".filter-btn");
    const sortSelect = document.getElementById("sortSelect");
    const template = document.getElementById("gallery-card-template");
    const loadMoreBtn = document.getElementById("loadMoreBtn");
    const messageArea = document.querySelector(".message-area");

    // メッセージマネージャーインスタンス
    const msgMgr = new MessageManager(messageArea);

    let currentFilter = "all";
    let currentSort = "newest";
    let offset = 0;
    const limit = 20;
    let total = 0;

    // 初回ロード
    loadGallery();

    // フィルタ変更
    filterBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            filterBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            currentFilter = btn.dataset.filter;
            loadGallery();
        });
    });

    // ソート変更
    sortSelect.addEventListener("change", () => {
        currentSort = sortSelect.value;
        loadGallery();
    });

    // もっと見るボタン
    loadMoreBtn.addEventListener("click", () => {
        loadGallery(true);
    });

    // ギャラリー読込
    async function loadGallery(isAppend = false) {

        if (!isAppend) {
            offset = 0;
            grid.innerHTML = "";
        }

        // ギャラリー一覧をリクエスト
        const url = `/api/v1/gallery?type=${currentFilter}&sort=${currentSort}&offset=${offset}&limit=${limit}`;
        const response = await HttpClient.get(
            url,
            { auth: true }
        );

        // メッセージをクリア
        msgMgr.clear();

        // Httpリクエストコード判定
        if (!response.isSuccess()) {
            msgMgr.show(response.body.message, MessageType.ERROR, "画像読込エラー", response.status);
            return;
        }

        // ギャラリーの取得
        const images = response.body.data.images;
        total = response.body.data.total;

        // 画像0件の場合
        if (images.length === 0) {
            grid.innerHTML = "<p class='empty'>画像がありません</p>";
            return;
        }

        // 画像をギャラリーにカード形式で表示
        for (const img of images) {
            const card = await createCard(img);
            grid.appendChild(card);
        }

        // 読み込んだ画像の分だけoffsetを加算
        offset += images.length;

        // 「もっと見る」ボタンの表示制御
        loadMoreBtn.style.display = (offset < total) ? "block" : "none";

    }

    async function createCard(img) {
        const node = template.content.cloneNode(true);
        const card = node.querySelector(".gallery-card");
        const image = node.querySelector(".gallery-img");
        const spinner = node.querySelector(".spinner-image-loading");
        
        // Blob URLを取得
        image.src = "";
        const objectUrl = await HttpClient.getBlobUrl(img.path);

        // 画像読込完了イベント
        image.onload = () => {
            //spinner.style.display = "none";
            card.classList.add("loaded");
            image.style.opacity = "1";
        };

        // 読み込み開始
        image.src = objectUrl;

        const previewBtn = node.querySelector(".preview-btn");
        previewBtn.onclick = (e) => {
            e.stopPropagation();
            openModal(img.path);
        };

        const editBtn = node.querySelector(".edit-btn");
        editBtn.onclick = (e) => {
            e.stopPropagation();
            window.location.href = `/image_edit?src=${encodeURIComponent(img.path)}`;
        };

        card.onclick = () => openModal(img.path);

        return node;
    }

    const modal = document.getElementById("galleryModal");
    const modalImg = document.getElementById("modalImage");
    const closeModal = document.querySelector(".close-modal");

    function openModal(path) {
        modal.style.display = "flex";
        modalImg.src = path;
    }

    closeModal.onclick = () => modal.style.display = "none";
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    })
}