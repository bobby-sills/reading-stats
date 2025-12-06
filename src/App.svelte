<script lang="ts">
  import ProgressBar from "./lib/ProgressBar.svelte";
  import koreaderData from "../data/koreader-data.json";

  interface Book {
    id: number;
    title: string;
    authors: string;
    percentage_completed: number;
  }

  const books: Book[] = koreaderData.books;
</script>

<svelte:head>
  <title>reading stats</title>
</svelte:head>

<main>
  <h1>reading stats</h1>

  <h2>currently reading</h2>
  {#each books as book (book.id)}
    <ProgressBar
      title={book.title}
      author={book.authors}
      percent={book.percentage_completed.toString()}
      totalPages="1000"
    />
  {/each}
  <h2>completed</h2>
  <h2>want to read</h2>
</main>

<style>
</style>
