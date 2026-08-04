#
# theme.py
#
# Gestione temi grafici
#
# Copyright 2026
#


class ThemeManager:


    ############################################################

    def __init__(self):

        self.current = "light"


        self.themes = {


            "light": {


                "background": "#F0F0F0",

                "foreground": "#000000",

                "entry": "#FFFFFF",

                "button": "#DDDDDD",

                "frame": "#FFFFFF"

            },


            "dark": {


                "background": "#202020",

                "foreground": "#FFFFFF",

                "entry": "#303030",

                "button": "#404040",

                "frame": "#252525"

            }


        }



    ############################################################

    def set_theme(
            self,
            name):


        if name in self.themes:

            self.current = name



    ############################################################

    def toggle(self):


        if self.current == "light":

            self.current = "dark"

        else:

            self.current = "light"



    ############################################################

    def get_theme(self):


        return self.themes[

            self.current

        ]



    ############################################################

    def get_color(
            self,
            element):


        theme = self.get_theme()


        return theme.get(

            element,

            "#FFFFFF"

        )



    ############################################################

    def is_dark(self):


        return self.current == "dark"



    ############################################################

    def apply_tkinter(
            self,
            widget):


        """
        Applica il tema ricorsivamente
        ai widget tkinter.
        """


        colors = self.get_theme()



        try:

            widget.configure(

                bg=colors["background"],

                fg=colors["foreground"]

            )


        except:

            pass



        try:

            for child in widget.winfo_children():

                self.apply_tkinter(

                    child

                )


        except:

            pass