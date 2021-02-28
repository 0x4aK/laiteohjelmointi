from collections import deque
import shelve
import os

import cherrypy


class Root(object):
    datafile = "/tmp/raspimonitor-data"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def data(self):
        data = {}

        with shelve.open(self.datafile) as db:
            for data_point, data_dictionary in db.items():

                data[data_point] = {}
                for key, value in data_dictionary.items():
                    data[data_point][key] = list(value) if isinstance(value, deque) else value

        return data


class Webserver:
    global_config = {'server.socket_port': 80,
                     'server.socket_host': "0.0.0.0",
                     'engine.autoreload.on': False,
                     'environment': "production"}

    app_config = {
        '/': {'tools.gzip.on': True,
              'tools.staticdir.on': True,
              'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
              'tools.staticdir.dir': "public",
              'tools.staticdir.index': "index.html"},
    }

    def start(self):
        cherrypy.config.update(self.global_config)
        cherrypy.tree.mount(Root(), '', self.app_config)
        cherrypy.engine.start()

    @staticmethod
    def quit():
        """ Prepares the webserver for exit """
        cherrypy.engine.exit()

    @staticmethod
    def join():
        """ Waits for the engine to exit """
        cherrypy.engine.block()
