const url = `https://port-0-naver-cafe-twitch-extension-otjl2cli1ot5ff.sel4.cloudtype.app`;

window.Twitch.ext.onAuthorized(function (params) {
	const channelId = params.channelId;
	console.log(channelId);

	function reloadItem() {
		fetch(`${url}/${channelId}/posts`, {
			method: "GET",
		})
			.then((res) => {
				return res.json();
			})
			.then((data) => {
				for (const idx in data) {
					const item = document.getElementById(idx);
					if (item == null) {
						const table = document.getElementById("table");
						console.log(table);
						if (idx == 0) {
							table.innerHTML += `<div class = "item" id = ${idx}><a href = ${data[idx].link} target="_blank">${data[idx].title}</a></div>`;
						} else {
							table.innerHTML += `<br/><div class = "item" id = ${idx}><a href = ${data[idx].link} target="_blank">${data[idx].title}</a></div>`;
						}
					} else {
						item.innerHTML = `<a href = ${data[idx].link} target="_blank">${data[idx].title}</a>`;
					}
					console.log(data[idx]);
				}
			});
	}

	function reloadTitle() {
		fetch(`${url}/${channelId}/config`, {
			method: "GET",
		})
			.then((response) => {
				return response.json();
			})
			.then((data) => {
				titleH1 = document.getElementById("title");
				titleH1.innerHTML = data.panel_title;
				titleA = document.querySelector("#title > a");
				titleA.href = `https://cafe.naver.com/${data.cafe_name}`;
			});
	}

	reloadTitle();
	reloadItem();

	refreshButton = document.getElementById("refresh");
	refreshButton.addEventListener("mousedown", function () {
		reloadItem();
		refreshButton.className = "display";
	});
	refreshButton.addEventListener("mouseup", function () {
		refreshButton.className = "undisplay";
	});
});
