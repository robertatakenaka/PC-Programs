# code: utf-8

import os

try:
    import Tkinter
except:
    pass


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
JOURNALS_CSV_URL = 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv'


def local_gettext(text):
    return text


try:
    from ..__init__ import _
except:
    _ = local_gettext


class ProxyChecker(object):

    def __init__(self, proxy_info):
        self.proxy_info = proxy_info

    def ask_proxy_data(self, debug=False):
        tk_root = Tkinter.Tk()
        tk_root.title(_('Proxy information'))
        tkFrame = Tkinter.Frame(tk_root)

        main = ProxyForm(tkFrame, self.server, self.port, debug)
        main.tkFrame.pack(side="top", fill="both", expand=True)

        tk_root.mainloop()
        tk_root.focus_set()

        r = main.info
        main = None
        if debug:
            print('proxy informed:')
            print(r)
        tk_root.destroy()
        return r

    def update(self):
        data = self.ask_proxy_data()
        if data is not None:
            self.proxy_info.server, self.proxy_info.port, self.proxy_info.user, self.proxy_info.password = data


class ProxyInfo(object):

    def __init__(self, server_and_port, user=None, password=None):
        self.server_and_port = server_and_port
        self.user = user
        self.password = password
        self.server, self.port = server_and_port.split(':')

    @property
    def handler_data(self):
        r = None
        if self.server_and_port is not None:
            proxy_handler_data = ''
            if self.user is not None and self.password is not None:
                proxy_handler_data = self.user + ':' + self.password + '@'
            proxy_handler_data += self.server_and_port
            r = {'http': 'http://'+proxy_handler_data, 'https': 'https://'+proxy_handler_data}
        return r


class ProxyForm(object):

    def __init__(self, tkFrame, registered_ip, registered_port, debug=False):
        self.info = None
        self.debug = False

        if registered_ip is None:
            registered_ip = ''
        if registered_port is None:
            registered_port = ''

        self.tkFrame = tkFrame

        self.tkFrame.labelframe_window = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.labelframe_window.pack(fill="both", expand="yes")

        self.tkFrame.labelframe_message = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=70)
        self.tkFrame.labelframe_message.pack(fill="both", expand="yes")
        self.tkFrame.label_message = Tkinter.Label(self.tkFrame.labelframe_message, text=_('This tool requires Internet access for some services, such as DOI, affiliations, and other data validations, and also to get journals data from SciELO.\n\nIf you do not use a proxy to access the Internet, and click on Cancel button.'), font="Verdana 12 bold", wraplength=450)
        self.tkFrame.label_message.pack()

        self.tkFrame.labelframe_proxy_ip = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=70)
        self.tkFrame.labelframe_proxy_ip.pack(fill="both", expand="yes")
        self.tkFrame.label_proxy_ip = Tkinter.Label(self.tkFrame.labelframe_proxy_ip, text='Proxy IP / server', font="Verdana 12 bold")
        self.tkFrame.label_proxy_ip.pack(fill="both", expand="yes")
        self.tkFrame.entry_proxy_ip = Tkinter.Entry(self.tkFrame.labelframe_proxy_ip)
        self.tkFrame.entry_proxy_ip.insert(0, registered_ip)
        self.tkFrame.entry_proxy_ip.pack()

        self.tkFrame.labelframe_proxy_port = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=5)
        self.tkFrame.labelframe_proxy_port.pack(fill="both", expand="yes")
        self.tkFrame.label_proxy_port = Tkinter.Label(self.tkFrame.labelframe_proxy_port, text='Proxy Port', font="Verdana 12 bold")
        self.tkFrame.label_proxy_port.pack(fill="both", expand="yes")
        self.tkFrame.entry_proxy_port = Tkinter.Entry(self.tkFrame.labelframe_proxy_port)
        self.tkFrame.entry_proxy_port.insert(0, registered_port)
        self.tkFrame.entry_proxy_port.pack()

        self.tkFrame.labelframe_proxy_user = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=70)
        self.tkFrame.labelframe_proxy_user.pack(fill="both", expand="yes")
        self.tkFrame.label_proxy_user = Tkinter.Label(self.tkFrame.labelframe_proxy_user, text=_('user'), font="Verdana 12 bold")
        self.tkFrame.label_proxy_user.pack(fill="both", expand="yes")
        self.tkFrame.entry_proxy_user = Tkinter.Entry(self.tkFrame.labelframe_proxy_user)
        self.tkFrame.entry_proxy_user.pack()

        self.tkFrame.labelframe_proxy_password = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10, width=70)
        self.tkFrame.labelframe_proxy_password.pack(fill="both", expand="yes")
        self.tkFrame.label_proxy_password = Tkinter.Label(self.tkFrame.labelframe_proxy_password, text=_('password'), font="Verdana 12 bold")
        self.tkFrame.label_proxy_password.pack(fill="both", expand="yes")
        self.tkFrame.entry_proxy_password = Tkinter.Entry(self.tkFrame.labelframe_proxy_password, show='*')
        self.tkFrame.entry_proxy_password.pack()

        self.tkFrame.labelframe_buttons = Tkinter.LabelFrame(self.tkFrame, bd=0, padx=10, pady=10)
        self.tkFrame.labelframe_buttons.pack(fill="both", expand="yes")

        self.tkFrame.button_cancel = Tkinter.Button(self.tkFrame.labelframe_buttons, text=_('Cancel'), command=lambda: self.tkFrame.quit())
        self.tkFrame.button_cancel.pack(side='right')

        self.tkFrame.button_execute = Tkinter.Button(self.tkFrame.labelframe_buttons, text=_('OK'), command=self.register)
        self.tkFrame.button_execute.pack(side='right')

    def register(self):
        r = [self.tkFrame.entry_proxy_ip.get(), self.tkFrame.entry_proxy_port.get(), self.tkFrame.entry_proxy_user.get(), self.tkFrame.entry_proxy_password.get()]
        self.info = [None if item == '' else item for item in r]
        self.tkFrame.quit()
