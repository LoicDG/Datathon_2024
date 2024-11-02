<script>
    let placeholder = 'Enter the name of the stock...'
    let stock = null
    const api_send_ticker_dev = 'http://localhost:5000/api/ticker'
    
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
        if(response.status == 200){
            //do something
        }else if(response.status == 400){
            //tell the user the stock is invalid
            return
        }else{
            //idk
            return
        }
        const data = await response.json()
        //do something with the thing that came from the stuff with the whatchumacallit
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
        if(stock == ''){
            placeholder = 'Enter the name of the stock...'
        }
    }}>
    <button class='mt-5 border rounded-lg py-2 px-1 bg-white hover:bg-gray-200'
    on:click={async() => {
        await send_ticker()
    }}
    >Get information</button>
</main>
