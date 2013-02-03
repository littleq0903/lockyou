#!/usr/bin/env python

# example base.py

import pygtk
pygtk.require('2.0')
import gtk
import webkit
import os
import PAM

INDEX_FILE = "file://%s/index.html" % os.path.join(os.path.split(os.path.abspath(__file__))[0:-1])

class Base:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.show()
        self.webview = webkit.WebView()
        self.webview.load_uri(INDEX_FILE)
        self.window.add(self.webview)
        self.window.show_all()
        self.window.fullscreen()
        self.window.set_keep_above(True)
        self.webview.execute_script(self.init_js())
        self.auth_name   = ""
        self.auth_secret = ""

        def title_changed(v, params):
            print 'title_changed: %s, %s' % (v, params)
            if not v.get_title():
                return
            if v.get_title().startswith("topython:::"):
                cmdparam = v.get_title().split(":::", 1)[1]
                command  = cmdparam.split("#", 1)[0]
                params   = cmdparam.split("#", 1)
                if len(params) > 1:
                    params = params[1]
                else:
                    params = ""
                if command == 'exit':
                    gtk.main_quit()
                if command == 'auth_name':
                    self.auth_name = params
                if command == 'auth_secret':
                    self.auth_secret = params
                if command == 'auth':
                    self.do_auth()

        self.window.connect('destroy', lambda x: gtk.main_quit())
        self.webview.connect('notify::title', title_changed)

    def do_auth(self):
        self.call_auth_done(self.auth(self.auth_name, self.auth_secret))

    # result: 1 or 0
    def call_auth_done(self,result):
        self.webview.execute_script("locker.is_auth = %s"%(result))
        self.webview.execute_script("auth_done()")


    def auth(self,user, secret):

        def provide_secret(auth, query_list, userData):
            return [(secret,0)]

        auth = PAM.pam()
        auth.start('passwd')
        auth.set_item(PAM.PAM_USER, user)
        auth.set_item(PAM.PAM_CONV, provide_secret)
        try:
                auth.authenticate()
        except PAM.error,resp:
                print '%s' % resp
                return 0
        except:
                print 'Internal error'
        else:
                return 1

    def init_js(self):
        return """
            window.locker = 
            {
                is_auth: 0
    
                ,provide_name: function(name)
                {
                    document.title = 'topython:::auth_name#'+name
                }
        
                ,provide_secret: function(secret)
                {
                    document.title = 'topython:::auth_secret#'+secret
                }

                ,auth: function()
                {
                    document.title = 'topython:::auth'
                }
                
                ,unlock: function()
                {
                    document.title = 'topython:::exit'
                }
            }
        """

    def main(self):
        gtk.main()



if __name__ == "__main__":
    base = Base()
    base.main()

