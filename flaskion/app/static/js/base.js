import { HttpClient } from "./utils.js";

/**
 * ページロード時処理
 */
document.addEventListener("DOMContentLoaded", function() {
    
    // ユーザーメニューセットアップ
    setupUserMenu();
    // 認証状態の反映
    setupAuthState();
    // ハンバーガーメニュ―セットアップ
    setupHamburgerMenu();

});

/**
 * ユーザーメニューセットアップ
 */
function setupUserMenu() {
    const userMenu = document.querySelector(".user-menu");

    if (userMenu) {
        userMenu.addEventListener("click", (e) => {
            // 親要素へのクリック伝播を防ぐ
            e.stopPropagation();
            userMenu.classList.toggle("open");
        });
    }

    document.addEventListener("click", () => {
        if (userMenu) {
            userMenu.classList.remove("open");
        }
    });

}

/**
 * ハンバーガーメニューセットアップ
 */
function setupHamburgerMenu() {
    const hamburger = document.getElementById("hamburger");
    const nav = document.querySelector(".nav");

    if (!hamburger || !nav) return;

    // ハンバーガーメニュークリック時イベント
    hamburger.addEventListener("click", (e) => {
        e.stopPropagation();
        nav.classList.toggle("open");
    });

    // 画面のどこかをクリックしたら閉じる
    document.addEventListener("click", () => {
        nav.classList.remove("open");
    });
}

/**
 * JWTを取得するヘルパー
 */
function getToken() {
    return localStorage.getItem("access_token");
}

/**
 * 認証状態に応じてUIを切り替える
 */
async function setupAuthState() {
    const userMenu = document.querySelector(".user-menu");
    const signinLink = document.querySelector(".signin");
    const userIcon = document.querySelector(".auth-area > .user-icon");

    try {
        // サーバーにカレントユーザー情報を問い合わせる
        const res = await HttpClient.get("/api/v1/auth/me", { auth: true });
        
        if (res.isSuccess()) {
            // ログイン状態
            if (signinLink) signinLink.style.display = "none";
            if (userIcon) userIcon.style.display = "none";
            if (userMenu) userMenu.style.display = "flex";

            // JWTからemailを取り出して表示する
            document.getElementById("username").textContent = res.body.data.email;
        } else {
            // 未ログイン状態
            if (signinLink) signinLink.style.display = "block";
            if (userIcon) userIcon.style.display = "inline";
            if (userMenu) userMenu.style.display = "none";
        }
    } catch (err) {
        // 通信エラー時は未ログインとする
        if (signinLink) signinLink.style.display = "block";
        if (userIcon) userIcon.style.display = "inline";
        if (userMenu) userMenu.style.display = "none";
    }
}

/**
 * ログアウト処理(JWTを解除する)
 */
window.logout = function() {
    localStorage.removeItem("access_token");
    window.location.href = "/signin";
}
