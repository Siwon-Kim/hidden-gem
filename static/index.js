
$(document).ready(function () {
	listing();
});

function listing() {
	let liked_store;
	fetch("/store")
		.then((res) => res.json())
		.then((data) => {
			let stores = data["stores"];
			try { liked_store = data["liked_store"] }
			catch { liked_store = [] }
			$("#cards").empty();
			stores.forEach((e) => {
				let name = e["store_name"];
				let address = e["address"];
				let category = e["category"];
				let image = e["image"];
				let star = e["star"];
				let comment = e["store_comment"];
				let like = e["like"];
				let id = e["_id"];

				let star_repeat = "⭐".repeat(star);
				let temp_html = `<div class="col">
                                    <div class="card h-100">
                                        <img
                                            src="${image}"
                                            class="card-img-top"
                                        />
										<div style="text-align: right;">
											<button
												type="button"
												class="btn btn-dark delete"
												value=${id}
												style="margin: 15px 15px 0 15px;"
											>
												삭제
											</button>
										</div>
                                        <div class="card-body content" style="padding-top: 0px;">
                                            <h4 class="card-title">${name}</h4>
                                            <p class="card-text">
                                                ${address}
                                            </p>
                                            <p class="card-text">
                                                ${category}
                                            </p>
                                            <p>${star_repeat}</p>
                                            <p class="mycomment">
                                                ${comment}
                                            </p>
											<p class="nick">
                                            	작성자 ${comment}
                                            </p>
                                        </div>
										<div class="store-btn">
											<button type="button" class="button is-info">저장</button>
												<button type="button" class="button is-warning is-light like" value=${id}>&#128077 ${like}</button>

												<button type="button" class="button is-warning unlike" value=${id}>&#128077 ${like}</button>
										</div>
									</div>
                                </div>`;

				$("#cards").append(temp_html);
			});
			
			$(".like").click(function () {
				let storeid = this.value
				// Like 버튼 클릭시 1 증가
				console.log(storeid, liked_store);
				if (!liked_store.includes(storeid)) {
					// Frontend: Increasing Like count on the page
					$(this).html(function (i, val) {
						return `&#128077 ${val.split(" ")[1] * 1 + 1}`;
					});
					liked_store.append(stordid)

					// Backend: Sending Like count on th page to the DB
					let formData = new FormData();
					formData.append("id_give", this.value);
					fetch("/likeUp", { method: "POST", body: formData })
						.then((response) => response.json())
						.then((data) => {
						});
				}
				// Like 버튼 클릭시 1 감소 
				else if (liked_store.includes(storeid)) {
					$(this).html(function (i, val) {
						return `&#128077 ${val.split(" ")[1] * 1 - 1}`;
					});

					let formData = new FormData();
					formData.append("id_give", this.value);
					fetch("/likeDown", { method: "POST", body: formData })
						.then((response) => response.json())
						.then((data) => {
						});
				}
			});

			$(".delete").click(function () {
				let formData = new FormData();
				formData.append("id_give", this.value);
				console.log(this.value);
				fetch("/store", { method: "DELETE", body: formData })
					.then((response) => response.json())
					.then((data) => {
						window.location.reload();
					});
			});
		});
}

function posting() {
	let url = $("#url").val();
	let comment = $("#comment").val();
	let star = $("#star").val();
	let nickname = $("#nickname").val();

	let formData = new FormData();
	formData.append("url_give", url);
	formData.append("comment_give", comment);
	formData.append("star_give", star);

	fetch("/store", { method: "POST", body: formData })
		.then((res) => res.json())
		.then((data) => {
			window.location.reload();
		});
}

function open_box() {
	$("#post-box").show();
}
function close_box() {
	$("#post-box").hide();
}

// 로그아웃은 내가 가지고 있는 토큰만 쿠키에서 없애면 됩니다.
function logout() {
	$.removeCookie("mytoken");
	alert("로그아웃!");
	window.location.href = "/login";
}

