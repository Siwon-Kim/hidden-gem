$(document).ready(function () {
	listing();
});

function listing() {
	let liked_store, userid;
	fetch("/store")
		.then((res) => res.json())
		.then((data) => {
			let stores = data["stores"];
			try {
				liked_store = data["liked_store"];
				userid = data["userid"];
				console.log(userid);
				console.log(liked_store);
			} catch {
				liked_store = [];
			}
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
				let temp_html, temp_html_1, temp_html_2;
				temp_html_1 = `<div class="col">
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
									</div>
								`;

				// 페이지가 리프레쉬돼도 버튼 눌림 style이 반영되는 코드
				// 유저가 로그인하지 않았을 때
				if (userid === null) {
					temp_html_2 = `<div class="store-btn">
										<button type="button" class="like button is-warning" title="Disabled button" disabled value=${id}>&#128077 ${like}</button>
								   </div>
								</div>
							</div>`;
				}
				// 유저가 이미 like를 눌렀을 때
				else if (liked_store.includes(id)) {
					temp_html_2 = `<div class="store-btn">
										<button type="button" class="button is-info">저장</button>
										<button type="button" class="like button is-warning" value=${id}>&#128077 ${like}</button>
								   </div>
								</div>
							</div>`;
				}
				// 유저가 like를 누르지 않았을 때
				else {
					temp_html_2 = `<div class="store-btn">
										<button type="button" class="button is-info">저장</button>
										<button type="button" class="like button is-warning is-light" value=${id}>&#128077 ${like}</button>
								   </div>
								</div>
							</div>`;
				}
				temp_html = temp_html_1.concat(temp_html_2);
				$("#cards").append(temp_html);
			});

			$(".like").click(function () {
				let storeid = this.value;
				// Like 버튼 클릭시 1 증가
				if (!liked_store.includes(storeid)) {
					// 페이지 상에서 숫자를 올려줍니다 (리프레시 안해도 숫자 올라감)
					$(this).removeClass("is-light");
					$(this).html(function (i, val) {
						return `&#128077 ${val.split(" ")[1] * 1 + 1}`;
					});

					// liked_store array에 store id를 추가해줍니다 (페이지상)
					liked_store.push(storeid);

					// 올라간 like를 db에 반영합니다
					let formData = new FormData();
					formData.append("id_give", this.value);
					fetch("/likeUp", { method: "POST", body: formData })
						.then((response) => response.json())
						.then((data) => {});
				}
				// Like 버튼 클릭시 1 감소
				else if (liked_store.includes(storeid)) {
					$(this).addClass("is-light");
					$(this).html(function (i, val) {
						return `&#128077 ${val.split(" ")[1] * 1 - 1}`;
					});

					// liked_store array에서 store id를 삭제해줍니다 (페이지상)
					liked_store = liked_store.filter((s) => {
						return s !== storeid;
					});

					let formData = new FormData();
					formData.append("id_give", this.value);
					fetch("/likeDown", { method: "POST", body: formData })
						.then((response) => response.json())
						.then((data) => {});
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
