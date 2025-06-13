<script lang="ts">
	import type { QuestionModelWithID } from '$lib/types';
	let { question, selectedAnswers }: { question: QuestionModelWithID; selectedAnswers: number[] } =
		$props();
	function toggle(id: number) {
		const present = selectedAnswers.indexOf(id) != -1;
		if (present) {
			while (selectedAnswers.indexOf(id) != -1) {
				selectedAnswers.splice(selectedAnswers.indexOf(id));
			}
		} else {
			selectedAnswers.push(id);
		}
	}
	console.log(question);
</script>

<div>
	<p>{question.text}</p>
	<div>
		{#each question.answers as answer (crypto.randomUUID())}
			<p>{answer.text} <input type="checkbox" onchange={() => toggle(answer.id)} /></p>
		{/each}
	</div>
</div>
