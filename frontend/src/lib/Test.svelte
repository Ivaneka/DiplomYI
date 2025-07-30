<script lang="ts">
	import type { TestModelWithID } from '$lib/types';
	import { onMount } from 'svelte';
	import Question from './Question.svelte';
	let { test }: { test: TestModelWithID } = $props();
	let selectedAnswers: number[] = $state([]);
	async function submit() {
		const body = {
			selectedAnswers: selectedAnswers,
			test_id: test.id
		};
		const response = await fetch('/api/attempt', {
			method: 'PUT',
			body: JSON.stringify(body),
			headers: { 'Content-Type': 'application/json' }
		});
	}
	onMount(() => {
		console.log(test);
	});
</script>

<div>
	<h1 class="h1">{test.title}</h1>
	<div>{test.description}</div>
	{#each test.questions as question (crypto.randomUUID())}
		<Question {question} {selectedAnswers} />
	{/each}
	<button onclick={submit}>Отправить ответы</button>
</div>
