<script>
    import { goto } from '$app/navigation'
    import { onMount } from 'svelte';
    let placeholder = 'Enter the name of the stock...'
    let stock = null;
    let error = false;
    let tickers = [];
    let data_received = null;
    const api_send_ticker_dev = 'http://localhost:5000/yfinance/get_price'
    const api_get_tickers_dev = 'http://localhost:5000/yfinance/get_stocks'
    const api_get_prompts_dev = 'http://localhost:5000/api/ticker'


    const send_data = async () => {
        let response = await fetch(api_get_tickers_dev)
        return await response.json()
    }
    onMount(async()=> {
        data_received = await send_data()
        for(const i in data_received['infos']){
            tickers = [...tickers, data_received['infos'][i]]
        }
        console.log(tickers)
    })
    
    const send_ticker = async () => {
        if (!stock){
            //error message
            return
        }
        let response = await fetch(api_send_ticker_dev, {
            method: 'POST',
            headers:{
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'ticker':stock})
        })
        const data = await response.json()
        if(response.status == 200){
            //do something
            sessionStorage.setItem('stock', stock)
            sessionStorage.setItem('price', data.price)
            await get_prompts()
            await goto('/informations')
        }else if(response.status == 400){
            //tell the user the stock is invalid
            error = true;
            return
        }
        //do something with the thing that came from the stuff with the whatchumacallit
    }
    const get_prompts = async () => {
        let response = await fetch(api_get_prompts_dev, {
            method:'POST',
            headers:{
                'Content-Type': 'application/json'
            },
            body:JSON.stringify({'ticker':stock})
        })
        let data = await response.json()
        let fundamental = data['fund']
        let technical = data['tech']
        sessionStorage.setItem('fund', fundamental)
        sessionStorage.setItem('tech', technical)
    }
</script>

<main class='flex flex-col items-center h-screen bg-stone-800'>
    <input type="text" 
    class='w-3/5 h-14 rounded-xl py-2 mt-40 text-lg text-center bg-stone-600 focus:outline-none text-white'
    placeholder={placeholder}
    bind:value={stock}
    on:keypress ={async(event) => {
        if(event.key == 'Enter'){
            await send_ticker()
        }
    }}
    on:input={() => {
        placeholder = ''
        error = false;
        if(stock == ''){
            placeholder = 'Enter the name of the stock...'
        }
    }}>
    {#if error}
    <div>
        <p class='text-sm text-red-400 mt-1'>Please enter a valid ticker</p>
    </div>
    {/if}
    <button class='mt-5 rounded-lg py-2 px-1 bg-black text-white hover:bg-stone-900'
    on:click={async() => {
        await send_ticker()
    }}
    >Get information</button>
    <div class='flex flex-grow items-center w-full h-full justify-center overflow-hidden'>
        <div class='animate-scroll inline-flex h-full items-center gap-10'>
             {#each tickers as ticker}
             <div class="border rounded-lg bg-white px-1 py-2 h-1/2 w-72 shadow-lg flex flex-col">
                <div class='w-full text-xl font-mono text-center mb-3'>
                    {ticker['name']}
                </div>
                <div class='w-full ml-2 flex flex-col font-serif text-lg gap-2'>
                    <div>
                        Ticker: {ticker['symbol']}
                    </div>
                    <div>
                        Current Price: {ticker['price']}$
                    </div>
                    <div>
                        High: {ticker['high']}$
                    </div>
                    <div>
                        Low: {ticker['low']}$
                    </div>
                    <div>
                        Price Target: {ticker['target']}$
                    </div>
                </div>
             </div>
             {/each}
             {#each tickers as ticker}
             <div class="border rounded-lg bg-white px-1 py-2 h-1/2 w-72 shadow-lg">
                <div class='w-full text-xl font-mono text-center mb-3'>
                    {ticker['name']}
                </div>
                <div class='w-full ml-2 flex flex-col font-serif text-lg gap-2'>
                    <div>
                        Ticker: {ticker['symbol']}
                    </div>
                    <div>
                        Current Price: {ticker['price']}$
                    </div>
                    <div>
                        High: {ticker['high']}$
                    </div>
                    <div>
                        Low: {ticker['low']}$
                    </div>
                    <div>
                        Price Target: {ticker['target']}$
                    </div>
                </div>
             </div>
             {/each}
        </div>
       
    </div>
</main>
