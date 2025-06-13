<script lang="ts">
	let username: string = '';
	let password: string = '';
	let error: string | null = null;
	async function login() {
		error = null;
		const credentials = {
			username: username,
			password: password
		};
		const request = await fetch('/api/login', {
			method: 'POST',
			body: JSON.stringify(credentials),
			headers: {
				'Content-Type': 'application/json'
			}
		});
		if (!request.ok) {
			const errorText = await request.text();
			error = `Ошибка: ${errorText}`;
		} else {
			window.location.href = '/';
		}
	}
</script>

<div class="flex flex-col">
	<input
		type="text"
		id="username-input"
		bind:value={username}
		placeholder="логин"
		class="border-surface-200-800 rounded-t-md border p-2"
	/>
	<input
		type="password"
		id="password-input"
		bind:value={password}
		placeholder="пароль"
		class="border-surface-200-800 rounded-b-md border p-2"
	/>
	<button
		onclick={login}
		class="btn bg-primary-300-700 hover:bg-primary-400-600 mt-2 rounded-full p-2">Войти</button
	>
	<div class="text-error-500 p-4 text-center" class:invisible={error == null}>{error}</div>
</div>

<style>
</style>
