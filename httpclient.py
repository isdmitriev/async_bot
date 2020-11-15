import asyncio
import aiohttp
class HttpClient(object):
    def __init__(self):
        self.url='https://api.telegram.org/bot1365051067:AAHIxSr2WCPuGqkukq0pHLQCupuEiGA6N3w/'



    async def get_data_from_server(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.telegram.org/bot1365051067:AAHIxSr2WCPuGqkukq0pHLQCupuEiGA6N3w/getUpdates') as response:
                result=await response.text()
                return result
    async def post_data_to_server(self,path,payLoad):
        fullUrl=self.url+path
        async with aiohttp.ClientSession() as session:

            await session.post(fullUrl,data=payLoad)
            


































    







