from typing import Callable, Optional, Tuple, Union
from customtkinter import CTkFrame
from customtkinter import CTkButton
from customtkinter import CTkToplevel
from customtkinter import CTkEntry
from customtkinter import CTkLabel
from customtkinter import CTkCanvas
from customtkinter import CTk
from tkinter import Event
from customtkinter import StringVar
from tkinter.ttk import Separator
from tkinter import Label
import tkinter as tk
from tkinter.font import Font

from customtkinter.windows.widgets.font import CTkFont
from customtkinter.windows.widgets.image import CTkImage

class SexyAssExceptions(Exception):

    def __init__(self, msg: str, *args: object) -> None:
        super().__init__(*args)
        print(msg)


class SexyAssBar(CTkToplevel):

    title_font: tuple = ("AngsanaUPC", 12)
    search_font: tuple = ("AngsanaUPC", 12)
    options_font: tuple = ("AngsanaUPC", 12)

    menu_btn_bg_color = "transparent"
    item_hover_color = "#144870"
    menu_fg_color = "#363636"
    border_color = "#48494B"

    __menu_object = {}
    __open_menu = None

    def __init__(self, master: CTk, lenght: int = 500, spacer: int = 70,**kwargs) -> None:
        self.lenght = lenght
        super().__init__(master=master, **kwargs)

        # Set private variables
        self.master = master
        self.__spacer = spacer

        # disable window manager
        self.overrideredirect(1)

        # remove toplevel from tool bar 
        self.attributes('-toolwindow', True)

        # Bring toplevel to front
        self.attributes('-topmost', 'true')

        # Remove background from topleve window
        bg_color = self["background"]
        self.attributes("-transparent", bg_color)

        # A-line topleve with root
        self.__locator()

        self.__frame()

        # Bind features to master window
        self.master.bind("<Configure>", self.__locator, add=True)

        self.master.bind("<Map>", self.__map_tool_bar, add=True)

        self.master.bind("<Unmap>", self.__unmap_tool_bar, add=True)

        self.master.bind("<FocusOut>", self.__master_focus, add=True)

        self.master.bind("<FocusIn>", self.__master_focus, add=True)

        self.bind("<FocusOut>", self.__title_focus, add=True)

        self.bind("<FocusIn>", self.__title_focus, add=True)

    def __locator(self, e: Event = None):
        """relocate top level"""

        __root_x = self.master.winfo_x()
        __root_y = self.master.winfo_y()
        # __root_t = self.master.title()

        self.geometry(f"{self.lenght}x30+{__root_x+self.__spacer}+{__root_y}")

        return
    
    def __frame(self, e: Event = None):
        """Add a frame to top level"""

        self.main_frame = CTkFrame(master=self, fg_color="transparent", bg_color="transparent", height=30)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack_configure(side="top", fill="x")
        self.main_frame.pack()

        return
    
    def __map_tool_bar(self, e: Event = None) -> None:
        """React to changes in root size"""
        
        state = self.master.state() # Get roots state

        items = self.main_frame.winfo_children()

        # Change padding according to windows size/location
        if state == "normal":
            self.state(newstate="normal")

            for i in items:

                i.pack_configure(pady=(5,5))

        elif state == "zoomed":
            self.state(newstate="normal")

            for i in items:

                i.pack_configure(pady=(10,0))

        self.__locator()

        del items

        return

    def __unmap_tool_bar(self, e: Event = None) -> None:
        """Unmap tool bar when root is minimised"""

        self.state(newstate="withdraw")

        try:
            self.withdraw()
        except AttributeError:
            pass

        return

    def __master_focus(self, e: Event = None):
        """if window no focus check if tool bar focus"""

        # Get focus information
        bar_focus = self.focus_displayof()
        root_focus = self.master.focus_displayof()

        topmost = self.attributes("-topmost")

        if root_focus == None and bar_focus == None:

            if root_focus == None and bar_focus == None:
                # Close dropmenu if focuse is lost
                try:
                    if self.__menu_container:
                        self.__destroy_menu()
                except AttributeError:
                    pass

            # remove topmost from bar and focus
            self.focus()
            self.attributes('-topmost', 'false')
        
        else:

            if topmost == 0:

                self.attributes('-topmost', 'true')

        return
    
    def __title_focus(self, e: Event = None):
        """if title bar not in focus check window"""

        # Get focus information
        bar_focus = self.focus_displayof()
        root_focus = self.master.focus_displayof()

        topmost = self.attributes("-topmost")

        if root_focus == None and bar_focus == None:

            if root_focus == None and bar_focus == None:
                # Close dropmenu if focuse is lost
                try:
                    if self.__menu_container:
                        self.__destroy_menu()
                except AttributeError:
                    pass

            # remove topmost from bar and focus
            self.focus()
            self.attributes('-topmost', 'false')
        
        else:

            if topmost == 0:
                self.attributes('-topmost', 'true')

        return
    
    def __menu_locator(self, title: str) -> None:
        """locate the menu title to ensure the dropmenu opens in correct place"""

        try:
            if not self.__menu_container:
                return
        except AttributeError as em:
            pass

        state = self.master.state()

        __bar_x = self.winfo_x()
        __bar_y = self.winfo_y()

        __title_x = self.__menu_object[f"{title}_menu"]["title"].winfo_x()
        __title_y = self.__menu_object[f"{title}_menu"]["title"].winfo_y()

        __absolute_x = __bar_x + __title_x
        __absolute_y = __bar_y + __title_y

        if state == "normal":
            try:
                self.__menu_container.geometry(f"+{__absolute_x}+{__absolute_y+25}")
            except Exception:
                pass
        elif state == "zoomed":
            try:
                self.__menu_container.geometry(f"+{__absolute_x}+{__absolute_y+25}")
            except Exception:
                pass
            
    def __destroy_menu(self, e: Event = None):
        """destroy open menu"""
        if self.__menu_container:
            self.__menu_container.destroy()
            self.__menu_container.update()
            self.__open_menu = None
            del self.__menu_container

        return
    
    def __hover_load(self, e: Event, title: str):
        """only allow hover load if a menu is open"""
        try:
            if type(e.widget) == Label:
                requested = e.widget.cget("text")
                if self.__menu_container and requested != self.__open_menu:
                    self.__load_menu(e=e, title=title)
        except AttributeError:
            return

    def __load_menu(self, e, title: str):
        """"""

        try:
            if self.__menu_container:
                current = e.widget.cget("text")
                if current == self.__open_menu:
                    self.__destroy_menu()
                    return
                else:
                    self.__destroy_menu()
        except AttributeError:
            pass

        # Create the menu container
        self.__menu_container = CTkToplevel(master=self)

        self.__menu_container.config(cursor="hand2")

        self.__menu_container.overrideredirect(1)

        self.__menu_container.attributes('-topmost', 'true')
        
        self.__menu_container.attributes('-toolwindow', True)

        bg_color = self.__menu_container["background"]

        self.__menu_container.attributes("-transparent", bg_color)

        self.__menu_locator(title=title)

        self.master.bind("<Button-1>", lambda e: self.__destroy_menu(e=e))

        self.bind("<Configure>", lambda e: self.__menu_locator(title=title))

        # add background color to menu
        panel_container = CTkFrame(master=self.__menu_container, fg_color=self.menu_fg_color, border_color=self.border_color, border_width=0.5)
        panel_container.pack_configure(side="top", fill="both", expand=True, padx=(5,5), pady=(5,5))
        panel_container.pack()

        panel = CTkFrame(master=panel_container, fg_color="transparent", bg_color="transparent", border_width=0)
        panel.pack_configure(side="top", fill="both", expand=True, padx=(5,5), pady=(5,5))
        panel.pack()

        # add options to menu container
        options = self.__menu_object[f"{title}_menu"]["options"]

        for option in options:   
            if option == "-sep-":
                sep = CTkFrame(master=panel, bg_color=self.border_color, height=1, border_color=None)
                sep.pack_configure(side="top", fill="x", expand=True, pady=(5,5))
                sep.pack()
                continue

            text = option["title"]

            # Check for shortcut
            shortcut = None
            submenu = False

            try:
                shortcut = option[f"shortCut"]
            except KeyError:
                pass

            try:
                submenu = option[f"subMenu"]
            except KeyError:
                pass

            button_frame = CTkFrame(master=panel, width=300)
            button_frame.pack_propagate(False)
            button_frame.pack()
            button_frame.columnconfigure(0, weight=1)
            button_frame.columnconfigure(1, weight=1)

            item = self.MenuBtn(master=button_frame, title=text, hover_color=self.item_hover_color, 
                           short_cut=shortcut, bg_color=self.menu_fg_color, font=self.options_font, 
                           sub_menu=submenu)
            
            item.grid_configure(row=0, column=0)
            item.grid()

        self.__open_menu = title    

    def add_search_bar(self, placeholder: str = "Search", width: int = 300, **kwargs):

        if hasattr(self, "__search_field") == True:
            return

        __search_field = CTkEntry(master=self.main_frame, placeholder_text=placeholder, **kwargs, 
                                  height=20, width=width, font=self.search_font)
        __search_field.pack_configure(side="left", padx=(5,5), pady=(5,5))
        __search_field.pack()

        __search_field.bind("<Button-1>", self.__destroy_menu)
        __search_field.bind("<FocusOut>", __search_field.update())

        return
    
    def add_menu(self, title: str):
        """Add menu to tool bar"""

        size = len(title)

        menu_title = CTkButton(master=self.main_frame, text=title, fg_color="transparent",
                               width=size*2, height=20, font=self.title_font)
        
        menu_title.pack_configure(side="left", padx=(5,5), pady=(5,5), anchor="s")
        menu_title.pack()

        menu_title.bind("<Button-1>", lambda e: self.__load_menu(e=e, title=title), add=True)
        menu_title.bind("<Enter>", lambda e: self.__hover_load(e=e, title=title), add=True)

        self.__menu_object[f"{title}_menu"] = {"title": menu_title, "options": []}

        options = self.__menu_object[f"{title}_menu"]["options"]

        return self.Add_options(menu_object=options, title=title)

    def update_font(self, select: str = "all", font: str = "AngsanaUPC", size: int = 12) -> None:
        """update tool bar fonts"""

        if select == "all":

            self.title_font = (font, size)
            self.search_font = (font, size)
            self.options_font = (font, size)
        
        elif select == "title":

            self.title_font = (font, size)

        elif select == "search":

            self.search_font = (font, size)

        elif select == "options":

            self.options_font = (font, size)
        
        else:
            
            msg = f"incorrect selection: _{select}: accepted ['title', 'search', 'option'] "
            raise SexyAssExceptions(msg=msg)
        
    class Add_options:

        def __init__(self, menu_object: list, title: str):
            """"""
            self.menu_object = menu_object
            self.title = title

        def __str__(self) -> str:
            """return menu title"""
            return self.title

        def __len__(self):
            """Return menu lenght"""
            return len(self.menu_object)

        def add_option(self, label: str, short_cut: str = None, sub_menu: bool = False, **kwargs):
            """Add option to menu"""

            __item = {"title":label, "shortCut":short_cut, "subMenu":sub_menu}

            self.menu_object.append(__item)

            return

        def add_separator(self, loc: int = None) -> None:
            """adds a separator to the list"""

            indicator = "-sep-"

            if loc == None:
                self.menu_object.append(indicator)

            else:
                try:
                    self.menu_object.insert(loc,indicator)
                except IndexError as em:
                    raise em
                
    class MenuBtn(CTkFrame):

        def __init__(self, master: any, title: str, hover_color: str, font: tuple, short_cut: str = None, 
                     sub_menu: bool = False, **kwargs):
            super().__init__(master, **kwargs)

            if short_cut == None or sub_menu == False:
                width = 200
            else:
                width = 300

            self.master = master

            color = self.cget("bg_color")

            title_var = StringVar()
            title_var.set(value=title)

            self.configure(width=width, height=25, fg_color=color)
            self.grid_propagate(False)

            self.pack()
            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)

            btn_label = CTkLabel(master=self, fg_color="transparent", text=title, anchor="w", font=font)
            btn_label.grid_configure(row=0, column=0, padx=(5,5), pady=(5,5), sticky="w")
            btn_label.grid()

            if short_cut != None and isinstance(short_cut, str) == True:
                short_cut_label = CTkLabel(master=self, fg_color="transparent", bg_color=color, 
                                           text=short_cut, anchor="e", font=font, height=20)
                short_cut_label.grid_configure(row=0, column=1, padx=(5,5), pady=(5,5))
                short_cut_label.grid()

            self.bind("<Enter>", lambda e: self.configure(fg_color=hover_color))
            self.bind("<Leave>", lambda e: self.configure(fg_color=color))

            btn_label.bind("<Enter>", lambda e: self.configure(fg_color=hover_color))
            btn_label.bind("<Leave>", lambda e: self.configure(fg_color=color))
        
