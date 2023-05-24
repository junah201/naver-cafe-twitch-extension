const url = `https://port-0-naver-cafe-twitch-extension-otjl2cli1ot5ff.sel4.cloudtype.app`;

window.Twitch.ext.onAuthorized(function (params) {
	const channelId = params.channelId;
	function saveConfig(channelId, title, keyword) {
		fetch(
			`${url}/config?channel_id=${channelId}&title=${title}&keyword=${keyword}`,
			{
				method: "POST",
			}
		).then((response) => console.log(response));

		console.log("Saved");
	}

	let boards = {};

	boardsFetchButton = document.getElementById("fetchButton");
	saveButton = document.getElementById("selectButton");
	console.log(boardsFetchButton);
	console.log(saveButton);

	boardsFetchButton.addEventListener("click", function () {
		const cafeNameInput = document.getElementById("cafeNameInput");

		if (cafeNameInput.value == "") {
			alert("카페 이름을 입력해주세요.");
			return;
		}

		fetch(`${url}/${cafeNameInput.value}/boards`, {
			method: "GET",
			headers: {
				accept: "application/json",
			},
		})
			.then((res) => {
				console.log(res);
				return res.json();
			})
			.then((data) => {
				boardsSelect = document.getElementById("boardSelect");
				boardsSelect.innerHTML = "";
				data.forEach((board) => {
					boards[board.cafe_menu_id] = board;
					boardsSelect.innerHTML += `<option value="${board.cafe_menu_id}">${board.board_name}</option>`;
				});
			});
	});

	saveButton.addEventListener("click", function () {
		const titleInput = document.getElementById("titleInput");
		const cafeNameInput = document.getElementById("cafeNameInput");
		const boardSelect = document.getElementById("boardSelect");
		const alertSpan = document.getElementById("alert");

		alertSpan.innerHTML = `저장 중...`;

		fetch(`${url}/${channelId}/config`, {
			method: "POST",
			headers: {
				accept: "application/json",
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				panel_title: titleInput.value,
				cafe_name: cafeNameInput.value,
				cafe_id: boards[boardSelect.value].cafe_id,
				cafe_menu_id: boardSelect.value,
				cafe_board_type: boards[boardSelect.value].cafe_board_type,
			}),
		})
			.then((res) => {
				if (res.status === 200) {
					alertSpan.innerHTML = `저장되었습니다.`;
					return;
				}
				alertSpan.innerHTML = `저장에 실패했습니다. 알 수 없는 오류`;
			})
			.catch((err) => {
				alert(`저장에 실패했습니다.\n\n${err}`);
			});
	});

	fetch(`${url}/${channelId}/config`, {
		method: "GET",
		headers: {
			accept: "application/json",
		},
	})
		.then((res) => {
			return res.json();
		})
		.then((configData) => {
			console.log(configData);
			titleInput = document.getElementById("titleInput");
			titleInput.value = configData?.panel_title;
			cafeNameInput = document.getElementById("cafeNameInput");
			cafeNameInput.value = configData?.cafe_name;

			if (configData?.cafe_name) {
				fetch(`${url}/${configData?.cafe_name}/boards`, {
					method: "GET",
					headers: {
						accept: "application/json",
					},
				})
					.then((res) => {
						console.log(res);
						return res.json();
					})
					.then((data) => {
						boardsSelect = document.getElementById("boardSelect");
						boardsSelect.innerHTML = "";
						data.forEach((board) => {
							boards[board.cafe_menu_id] = board;
							boardsSelect.innerHTML += `<option value="${board.cafe_menu_id}">${board.board_name}</option>`;
						});

						boardsSelect.value = configData?.cafe_menu_id;
					})
					.catch((err) => {
						console.log(err);
						alertSpan = document.getElementById("alert");
						alertSpan.innerHTML = `카페 아이디가 잘못되었습니다. ${err}`;
					});
			}
		});
});
