<script lang="ts">
	import { onMount } from 'svelte';
	import type { TestModelWithID, Attempt } from '$lib/types';
	import AttemptWidget from '$lib/AttemptWidget.svelte';

	let users: string[] = $state([]);
	let selectedUser: string = $state('');
	let tests: TestModelWithID[] = $state([]);
	let selectedTestID: number = $state(0);

	async function updateTests() {
		tests = [];
		const request = await fetch('/api/test');
		tests = await request.json();
	}

	onMount(async () => {
		const request = await fetch('/api/user');
		if (request.ok) {
			users = await request.json();
			selectedUser = users[0];
		}
		updateTests();
	});

	async function assignTest() {
		await fetch('/api/assign', {
			method: 'POST',
			body: JSON.stringify({ username: selectedUser, test_id: selectedTestID }),
			headers: { 'Content-Type': 'application/json' }
		});
	}
</script>

<div class="flex flex-row gap-4 justify-center">
	<select bind:value={selectedUser}>
		{#each users as user (user)}
			<option value={user}>{user}</option>
		{/each}
	</select>

	<select bind:value={selectedTestID}>
		{#each tests as test (test.id)}
			<option value={test.id}>{test.title}</option>
		{/each}
	</select>

	<button onclick={assignTest}>Назначить</button>
</div>
