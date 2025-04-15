<script>
  import svelteLogo from "./assets/svelte.svg";
  import viteLogo from "/vite.svg";
  import Counter from "./lib/Counter.svelte";
  import Search from "./lib/Search.svelte";

  import { onMount } from "svelte";
  import TransferSearch from "./lib/TransferSearch.svelte";

  let players = $state([]);

  onMount(async () => {
    const response = await fetch("http://127.0.0.1:5000/players");
    const json = await response.json();
    players = json.data;
  });
</script>

<main>
  <!-- <div>
    <a href="https://vite.dev" target="_blank" rel="noreferrer">
      <img src={viteLogo} class="logo" alt="Vite Logo" />
    </a>
    <a href="https://svelte.dev" target="_blank" rel="noreferrer">
      <img src={svelteLogo} class="logo svelte" alt="Svelte Logo" />
    </a>
  </div> -->
  <h1>FPL Transfer Recommender</h1>
  <!-- 
  <div class="card">
    <Counter />
  </div> -->

  <div>
    <div class="transfer">
      <!-- <p>Transfer Recommender</p> -->
      <TransferSearch {players} />
    </div>
    <!-- <div class="search">
      <p>Player Search</p>
      <Search {players} />
    </div> -->
  </div>
</main>

<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
  .flex-container {
    flex-direction: row;
    display: flex;
    justify-content: center;
  }
  .transfer {
    justify-items: center;
  }
  .search {
    justify-items: center;
  }
</style>
