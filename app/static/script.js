function updateBar() {
  const totalVotes = messiVotes + ronaldoVotes;
  const messiPercentageSpan = document.querySelector(
    ".messi-bar .percentage-text"
  );
  const ronaldoPercentageSpan = document.querySelector(
    ".ronaldo-bar .percentage-text"
  );

  if (totalVotes === 0) {
    document.querySelector(".messi-bar").style.width = "50%";
    document.querySelector(".ronaldo-bar").style.width = "50%";
    messiPercentageSpan.textContent = "";
    ronaldoPercentageSpan.textContent = "";
    messiPercentageSpan.style.opacity = "0";
    ronaldoPercentageSpan.style.opacity = "0";
  } else {
    const messiPercentage = (messiVotes / totalVotes) * 100;
    const ronaldoPercentage = (ronaldoVotes / totalVotes) * 100;

    document.querySelector(".messi-bar").style.width = messiPercentage + "%";
    document.querySelector(".ronaldo-bar").style.width =
      ronaldoPercentage + "%";

    messiPercentageSpan.textContent = messiPercentage.toFixed(0) + "%";
    ronaldoPercentageSpan.textContent = ronaldoPercentage.toFixed(0) + "%";
    messiPercentageSpan.style.opacity = "1";
    ronaldoPercentageSpan.style.opacity = "1";
  }

  document.querySelector(".messi-votes").textContent = `Messi: ${messiVotes}`;
  document.querySelector(
    ".ronaldo-votes"
  ).textContent = `Ronaldo: ${ronaldoVotes}`;
  document.querySelector(".total-votes").textContent = `Total: ${totalVotes}`;
}

function vote(player) {
  fetch("/vote", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ vote: player }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        messiVotes = data.messi_votes;
        ronaldoVotes = data.ronaldo_votes;
        updateBar();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function showPlayerLabel(player) {
  document.getElementById(player + "-label").style.opacity = "1";
}

function hidePlayerLabel(player) {
  document.getElementById(player + "-label").style.opacity = "0";
}

document.addEventListener("DOMContentLoaded", () => {
  updateBar();
});
