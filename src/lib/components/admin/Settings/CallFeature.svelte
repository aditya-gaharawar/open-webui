<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { onMount, getContext } from 'svelte';
	import { getCodeExecutionConfig, setCodeExecutionConfig } from '$lib/apis/configs'; // Reuse existing API fns

	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import Switch from '$lib/components/common/Switch.svelte';

	const i18n = getContext('i18n');

	export let saveHandler: Function;

	let config = {
        // Provide default structure to avoid errors before load
        ENABLE_CALL_FEATURE: true
        // Other fields from CodeInterpreterConfigForm exist here too, but we only care about ENABLE_CALL_FEATURE
    };
    let initialLoading = true;


	const submitHandler = async () => {
        // Only proceed if config is loaded
        if (initialLoading) return;
		const res = await setCodeExecutionConfig(localStorage.token, config);
	};

	onMount(async () => {
		const res = await getCodeExecutionConfig(localStorage.token);

		if (res) {
			config = res;
            initialLoading = false;
		} else {
            toast.error(i18n.t('Failed to load Call Feature settings'));
            // Keep initialLoading true or handle error appropriately
        }
	});
</script>

<form
	class="flex flex-col h-full justify-between space-y-3 text-sm"
	on:submit|preventDefault={async () => {
        if (!initialLoading) {
            await submitHandler();
		    saveHandler(); // Call the parent save handler (shows success toast etc.)
        } else {
            toast.error(i18n.t('Settings not loaded yet, please wait.'));
        }
	}}
>
	<div class=" space-y-3 overflow-y-scroll scrollbar-hidden h-full">
		{#if !initialLoading}
			<div>
				<div class="mb-3.5">
					<div class=" mb-2.5 text-base font-medium">{$i18n.t('Call Feature')}</div>
					<hr class=" border-gray-100 dark:border-gray-850 my-2" />

					<div class="mb-2.5">
                        <div class=" flex w-full justify-between">
                            <div class=" self-center pr-4">
                                <div class="text-xs font-medium">
                                    {$i18n.t('Enable Call Feature')}
                                </div>
                                <div class="text-xs text-gray-500">
                                    {$i18n.t('Allows users to initiate voice interactions and enables backend tool/function calling capabilities for models.')}
                                </div>
                            </div>

                            <Switch bind:state={config.ENABLE_CALL_FEATURE} />
                        </div>
                    </div>
				</div>

                <!-- Placeholder for future call-specific settings -->
                <!--
                <div class="mb-3.5">
					<div class=" mb-2.5 text-base font-medium">{$i18n.t('Voice Settings (Example)')}</div>
					<hr class=" border-gray-100 dark:border-gray-850 my-2" />
                    <div class="text-xs text-gray-500">Future settings related to STT/TTS engines could go here.</div>
                </div>
                -->

			</div>
        {:else}
            <!-- Optional: Loading indicator -->
            <div class="p-4 text-center text-gray-500">{$i18n.t('Loading settings...')}</div>
		{/if}
	</div>

	<div class="flex justify-end items-center">
		<button
            disabled={initialLoading}
			class="disabled:opacity-50 disabled:cursor-not-allowed bg-gray-900 dark:bg-gray-800 hover:bg-gray-800 dark:hover:bg-gray-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition"
			type="submit"
		>
			{$i18n.t('Save Changes')}
		</button>
	</div>
</form>
