
// 간단한 회원가입 함수입니다.
// 아이디, 비밀번호, 닉네임을 받아 DB에 저장합니다.
function register() {
    $.ajax({
        type: "POST",
        url: "/api/register/save",
        data: {
            id_give: $("#userid").val(),
            pw_give: $("#userpw").val(),
            nickname_give: $("#usernick").val(),
        },
        success: function (response) {
            if (response["result"] == "success") {
                alert("회원가입이 완료되었습니다.");
                window.location.href = "/login";
            } else {
                alert(response["msg"]);
            }
        },
    });
}

// 아이디, 닉네임 중복 여부를 체크하기 위한 함수입니다
function check_duplicates() {
    $.ajax({
        type: "POST",
        url: "api/register/duplicate_check",
        data: {
            id_give: $("#userid").val(),
            nickname_give: $("#usernick").val(),
        },
        success: function (response) {
            if (response["exists"]) {
                alert("이미 존재하는 아이디/닉네임입니다.");
            } else {
                window.location.href = "/login";
            }
        },
    });
}