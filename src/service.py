#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from soup import Soup
import json
from service_exceptions import NoPermissions, InvalidSoupId

import cherrypy

class RESTResource(object):
   """
   Base class for providing a RESTful interface to a resource.

   To use this class, simply derive a class from it and implement the methods
   you want to support.  The list of possible methods are:
   handle_GET
   handle_PUT
   handle_POST
   handle_DELETE
   """
   @cherrypy.expose
   def default(self, *vpath, **params):
      """
      According to the requested web service, this method selects the one method to handle it
      """
      method = getattr(self, "handle_" + cherrypy.request.method, None)
      if not method:
         methods = [x.replace("handle_", "")
            for x in dir(self) if x.startswith("handle_")]
         cherrypy.response.headers["Allow"] = ",".join(methods)
         raise cherrypy.HTTPError(405, "Method not implemented.")
      return method(*vpath, **params);

class alphabetResource(RESTResource):
    """
    Implemets the RESTful service
    """
    def handle_GET(self, *vpath, **params):
        """
        Handles GET request
        """
        if len(vpath) == 3:
            if vpath[2] not in cherrypy.session:
                raise InvalidSoupId()
            if vpath[1] == 'list':
                return json.dumps({'words':cherrypy.session[vpath[2]].words})#JSON
            elif vpath[1] == 'view':
                return str(cherrypy.session[vpath[2]])#TEXTO PLANO
            raise Exception("list or view should be in the GET path")
        raise Exception("path should have exactly 3 arguments")


    def handle_POST(self, *vpath, **params):
        """
        Handles POST request
        """
        if vpath[0] == 'alphabetSoup':
            try:
                s = Soup(params['w'],params['h'],params['ltr'],params['rtl'],params['ttb'],params['btt'],params['d'])
                cherrypy.session[s.id] = s
            except NoPermissions:
                json.dumps({'message':'No se otorgaron permisos para la creacion de la sopa'})#JSON
            except Exception:
                json.dumps({'message':'Error. Intente de nuevo mas tarde'})#JSON
            return json.dumps({'id':s.id})#JSON
        raise Exception("Path should have exactly one argument, alphabetSoup")

    def handle_PUT(self, *vpath, **params):
        """
        Handles PUT request
        """
        if len(vpath) != 2:
            raise Exception("PUT method should have length 2 path")
        if vpath[0] == 'alphabetSoup':
            if vpath[1] not in cherrypy.session:
                raise InvalidSoupId()
            soup = cherrypy.session[vpath[1]]
            found = soup.find(params['sr'], params['sc'], params['er'], params['ec'])
            message = 'La palabra'+ (' ' if found else ' NO ') +'ha sido encontrada satisfactoriamente'
            if soup.finished:
                message += '. Con esta palabra, has encontrado todas, felicidades!'
            return json.dumps({'message': message})
        else:
            raise Exception("Non recognized first path element, did you mean alphabetSoup?")


if __name__ == '__main__':
    #we want to save sessions
    conf = {
        '/': {
            'tools.sessions.on': True
        }
    }
    service = alphabetResource()
    cherrypy.quickstart(service, '/', conf)
