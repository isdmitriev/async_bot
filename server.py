import aiohttp
import asyncio
import ssl
from httpclient import HttpClient,SetWebHook
from DialogFlowApi import DialogFlowApiManager
from aiohttp import  web
from ELIZA.MessageHandler import MessageHandler
from ELIZA.eliza_two import analyze
SetWebHook().set_web_hook()
router=web.RouteTableDef()

messageHandler=MessageHandler()


@router.post('/1365051067:AAHIxSr2WCPuGqkukq0pHLQCupuEiGA6N3w')
async def handler(request:web.Request):

    responseDict = await request.json()

    if ('sticker' in responseDict['message']):
        fileId = responseDict['message']['sticker']['file_id']
        chatId = responseDict['message']['chat']['id']
        payloAd = dict()
        payloAd.update(chat_id=chatId, sticker=fileId)
        await HttpClient().post_data_to_server('sendSticker', payloAd)
        return web.Response(status=200)

    elif ('photo' in responseDict['message']):
        fileId = responseDict['message']['photo'][0]['file_id']
        chatId = responseDict['message']['chat']['id']
        payloAd = dict()
        payloAd.update(chat_id=chatId, photo=fileId)
        await HttpClient().post_data_to_server('sendPhoto', payloAd)
        return web.Response(status=200)


    elif ('animation' in responseDict['message']):
        fileId = responseDict['message']['animation']['file_id']
        chatId = responseDict['message']['chat']['id']
        payloAd = dict()
        payloAd.update(chat_id=chatId, animation=fileId)
        await HttpClient().post_data_to_server('sendAnimation', payloAd)
        return web.Response(status=200)

    else:
        chat_id = responseDict['message']['chat']['id']
        message = responseDict['message']['text']
        # result_message = messageHandler.get_answer(message)
        result_message=analyze(message)






        payloAd = dict()
        payloAd.update(chat_id=chat_id, text=result_message)
        await HttpClient().post_data_to_server('sendMessage', payloAd)
        return web.Response(status=200)

async def init_app():

    app=web.Application(debug=True)

    app.add_routes(router)
    return app

sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
sslcontext.load_cert_chain('webhook_cert.pem','webhook_pkey.pem')


web.run_app(init_app(),port=8443,ssl_context=sslcontext)



