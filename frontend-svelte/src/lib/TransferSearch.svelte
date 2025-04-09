<script>
  let playerName = $state("");
  let playerDataJson = $state();
  let { players } = $props();
  let searchTransfer = $state("");
  let selectedPlayers = $state([]);
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
      player
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
    if (selectedPlayers.length < 15 && !selectedPlayers.includes(cPlayer)) {
      selectedPlayers = [...selectedPlayers, cPlayer];
    }
  }
</script>

<!-- <form method="post" onsubmit={search} id="searchbar"></form> -->
<form method="post" id="transferSearch">
  <input bind:value={searchTransfer} placeholder="Search Player" />
  <!-- <button type="submit">Search</button> -->
</form>

<div class="flex-container">
  {#if searchTransfer === ""}
    <p></p>
  {:else}
    <div class="suggestionView">
      {#each filteredPlayers as player}
        <div>
          <button onclick={() => chosenPlayer(player)} class="suggestion"
            >{player}</button
          >
        </div>
      {/each}
    </div>
  {/if}
  <div>
    <div style="justify-items: center;">{selectedPlayers.length}/15</div>
    <div class="selectedView">
      {#each selectedPlayers as player}
        <p>{player}</p>
      {/each}
    </div>
  </div>
</div>

<style>
  .suggestionView {
    overflow-y: auto;
    max-height: 20em;
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
