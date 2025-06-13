<script lang="ts">
	import type { QuestionModel, AnswerModel, TestModel } from '$lib/types';
	import QuestionForm from './QuestionForm.svelte';
	let { test }: { test: TestModel } = $props();
</script>

<div>
	<input type="text" bind:value={test.title} placeholder="Название теста" />
	<input type="text" bind:value={test.description} placeholder="Описание теста" />
	<div>
		{#each test.questions as question (crypto.randomUUID())}
			<QuestionForm {question} />
		{/each}
		<button
			onclick={() => {
				test.questions.push({ text: '', options: [] });
			}}>Новый вопрос</button
		>
	</div>
</div>
