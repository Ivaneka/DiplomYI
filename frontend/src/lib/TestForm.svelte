<script lang="ts">
	import type { QuestionModel, AnswerModel, TestModel } from '$lib/types';
	import QuestionForm from './QuestionForm.svelte';
	let { test }: { test: TestModel } = $props();
</script>

<div class="flex flex-col w-full">
	<input type="text" bind:value={test.title} placeholder="Название теста" />
	<textarea bind:value={test.description} class="resize-none" placeholder="Описание теста"
	></textarea>

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
