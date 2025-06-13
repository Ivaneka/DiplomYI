<script lang="ts">
	import type { QuestionModel, AnswerModel } from '$lib/types';
	import AnswerForm from './AnswerForm.svelte';
	let { question }: { question: QuestionModel } = $props();
</script>

<div>
	<input type="text" bind:value={question.text} placeholder="Текст вопроса" />
	<div>
		{#each question.options as answer (crypto.randomUUID())}
			<AnswerForm {answer} />
		{/each}
		<button
			onclick={() => {
				question.options.push({ text: '', is_correct: false });
			}}>Новый вариант ответа</button
		>
	</div>
</div>
