<script>
  let playerName = $state("");

  let playerDataJson = $state();
  let { players } = $props();
  let searchTransfer = $state("");
  let selectedPlayers = $state([]);
  let goalkeepers = $state([]);
  let forwards = $state([]);
  let defenders = $state([]);
  let midfielders = $state([]);
  let bankMoney = $state();
  let recommendation = $state([]);

  let startgoalkeepers = $state([]);
  let startforwards = $state([]);
  let startdefenders = $state([]);
  let startmidfielders = $state([]);

  let afterTransfer = $state([]);
  /*   const search = (e) => {
    e.preventDefault();
    playerName = document.forms["searchbar"].elements[0].value;
    playerData();
  };
  async function playerData() {
    const url = `http://127.0.0.1:5000/search/${encodeURIComponent(playerName.toLowerCase())}`;

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error("Error with getting player data");
      }
      const json = await response.json();
      playerDataJson = json.data;
    } catch (error) {
      console.error(error.message);
    }
  }
 */
  let filteredPlayers = $derived(
    players.filter((player) =>
      player["name"]
        .normalize("NFD")
        .replace(/\p{Diacritic}/gu, "")
        .toLowerCase()
        .includes(
          searchTransfer
            .normalize("NFD")
            .replace(/\p{Diacritic}/gu, "")
            .toLocaleLowerCase()
        )
    )
  );

  function chosenPlayer(cPlayer) {
    if (
      cPlayer["position"] === "Forward" &&
      !forwards.includes(cPlayer) &&
      forwards.length < 3
    ) {
      forwards = [...forwards, cPlayer];
    } else if (
      cPlayer["position"] === "Goalkeeper" &&
      !goalkeepers.includes(cPlayer) &&
      goalkeepers.length < 2
    ) {
      goalkeepers = [...goalkeepers, cPlayer];
    } else if (
      cPlayer["position"] === "Midfielder" &&
      !midfielders.includes(cPlayer) &&
      midfielders.length < 5
    ) {
      midfielders = [...midfielders, cPlayer];
    } else if (
      cPlayer["position"] === "Defender" &&
      !defenders.includes(cPlayer) &&
      defenders.length < 5
    ) {
      defenders = [...defenders, cPlayer];
    }
  }

  async function getTransferRec() {
    const url = "http://127.0.0.1:5000/transfer";
    selectedPlayers = [
      ...forwards,
      ...defenders,
      ...goalkeepers,
      ...midfielders,
    ];
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          bank: bankMoney,
          selectedPlayers: selectedPlayers,
        }),
      });
      if (!response.ok) {
        throw new Error("Error with getting player data");
      }
      const json = await response.json();
      recommendation = json.data;
      console.log(recommendation);
    } catch (error) {
      console.error(error.message);
    }
  }

  function reset() {
    selectedPlayers = [];
    goalkeepers = [];
    forwards = [];
    midfielders = [];
    defenders = [];
  }

  function removePlayer(player) {
    if (player["position"] === "Forward") {
      forwards = forwards.filter((p) => p["name"] !== player["name"]);
    } else if (player["position"] === "Midfielder") {
      midfielders = midfielders.filter((p) => p["name"] !== player["name"]);
    } else if (player["position"] === "Defender") {
      defenders = defenders.filter((p) => p["name"] !== player["name"]);
    } else if (player["position"] === "Goalkeeper") {
      goalkeepers = goalkeepers.filter((p) => p["name"] !== player["name"]);
    }
  }

  function applyTransfer(rec) {
    afterTransfer = selectedPlayers.map((player) => {
      if (rec["playerOut"]["id"] === player["id"]) {
        return rec["playerIn"];
      }
      return player;
    });

    afterTransfer = afterTransfer.sort(
      (x, y) =>
        parseFloat(y["predictedPoints"]) - parseFloat(x["predictedPoints"])
    );

    let total = 0;
    startgoalkeepers = [];
    startdefenders = [];
    startmidfielders = [];
    startforwards = [];
    for (let player of afterTransfer) {
      if (
        player["position"] === "Goalkeeper" &&
        startgoalkeepers.length < 1 &&
        total < 11
      ) {
        startgoalkeepers = [...startgoalkeepers, player];
        total++;
      } else if (
        player["position"] === "Defender" &&
        startdefenders.length < 5 &&
        total < 11
      ) {
        startdefenders = [...startdefenders, player];
        total++;
      } else if (
        player["position"] === "Midfielder" &&
        startmidfielders.length < 5 &&
        total < 11
      ) {
        startmidfielders = [...startmidfielders, player];
        total++;
      } else if (
        player["position"] === "Forward" &&
        startforwards.length < 3 &&
        total < 11
      ) {
        startforwards = [...startforwards, player];
        total++;
      }
    }
  }
</script>

<!-- <form method="post" onsubmit={search} id="searchbar"></form> -->

<!-- <input bind:value={bankMoney} placeholder="Money left in bank" /> -->

<!-- replace separate lists with just position checks in for each loop -->
<div class="transferLayout">
  <div class="selectedPlayers">
    <div>
      <button onclick={() => reset()}>Reset Squad</button>
    </div>
    <div>
      <p>Goalkeepers: {goalkeepers.length}/2</p>
      <div class="playerRow">
        {#each goalkeepers as gk}
          <div class="player">
            {gk["name"]}
            <button class="x" onclick={() => removePlayer(gk)}>x</button>
          </div>
        {/each}
      </div>

      <p>Defenders: {defenders.length}/5</p>
      <div class="playerRow">
        {#each defenders as def}
          <div class="player">
            {def["name"]}
            <button class="x" onclick={() => removePlayer(def)}>x</button>
          </div>
        {/each}
      </div>

      <p>Midfielders: {midfielders.length}/5</p>
      <div class="playerRow">
        {#each midfielders as mid}
          <div class="player">
            {mid["name"]}
            <button class="x" onclick={() => removePlayer(mid)}>x</button>
          </div>
        {/each}
      </div>

      <p>Forwards: {forwards.length}/3</p>
      <div class="playerRow">
        {#each forwards as fwd}
          <div class="player">
            {fwd["name"]}
            <button class="x" onclick={() => removePlayer(fwd)}>x</button>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <div class="searchLayout">
    <div class="searchContainer">
      <form method="post" class="transferSearch">
        <input bind:value={searchTransfer} placeholder="Search Player" />
      </form>

      {#if searchTransfer !== ""}
        <div class="suggestionView">
          {#each filteredPlayers as player}
            <div>
              <button onclick={() => chosenPlayer(player)} class="suggestion"
                >{player["name"]}</button
              >
            </div>
          {/each}
        </div>
      {/if}
    </div>

    <div class="startingSection">
      <div>Recommended Starting 11 after applied transfer</div>
      <div>
        <p>Goalkeepers</p>
        <div class="playerRow">
          {#each startgoalkeepers as gk}
            <div class="player">
              {gk["name"]}
            </div>
          {/each}
        </div>

        <p>Defenders</p>
        <div class="playerRow">
          {#each startdefenders as def}
            <div class="player">
              {def["name"]}
            </div>
          {/each}
        </div>

        <p>Midfielders</p>
        <div class="playerRow">
          {#each startmidfielders as mid}
            <div class="player">
              {mid["name"]}
            </div>
          {/each}
        </div>

        <p>Forwards:</p>
        <div class="playerRow">
          {#each startforwards as fwd}
            <div class="player">
              {fwd["name"]}
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
  <div class="bankRecs">
    <div class="bankRow">
      <input
        class="bank"
        bind:value={bankMoney}
        placeholder="Money left in bank"
      />
    </div>
    <div>
      <button onclick={() => getTransferRec()}>Get transfer rec</button>

      {#if Object.keys(recommendation).length > 0}
        <p>Our Top 3 Recommendations</p>
        <div class="recContainer">
          <div class="recHeader">
            <p class="out">OUT</p>
            <p class="in">IN</p>
          </div>
          {#each recommendation as rec}
            <div class="recRow">
              <div class="playerOut">{rec["playerOut"]["name"]}</div>
              <div class="playerIn">{rec["playerIn"]["name"]}</div>
              <button class="applyButton" onclick={() => applyTransfer(rec)}
                >Apply</button
              >
            </div>
          {/each}
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  * {
    box-sizing: border-box;
  }
  .suggestionView {
    overflow-y: auto;
    max-height: 20em;
    z-index: 10;
    max-width: 400px;
    position: absolute;
    background-color: white;
    border: 1px solid #ddd;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  .suggestion {
    font-size: 13px;
    width: 300px;
    border-radius: 0;
    border-top-color: whitesmoke;
  }

  .searchContainer {
    position: relative;
  }
  .flex-container {
    flex-direction: row;
    display: flex;
  }
  .selectedView {
    overflow-y: auto;
    max-height: 20em;
  }
  .transferLayout {
    flex-direction: row;
    display: flex;
    justify-content: space-evenly;
    gap: 100px;
    max-width: 100%;
  }
  .transferSearch input {
    border-radius: 5px;
    height: 30px;
    width: 300px;
    outline: none;
    /* transition: border-color 0.2s; */
    text-align: center;
  }
  .playerRow {
    display: flex;
    flex-wrap: wrap;
    max-width: 400px;
    max-height: 150px;
    justify-content: center;
    gap: 5px;
  }
  .player {
    flex-direction: row;
    display: flex;
    padding: 5px;
    font-size: 13px;
    justify-content: center;
    align-items: center;
    background-color: darkgray;
    border-radius: 5px;
  }
  .bank {
    border-radius: 5px;
    height: 30px;
    width: 150px;
    outline: none;
    /* transition: border-color 0.2s; */
    text-align: center;
  }
  .bankRow {
    flex-direction: row;
    display: flex;
    align-content: center;
    padding-bottom: 20px;
  }
  .x {
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    height: 24px;
    width: 24px;
    background-color: rgb(193, 80, 80);
    font-size: 9px;
  }
  .selectedPlayers {
    max-width: 400px;
    width: 400px;
  }
  .searchLayout {
    width: 300px;
    max-width: 300px;
    flex-shrink: 0;
  }
  .bankRecs {
    display: flex;
    flex-direction: column;
    width: 400px;
    max-width: 400px;
    justify-self: center;
    align-items: center;
  }
  .recHeader {
    display: flex;
    flex-direction: row;
  }
  .out {
    justify-content: center;
    text-align: center;
    background-color: red;
    width: 200px;
  }
  .in {
    justify-content: center;
    text-align: center;
    background-color: green;
    width: 200px;
  }
  .recRow {
    flex-direction: row;
    display: flex;
    width: 100%;
  }
  .recRow {
    display: flex;
    align-items: center;
    width: 100%;
    padding: 5px;
  }
  .playerOut,
  .playerIn {
    width: 40%;
    text-align: center;
  }
  .recContainer {
    width: 100%;
    border: 1px solid #ddd;
    border-radius: 5px;
    overflow: hidden;
    margin-top: 10px;
  }
  .applyButton {
    width: 20%;
    padding: 3px;
    margin-left: auto;
  }
</style>
