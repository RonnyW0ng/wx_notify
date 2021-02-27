# -*- coding: utf-8 -*-

import web
from handle import Handle
from send import Sender

urls = (
        '/wx','Handle',
        '/send','Sender',
)
app = web.application(urls,globals())


if __name__ == "__main__":
    app.run()
