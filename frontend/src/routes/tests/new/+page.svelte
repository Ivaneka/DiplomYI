<script lang="ts">
	import TestForm from '$lib/TestForm.svelte';
	import { onMount } from 'svelte';

	let test: TestModel = $state({ title: '', description: '', material_ids: [], questions: [] });
	let materials: null | MaterialModel[] = null;
	onMount(async () => {
		const response = await fetch('/api/material');
		materials = await response.json();
	});

	async function createTest() {
		fetch('/api/test', {
			method: 'PUT',
			body: JSON.stringify(test),
			headers: { 'Content-Type': 'application/json' }
		});
	}
</script>

<TestForm {test} />
<button onclick={createTest}>Создать тест</button>
