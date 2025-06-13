<script lang="ts">
	import { marked } from 'marked';
	let title: string = '';
	let content: string = '';
	let error: string | null = null;
	async function createMaterial() {
		const response = await fetch('/api/material', {
			method: 'PUT',
			body: JSON.stringify({ title: title, content: content }),
			headers: { 'Content-Type': 'application/json' }
		});
		if (!response.ok) {
			const detail = await response.text();
			error = `Ошибка: ${detail}`;
			return;
		}
		error = null;
	}
</script>

<div class="flex flex-col h-full">
	<input bind:value={title} type="text" placeholder="Название материала" />
	<div class="flex flex-row flex-1 gap-1">
		<textarea bind:value={content} class="flex-1 p-1 resize-none" placeholder="Текст материала"
		></textarea>
		<div class="flex-1 p-1">{@html marked(content)}</div>
	</div>
	<button onclick={createMaterial}>Создать</button>
	<div class="text-error-500 p-4 text-center" class:invisible={error == null}>{error}</div>
</div>
