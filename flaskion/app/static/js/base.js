/**
 * ページロード時処理
 */
document.addEventListener("DOMContentLoaded", function() {
    
    // ユーザーメニューセットアップ
    setupUserMenu();

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