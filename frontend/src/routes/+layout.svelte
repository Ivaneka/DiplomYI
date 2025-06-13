<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

{@render children()}

<style>
	:global(html),
	:global(body) {
		@apply h-full;
	}
</style>
