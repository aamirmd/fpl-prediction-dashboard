<script>
  /* let count = $state(0);
  const increment = () => {
    count += 1;
  }; */
  let playerName = $state("");
  let playerDataJson = $state();
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
      console.log(json.data);
      playerDataJson = json.data;
    } catch (error) {
      console.error(error.message);
    }
  }
</script>

<form method="post" onsubmit={search} id="searchbar">
  <input placeholder="Search Player" />
  <button type="submit">Search</button>
</form>
<p>Searched : {playerDataJson?.search}</p>
<p>Player ID : {playerDataJson?.id}</p>
<p>Goals scored : {playerDataJson?.goals}</p>
