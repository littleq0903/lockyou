#!/usr/bin/env python

# example base.py

import pygtk
pygtk.require('2.0')
import gtk
import webkit
import os

INDEX_FILE = "file://%s/index.html" % os.path.join(os.path.split(os.path.abspath(__file__))[0:-1])

class Base:
    def __init__(self):
        """
            self.window: gtk window object
            self.webview: webkit webview object
        """
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.show()
        self.webview = webkit.WebView()
        self.webview.load_uri(INDEX_FILE)
        self.window.add(self.webview)
        self.window.show_all()
        self.window.fullscreen()
        self.window.set_keep_above(True)


        # Events binding
        self.window.connect('destroy', lambda x: gtk.main_quit())
        self.window.connect('size-request', self.size_changed)
        self.webview.connect('notify::title', self.title_changed)
        
    def title_changed(self, webview, *params):
        if not webview.get_title():
            return
        if webview.get_title().startswith("topython:::"):
            command = webview.get_title().split(":::", 1)[1]
            if command == 'exit':
                gtk.main_quit()

    def size_changed(self, window, *params):
            window.fullscreen()

    def main(self):
        gtk.main()



if __name__ == "__main__":
    base = Base()
    base.main()
