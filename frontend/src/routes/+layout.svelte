<script lang="ts">
	import Nav from '$lib/Nav.svelte';
	import '../app.css';
	let { children } = $props();
</script>

<Nav />
<div class="relatve">
	{@render children()}
</div>

<style>
	:global(html),
	:global(body) {
		@apply h-full;
	}
</style>
