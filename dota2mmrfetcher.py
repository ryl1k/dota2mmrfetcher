import aiohttp
import asyncio

#fetch mmr
async def fetch_mmr(session, base_url, account_id, api_key):
    url = f"{base_url}{account_id}"
    headers = {'Content-Type': 'application/json'}

    async with session.get(url, params={'api_key': api_key}, headers=headers) as response:
        if response.status == 200:
            player_data = await response.json()
            player_name = player_data.get('profile', {}).get('personaname', 'N/A')
            mmr = player_data.get('mmr_estimate', {}).get('estimate', 'N/A')
            return player_name, mmr
        else:
            return 'Error', 'N/A'

async def main():
    # Replace with your Steam API key
    api_key = 'YOUR_STEAM_API_KEY'

    # List of Dota 2 player account IDs
    account_ids = []
    # Dota 2 API URL
    base_url = 'https://api.opendota.com/api/players/'

    async with aiohttp.ClientSession() as session:
        tasks = []

        # Create a list of tasks for asynchronous requests
        for account_id in account_ids:
            task = fetch_mmr(session, base_url, account_id, api_key)
            tasks.append(task)

        # Execute all tasks concurrently
        mmr_data = await asyncio.gather(*tasks)

        # Process the results and build the response message
        for player_name, mmr in mmr_data:
            print(f"{player_name}: {mmr} MMR")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())