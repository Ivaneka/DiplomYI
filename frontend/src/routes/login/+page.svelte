<script lang="ts">
	import Login from '$lib/Login.svelte';
	import Signup from '$lib/Signup.svelte';
	import { Tabs } from '@skeletonlabs/skeleton-svelte';

	let selectedTab = $state('login');
</script>

<svelte:head>
	<title>Login - Simple Messenger</title>
</svelte:head>

<div id="container" class="h-screen flex-col items-center justify-center">
	<div id="tabs-container" class="h-48 w-96">
		<Tabs value={selectedTab} onValueChange={(e) => (selectedTab = e.value)} fluid>
			{#snippet list()}
				<Tabs.Control value="login">Войти</Tabs.Control>
				<Tabs.Control value="signup">Создать аккаунт</Tabs.Control>
			{/snippet}
			{#snippet content()}
				<Tabs.Panel value="login"><Login /></Tabs.Panel>
				<Tabs.Panel value="signup"><Signup onsignup={() => (selectedTab = 'login')} /></Tabs.Panel>
			{/snippet}
		</Tabs>
	</div>
</div>

<style>
	#container {
		display: flex;
		flex-direction: column;
	}
</style>
