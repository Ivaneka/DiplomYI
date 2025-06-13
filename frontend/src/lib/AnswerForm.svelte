<script lang="ts">
	import type { AnswerModel } from '$lib/types';
	let { answer }: { answer: AnswerModel } = $props();
</script>

<div>
	<input type="text" bind:value={answer.text} placeholder="Текст ответа" />
	<input type="checkbox" bind:checked={answer.is_correct} />
</div>
