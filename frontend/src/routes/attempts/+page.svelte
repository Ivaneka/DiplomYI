<script lang="ts">
	import { onMount } from 'svelte';
	import type { TestModelWithID, Attempt } from '$lib/types';
	import AttemptWidget from '$lib/AttemptWidget.svelte';

	let users: string[] = $state([]);
	let selectedUser: string = $state('');
	let tests: TestModelWithID[] = $state([]);
	let selectedTestID: number = $state(0);
	let attempts: Attempt[] = $state([]);

	onMount(async () => {
		const request = await fetch('/api/user');
		if (request.ok) {
			users = await request.json();
			selectedUser = users[0];
		} else {
			const me = await fetch('/api/me')
				.then((r) => r.json())
				.then((o) => o.username);
			users = [me];
			selectedUser = me;
		}
	});

	async function updateTests() {
		tests = [];
		const params = new URLSearchParams({ username: selectedUser });
		const request = await fetch('/api/tests/assigned?' + params);
		tests = await request.json();
	}

	async function updateAttempts() {
		attempts = [];
		const params = new URLSearchParams({
			username: selectedUser,
			test_id: selectedTestID.toString()
		});
		const request = await fetch('/api/attempt?' + params);
		attempts = await request.json();
	}
	onMount(() => console.log(tests));
</script>

<div class="flex flex-row justify-center w-full p-4">
	<select
		bind:value={selectedUser}
		onchange={async () => {
			await updateTests();
			await updateAttempts();
		}}
		class="flex-1"
	>
		{#each users as user (crypto.randomUUID())}
			<option value={user}>{user}</option>
		{/each}
	</select>

	<select bind:value={selectedTestID} onchange={updateAttempts} class="flex-1">
		{#each tests as test (crypto.randomUUID())}
			<option value={test.id}>{test.title}</option>
		{/each}
	</select>
</div>

<div class="flex flex-col p-4 gap-4">
	{#each attempts as attempt (crypto.randomUUID())}
		<AttemptWidget {attempt} />
	{/each}
</div>
