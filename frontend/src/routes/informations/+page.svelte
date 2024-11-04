<script>
    import {goto} from '$app/navigation'
    import { onMount } from 'svelte';
    let css_button = "border border-white rounded-lg px-6 py-4 text-white shadow-xl transition ease-in-out hover:scale-110"
    let stock = ''
    let price = ''

    onMount(() => {
        stock = sessionStorage.getItem('stock')
        price = sessionStorage.getItem('price')
    })
</script>

<main class='bg-stone-800 h-screen'>
    <div class='flex flex-col justify-center items-center h-full'>
        <div class='mb-28 flex justify-center w-full relative'>
            <button class='absolute left-5 top-5 border border-solid rounded-md bg-white px-2 py-1 hover:bg-gray-200'
            on:click={async() => {
                sessionStorage.removeItem('stock')
                sessionStorage.removeItem('price')
                await goto('../')
            }}
            >
                Go Back
            </button>
            <div class='flex flex-col w-full items-center mt-10'>
                <p class='text-5xl text-white font-mono py-2 px-1'>{stock}</p>
                <p class='text-4xl text-white font-mono py-2 px-1'>{price}$</p>
            </div>
        </div>
        <div class='w-full flex h-full justify-center mb-10'>
            <div class='border h-full w-2/3 rounded-md mr-2 flex flex-col justify-end pl-1'>
                <input class='mt-auto h-12 w-10/12 text-white rounded-lg focus:outline-none px-2 bg-stone-800'
                placeholder="Enter your question..."
                />
            </div>
            <div class='w-1/4 h-full rounded-md grid grid-rows-3 items-center justify-center'>
                <button class={css_button}>
                    General Analysis
                </button>
                <button class={css_button}>
                    Fundamental Analysis
                </button>
                <button class={css_button}>
                    Technical Analysis
                </button>
            </div>
        </div>
    </div>
</main>