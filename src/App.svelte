<script lang="ts">
  import ProgressBar from "./lib/ProgressBar.svelte";
  import koreaderData from "../data/koreader-data.json";
  import manualData from "../data/manual-data.json";

  interface Book {
    title: string;
    authors: string;
    percentage_completed: number;
    total_pages?: number;
    date_completed?: string;
  }

  // Combine koreader books with manual books (prefer KOReader data)
  const koreaderBooks = koreaderData.books.map(book => ({
    ...book,
    total_pages: manualData.page_counts[book.title as keyof typeof manualData.page_counts]
  }));

  // Get titles from KOReader to avoid duplicates
  const koreaderTitles = new Set(koreaderBooks.map(b => b.title));

  // Add manual currently_reading books that aren't in KOReader data
  const manualCurrentlyReading = manualData.currently_reading
    .filter(book => !koreaderTitles.has(book.title))
    .map(book => ({
      title: book.title,
      authors: book.authors,
      percentage_completed: (book.pages_read / book.total_pages) * 100,
      total_pages: book.total_pages
    }));

  // Add completed books from manual data
  const manualCompleted = manualData.completed
    .filter(book => !koreaderTitles.has(book.title))
    .map(book => ({
      title: book.title,
      authors: book.authors,
      percentage_completed: 100,
      date_completed: book.date_completed
    }));

  const books: Book[] = [
    ...koreaderBooks,
    ...manualCurrentlyReading,
    ...manualCompleted
  ];
</script>

<svelte:head>
  <title>reading stats</title>
</svelte:head>

<main>
  <h1>reading stats</h1>

  <h2>currently reading</h2>
  {#each books as book (book.title)}
    <ProgressBar
      title={book.title}
      author={book.authors}
      percent={book.percentage_completed.toString()}
      totalPages={book.total_pages?.toString() ?? "0"}
    />
  {/each}
  <h2>completed</h2>
  <h2>want to read</h2>
</main>

<style>
</style>
