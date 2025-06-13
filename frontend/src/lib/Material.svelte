<script lang="ts">
	import { marked } from 'marked';
	let { title, content }: { title: string; content: string } = $props();
</script>

<h1 class="h1">{title}</h1>
<div>{@html marked(content)}</div>
