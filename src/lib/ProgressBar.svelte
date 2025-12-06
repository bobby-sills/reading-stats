<script lang="ts">
  const { title, author, percent, totalPages } = $props();
</script>

<div>
  <div id="book-information">
    <div style="display: flex; flex-direction: column; gap: 5px;">
      <span style="color: var(--fg); font-size: larger;">{title}</span>
      <span style="color: var(--fg4);">by {author}</span>
    </div>
    <span style="color: var(--fg); font-size: larger;"
      >{Math.ceil((percent / 100) * totalPages)}/{totalPages} pages</span
    >
  </div>
  <div id="progress-bar">
    <div style:width="{percent}%" id="progress-fill"></div>
  </div>
</div>

<style>
  #book-information {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }

  #progress-bar {
    height: 10px;
    width: 100%;
    margin: 10px 0px;
    background-color: var(--bg3);
    overflow: hidden;
    border-radius: 999px;
  }

  #progress-fill {
    height: 100%;
    background-color: var(--green);
    border-radius: 999px;
  }
</style>
