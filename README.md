<h1>Video website for https://github.com/lukeschwab17/LukeBot</h1>
Website hosts video compilations created via LukeBot discord bot
<br></br>
<h2>Notes:</h2>
<ol>
  <li><h4>This project is tied to my discord bot github project (linked above)</li>
  <li><h4>Uses OAuth 2.0 for login, as the videos a user may view are tied to what guilds they are in.</li>
  <li><h4>Uses a local database containing servers (called 'guilds') that the bot is in and the users of those servers. Reasoning:</li>
  <ul>
    <li>I could have used discord api and requested the user to hand over the list of all the servers they are in on login, but the guilds that the bot is not in are not relevant to the website.</li>
    <li>Not everyone would want someone to have access to see every server that they are a member of.</li>
  </ul>
</ol>
