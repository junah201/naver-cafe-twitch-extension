const url = `https://navercafe-backend.herokuapp.com`;

function saveConfig(channelId, title, keyword) {
  fetch(
    `${url}/config?channel_id=${channelId}&title=${title}&keyword=${keyword}`,
    {
      method: "POST",
    }
  ).then((response) => console.log(response));

  console.log("Saved");
}

window.Twitch.ext.onAuthorized(function (params) {
  const channelId = params.channelId;
  console.log(channelId);

  saveButton = document.getElementById("save-button");
  saveLabel = document.getElementById("save-label");

  fetch(`${url}/title?channel_id=${channelId}`, {
    method: "GET",
  })
    .then((response) => {
      console.log(response);
      console.log(response.text);
      return response.json();
    })
    .then((data) => {
      console.log(data);
      titleInput = document.getElementById("title-input");
      titleInput.value = data.title;
    });

  fetch(`${url}/keyword?channel_id=${channelId}`, {
    method: "GET",
  })
    .then((response) => {
      console.log(response);
      console.log(response.text);
      return response.json();
    })
    .then((data) => {
      console.log(data);
      keywordInput = document.getElementById("keyword-input");
      keywordInput.value = data.keyword;
    });

  saveButton.addEventListener("click", function () {
    saveLabel.innerHTML = "";
    const title = document.getElementById("title-input").value;
    const keyword = document.getElementById("keyword-input").value;
    if (title == "" || keyword == "") {
      saveLabel.innerHTML = "모든 값을 입력해주세요.";
      return;
    }
    saveConfig(channelId, title, keyword);
    saveLabel.innerHTML = "저장되었습니다.";
  });
});
