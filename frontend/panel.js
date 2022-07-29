const url = `https://navercafe-backend.herokuapp.com`;

window.Twitch.ext.onAuthorized(function (params) {
  const channelId = params.channelId;
  console.log(channelId);

  function reloadItem() {
    fetch(`${url}/naver?channel_id=${channelId}`, {
      method: "GET",
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        for (var idx of data.items.keys()) {
          const item = document.getElementById(idx);
          if (item == null) {
            const table = document.getElementById("table");
            if (idx == 0) {
              table.innerHTML += `<div class = "item" id = ${idx}><a href = ${data.items[idx].link} target="_blank">${data.items[idx].title}</a></div>`;
            } else {
              table.innerHTML += `</br><div class = "item" id = ${idx}><a href = ${data.items[idx].link} target="_blank">${data.items[idx].title}</a></div>`;
            }
          } else {
            item.innerHTML = `<a href = ${data.items[idx].link} target="_blank">${data.items[idx].title}</a>`;
          }
          console.log(data.items[idx]);
        }
        var t = document.getElementById(0);
      });
    console.log("reloading");
  }

  function reloadTitle() {
    fetch(`${url}/title?channel_id=${channelId}`, {
      method: "GET",
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        titleH1 = document.getElementById("title");
        titleH1.innerHTML = data.title;
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
