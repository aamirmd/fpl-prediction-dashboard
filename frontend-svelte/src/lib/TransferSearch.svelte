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
  let recommendation = $state({});
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
</script>

<!-- <form method="post" onsubmit={search} id="searchbar"></form> -->

<!-- <input bind:value={bankMoney} placeholder="Money left in bank" /> -->

<!-- replace separate lists with just position checks in for each loop -->
<div class="transferLayout">
  <div>
    <div>
      <button onclick={() => reset()}>Reset Squad</button>
    </div>
    <div>
      <p>Goalkeepers: {goalkeepers.length}/2</p>
      <div class="playerRow">
        {#each goalkeepers as gk}
          <div class="player">{gk["name"]}</div>
        {/each}
      </div>

      <p>Defenders: {defenders.length}/5</p>
      <div class="playerRow">
        {#each defenders as def}
          <div class="player">{def["name"]}</div>
        {/each}
      </div>

      <p>Midfielders: {midfielders.length}/5</p>
      <div class="playerRow">
        {#each midfielders as mid}
          <div class="player">{mid["name"]}</div>
        {/each}
      </div>

      <p>Fowards: {forwards.length}/3</p>
      <div class="playerRow">
        {#each forwards as fwd}
          <div class="player">{fwd["name"]}</div>
        {/each}
      </div>
    </div>
  </div>

  <div class="searchLayout">
    <div>
      <form method="post" class="transferSearch">
        <input bind:value={searchTransfer} placeholder="Search Player" />
        <!-- <button type="submit">Search</button> -->
      </form>
    </div>

    <div>
      {#if searchTransfer === ""}
        <p></p>
      {:else}
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
  </div>

  <div class="bankRow">
    <input
      class="bank"
      bind:value={bankMoney}
      placeholder="Money left in bank"
    />
  </div>
</div>

<!-- <div>
  <button onclick={() => getTransferRec()}>Get transfer rec</button>
  <p>Recommendation</p>
  <p>{recommendation}</p>
</div> -->

<style>
  .suggestionView {
    overflow-y: auto;
    max-height: 20em;
    z-index: 10;
    max-width: 300px;
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
    gap: 20px;
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
    max-width: 500px;
    justify-content: center;
  }
  .player {
    padding: 5px;
    font-size: 15px;
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
  }
</style>
