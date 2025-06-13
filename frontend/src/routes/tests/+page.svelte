<script lang="ts">
	import { onMount } from 'svelte';
	import type { TestModelWithID } from '$lib/types.ts';
	import Test from '$lib/Test.svelte';

	let username: string | null = null;
	let tests: TestModelWithID[] = $state([]);
	let currentTest: TestModelWithID | null = $state(null);
	async function fetchUsername() {
		const response = await fetch('/api/me');
		const body = await response.json();
		username = body.username;
	}

	async function fetchAssignedTests(username: string) {
		const params = new URLSearchParams({ username: username });
		const response = await fetch('/api/tests/assigned?' + params);
		tests = await response.json();
	}
	onMount(async () => {
		await fetchUsername();
		if (username !== null) {
			await fetchAssignedTests(username);
		}
	});
</script>

<aside
	class="resize:horizontal border-r-double border-surface-50-950 fixed top-0 left-0 z-10 z-40 flex mt-20
	h-full w-40 -translate-x-full translate-x-0 flex-col overflow-x-hidden overflow-y-scroll text-wrap lg:w-64"
>
	{#if tests !== null}
		{#each tests as test (test.id)}
			<button
				onclick={() => {
					currentTest = test;
				}}
				class:bg-primary-800-200={currentTest?.id == test.id}
				class:text-surface-50-950={currentTest?.id == test.id}
				class="btn btn-lg rounded-none"
			>
				<p style="overflow: hidden; text-overflow: ellipsis;">{test.title}</p>
			</button>
		{/each}
	{/if}
</aside>
<div class="ml-40 p-4 pb-0 lg:ml-64">
	{#if currentTest !== null}
		{#key currentTest.id}
			<Test test={currentTest} />{/key}
	{/if}
</div>
