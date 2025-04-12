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
    if (selectedPlayers.length < 15 && !selectedPlayers.includes(cPlayer)) {
      selectedPlayers = [...selectedPlayers, cPlayer];
    }
  }

  async function getTransferRec() {
    const url = "http://127.0.0.1:5000/transfer";

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(selectedPlayers),
      });
      if (!response.ok) {
        throw new Error("Error with getting player data");
      }
      const json = await response.json();
      recommendation = json.data;
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
<form method="post" id="transferSearch">
  <input bind:value={searchTransfer} placeholder="Search Player" />
  <!-- <button type="submit">Search</button> -->
</form>

<div class="flex-container">
  <div>
    <p>Goalkeepers</p>
    {#each goalkeepers as gk}
      <div>{gk["name"]}</div>
    {/each}
    <p>Fowards:</p>
    {#each forwards as fwd}
      <div>{fwd["name"]}</div>
    {/each}
    <p>Midfielders:</p>
    {#each midfielders as mid}
      <div>{mid["name"]}</div>
    {/each}
    <p>Defenders:</p>
    {#each defenders as def}
      <div>{def["name"]}</div>
    {/each}
  </div>
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
    <p>testing</p>
  {/if}
  <div>
    <button onclick={() => reset()}>Reset</button>
    <div style="justify-items: center;">{selectedPlayers.length}/15</div>
    <div class="selectedView">
      {#each selectedPlayers as player}
        <p>{player["name"]}</p>
      {/each}
    </div>
  </div>
</div>
<div>
  <button onclick={() => getTransferRec()}>Get transfer rec</button>
  <p>Recommendation</p>
  <p>{recommendation}</p>
</div>

<style>
  .suggestionView {
    overflow-y: auto;
    max-height: 20em;
    z-index: 10;
  }
  .flex-container {
    flex-direction: row;
    display: flex;
  }
  .selectedView {
    overflow-y: auto;
    max-height: 20em;
  }
</style>
