/**
 * ページロード時処理
 */
document.addEventListener("DOMContentLoaded", function() {
    
    // ユーザーメニューセットアップ
    setupUserMenu();
    // 認証状態の反映
    setupAuthState();

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
 * JWTを取得するヘルパー
 */
function getToken() {
    return localStorage.getItem("access_token");
}

/**
 * 認証状態に応じてUIを切り替える
 */
function setupAuthState() {
    const token = getToken();
    const userMenu = document.querySelector(".user-menu");
    const signinLink = document.querySelector(".signin");
    const userIcon = document.querySelector(".auth-area > .user-icon");

    if (token) {
        // ログイン状態
        if (signinLink) signinLink.style.display = "none";
        if (userIcon) userIcon.style.display = "none";
        if (userMenu) userMenu.style.display = "flex";

        // JWTからemailを取り出して表示する
        const payload = JSON.parse(atob(token.split(".")[1]));
        document.getElementById("username").textContent = payload.email;
    } else {
        // 未ログイン状態
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
