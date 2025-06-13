<script lang="ts">
	import Material from '$lib/Material.svelte';
	import { onMount } from 'svelte';

	interface MaterialModel {
		id: number;
		title: string;
		content: string;
	}
	let materials: null | MaterialModel[] = null;
	let currentMaterial: null | MaterialModel = null;
	onMount(async () => {
		const response = await fetch('/api/material');
		materials = await response.json();
	});
</script>

<aside
	class="resize:horizontal border-r-double border-surface-50-950 fixed top-0 left-0 z-10 z-40 flex
	h-screen w-40 -translate-x-full translate-x-0 flex-col overflow-x-hidden overflow-y-scroll text-wrap lg:w-64"
>
	{#if materials !== null}
		{#each materials as material (material.id)}
			<button
				onclick={() => {
					currentMaterial = material;
				}}
				class:bg-primary-800-200={currentMaterial?.id == material.id}
				class:text-surface-50-950={currentMaterial?.id == material.id}
				class="btn btn-lg rounded-none"
			>
				<p style="overflow: hidden; text-overflow: ellipsis;">{material.title}</p>
			</button>
		{/each}
	{/if}
</aside>
<div class="ml-40 h-screen p-4 pb-0 lg:ml-64">
	{#if currentMaterial !== null}
		{#key currentMaterial.id}
			<Material title={currentMaterial.title} content={currentMaterial.content} />{/key}
	{/if}
</div>
{#if materials !== null}
	{#each materials as material (material.id)}
		<Material title={material.title} content={material.content} />
	{/each}
{/if}
