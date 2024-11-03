<script>
    import {goto} from '$app/navigation'
    import { onMount } from 'svelte';
    let css_button = "w-full border border-white rounded-lg h-full mx-2 transition ease-in-out hover:scale-105"
    let css_div = "flex flex-col justify-center items-center w-full h-full"
    let css_p = "mb-3"
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
            <button class='absolute left-5 border border-solid rounded-md bg-white px-2 py-1 hover:bg-gray-200'
            on:click={async() => {
                sessionStorage.removeItem('stock')
                sessionStorage.removeItem('price')
                await goto('../')
            }}
            >
                Go Back
            </button>
            <p class='text-5xl bg-white font-mono border rounded-lg py-2 px-1'>{stock}:{price}$</p>
        </div>
        <div class='grid grid-cols-3 w-full h-1/2  text-white items-center gap-4 mb-28'>
            <div class={css_div}>
                <p
                class={css_p}>Fundamental Analysis</p>
                <button class={css_button}
                on:click={async() => {
                    await goto('informations/fundamental')
                }}
                >
                    1
                </button>
            </div>
            <div class={css_div}>
                <p class={css_p}>Technical Analysis</p>
                <button class={css_button}
                on:click={async() => {
                    await goto('informations/technical')
                }}>
                   2
               </button>
           </div>
            <div class={css_div}>
                <p class={css_p}>News</p>
                <button class={css_button}
                on:click={async() => {
                    await goto('informations/news')
                }}>
                    3
                </button>
            </div>
        </div>
    </div>
</main>