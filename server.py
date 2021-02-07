import aiohttp
import asyncio
import ssl
from httpclient import HttpClient,SetWebHook
from dialog_flow_api import DialogFlowApiManager
from aiohttp import  web
from ELIZA.message_handler import MessageHandler
from ELIZA.eliza_two import analyze
SetWebHook().set_web_hook()
router=web.RouteTableDef()

message_handler=MessageHandler()


@router.post('/1365051067:AAHIxSr2WCPuGqkukq0pHLQCupuEiGA6N3w')
async def handler(request:web.Request):

    response_dict = await request.json()

    if ('sticker' in response_dict['message']):
        file_id = response_dict['message']['sticker']['file_id']
        chat_id = response_dict['message']['chat']['id']
        paylo_ad = dict()
        paylo_ad.update(chat_id=chat_id, sticker=file_id)
        await HttpClient().post_data_to_server('sendSticker', paylo_ad)
        return web.Response(status=200)

    elif ('photo' in response_dict['message']):
        file_id = response_dict['message']['photo'][0]['file_id']
        chat_id = response_dict['message']['chat']['id']
        paylo_ad = dict()
        paylo_ad.update(chat_id=chat_id, photo=file_id)
        await HttpClient().post_data_to_server('sendPhoto', paylo_ad)
        return web.Response(status=200)


    elif ('animation' in response_dict['message']):
        file_id = response_dict['message']['animation']['file_id']
        chat_id = response_dict['message']['chat']['id']
        paylo_ad = dict()
        paylo_ad.update(chat_id=chat_id, animation=file_id)
        await HttpClient().post_data_to_server('sendAnimation', paylo_ad)
        return web.Response(status=200)

    else:
        chat_id = response_dict['message']['chat']['id']
        message = response_dict['message']['text']
        # result_message = messageHandler.get_answer(message)
        result_message=analyze(message)






        paylo_ad = dict()
        paylo_ad.update(chat_id=chat_id, text=result_message)
        await HttpClient().post_data_to_server('sendMessage', paylo_ad)
        return web.Response(status=200)

async def init_app():

    app=web.Application(debug=True)

    app.add_routes(router)
    return app

sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
sslcontext.load_cert_chain('webhook_cert.pem','webhook_pkey.pem')


web.run_app(init_app(),port=8443,ssl_context=sslcontext)



