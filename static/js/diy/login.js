
// 隐藏登录模态框
$(document).on("click", ".cancel-login-href", function () {
    $('#loginModal').modal('hide');
});

// 弹出登录模态框
$(document).on("click", ".show-login-href", function () {
    $('#loginModal').modal('show');
});