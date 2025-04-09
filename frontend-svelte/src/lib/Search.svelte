<script>
  let playerName = $state("");
  let playerDataJson = $state();
  let { players } = $props();
  let searchTerm = $state("");

  const search = (e) => {
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

  let filteredPlayers = $derived(
    players.filter((player) =>
      player
        .normalize("NFD")
        .replace(/\p{Diacritic}/gu, "")
        .toLowerCase()
        .includes(
          searchTerm
            .normalize("NFD")
            .replace(/\p{Diacritic}/gu, "")
            .toLocaleLowerCase()
        )
    )
  );

  function chosenPlayer(cPlayer) {
    searchTerm = cPlayer;
    playerName = searchTerm;
    playerData();
  }
</script>

<form method="post" onsubmit={search} id="searchbar">
  <input bind:value={searchTerm} placeholder="Search Player" />
  <button type="submit">Search</button>
</form>
{#if searchTerm === ""}
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
<p>Searched : {playerDataJson?.search}</p>
<p>Player ID : {playerDataJson?.id}</p>
<p>Predicted Points : {playerDataJson?.points}</p>

<style>
  .suggestionView {
    overflow-y: auto;
    max-height: 20em;
  }
</style>
