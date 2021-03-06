from aiohttp import web
from aiohttp_xmlrpc import handler
from constants import XMLRPC_LISTEN_HOST, XMLRPC_LISTEN_PORT, APPLICATION_VERSION

class XMLRPCListener:

    class XMLRPCHandler(handler.XMLRPCView):
        def rpc_version(self):
            return APPLICATION_VERSION

    def __init__(self):
        self._app = web.Application()
        self._app.router.add_route('*', '/hamlog/agent/', self.XMLRPCHandler)

    async def start(self):
        runner = web.AppRunner(self._app)
        await runner.setup()
        self._site = web.TCPSite(runner, XMLRPC_LISTEN_HOST, XMLRPC_LISTEN_PORT, reuse_address=True)
        await self._site.start()

    async def stop(self):
        try:
            await self._site.stop()
        except:
            pass
