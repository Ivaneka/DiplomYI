<script lang="ts">
	let { onsignup }: { onsignup: () => void } = $props();
	let username: string = $state('');
	let password: string = $state('');
	let passwordConfirmation: string = $state('');
	let error: string | null = $state(null);

	async function signup() {
		error = null;
		if (password != passwordConfirmation) {
			error = "Passwords don't match";
			return;
		}
		const credentials = {
			username: username,
			password: password
		};
		const request = await fetch('/api/signup', {
			method: 'POST',
			body: JSON.stringify(credentials),
			headers: {
				'Content-Type': 'application/json'
			}
		});
		if (!request.ok) {
			const text = await request.text();
			error = `Couldn't sign up: ${text}`;
			return;
		}
		onsignup();
	}
</script>

<div class="flex flex-col">
	<input
		type="text"
		id="username-input"
		bind:value={username}
		placeholder="username"
		class="border-surface-200-800 rounded-t-md border p-2"
	/>
	<input
		type="password"
		id="password-input"
		bind:value={password}
		placeholder="password"
		class="border-surface-200-800 border p-2"
	/>
	<input
		type="password"
		id="password-confirmation-input"
		bind:value={passwordConfirmation}
		placeholder="password again"
		class="border-surface-200-800 rounded-b-md border p-2"
	/>
	<button
		onclick={signup}
		class="btn bg-primary-300-700 hover:bg-primary-400-600 mt-2 rounded-full p-2">Sign up</button
	>
	<div class="text-error-500 p-4 text-center" class:invisible={error == null}>{error}</div>
</div>

<style>
</style>
