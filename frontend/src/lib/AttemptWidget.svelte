<script lang="ts">
	import type { Attempt } from '$lib/types';
	let { attempt }: { attempt: Attempt } = $props();
	let recall = $derived.by(() => {
		let accurate = 0;
		for (const answer of attempt.attempt_answers) {
			if (answer.answer.is_correct) {
				accurate += 1;
			}
		}
		let res = accurate / attempt.attempt_answers.length;
		if (isNaN(res)) {
			res = 0;
		}
		return res;
	});
</script>

<div
	class="flex flex-col w-full items-left border-solid border-1 border-surface-950-50 rounded-xl p-4"
>
	Recall: {Math.round(recall * 100)}%
	<ul>
		{#each attempt.attempt_answers as answerWrapper (answerWrapper.answer.id)}
			<li>{answerWrapper.answer.text} {answerWrapper.answer.is_correct ? '+' : 'x'}</li>
		{/each}
	</ul>
</div>
