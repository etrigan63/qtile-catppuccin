# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
#from libqtile import layout, bar, widget, hook
from libqtile import layout, bar, hook
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.widget import Spacer
#import arcobattery

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')
terminal = "kitty"


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [

# Most of our keybindings are in sxhkd file - except these

# SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),


# SUPER + SHIFT KEYS

    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),


# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    ]

def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)

keys.extend([
    # MOVE WINDOW TO NEXT SCREEN
    Key([mod,"shift"], "Right", lazy.function(window_to_next_screen, switch_screen=True)),
    Key([mod,"shift"], "Left", lazy.function(window_to_previous_screen, switch_screen=True)),
])

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]

# FOR AZERTY KEYBOARDS
#group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

#group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
#group_labels = ["", "", "", "", "", "", "", "", "", "",]
group_labels = ["㊀", "㊁", "㊂", "㊃", "㊄", "㊅", "㊆", "㊇", "㊈", "㊉",]
#group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = ["monadthreecol", "monadthreecol", "monadthreecol", "monadthreecol", "monadthreecol", "monadthreecol", "monadthreecol", "monadthreecol", "monadthreecol", "monadthreecol",]
#group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin":5,
            "border_width":2,
            "border_focus": "#8CAAEE",
            "border_normal": "#626880"
            }

layout_theme = init_layout_theme()


layouts = [
    #layout.MonadTall(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    #layout.MonadTall(**layout_theme),
    layout.MonadThreeCol(**layout_theme),
    #layout.MonadWide(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    #layout.MonadWide(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Floating(**layout_theme),
    #layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme)
]

# COLORS FOR THE BAR
#Theme name : ArcoLinux Catppuccin Frappe
def init_colors():
    return [["#51576D", "#51576D"], # color 0
            ["#E78284", "#E78284"], # color 1
            ["#A6D189", "#A6D189"], # color 2
            ["#E5C890", "#E5C890"], # color 3
            ["#8CAAEE", "#8CAAEE"], # color 4
            ["#F4B8E4", "#F4B8E4"], # color 5
            ["#67afc1", "#67afc1"], # color 6
            ["#B5BFE2", "#B5BFE2"], # color 7
            ["#626880", "#626880"], # color 8
            ["#E78284", "#E78284"], # color 9
            ["#A6D189", "#A6D189"], # color 10
            ["#E5C890", "#E5C890"], # color 11
            ["#8CAAEE", "#8CAAEE"], # color 12
            ["#F4B8E4", "#F4B8E4"], # color 13
            ["#81C8BE", "#81C8BE"], # color 14
            ["#A5ADCE", "#A5ADCE"], # color 15
            ["#303446", "#303446"], # color 16 - background
            ["#C6D0F5", "#C6D0F5"]] # color 17 - foreground
colors = init_colors()


# WIDGETS FOR THE BAR

decor = {
    "decorations": [
        RectDecoration(colour=colors[0], radius=10, filled=True, padding_y=5)
    ],
    "padding": 10,
}
decor_left = {
    "decorations": [
        RectDecoration(colour=colors[0], radius=[10,0,0,10], filled=True, padding_y=5)
    ],
    "padding": 5,
}
decor_right = {
    "decorations": [
        RectDecoration(colour=colors[0], radius=[0,10,10,0], filled=True, padding_y=5)
    ],
    "padding": 5,
}
def init_widgets_defaults():
    return dict(font="RobotoMono Nerd Font",
                fontsize = 12,
                padding = 2,
                background=colors[16])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [ 
                widget.Image(
                        filename = "~/.config/qtile/python.png",
                        background = colors[16],
                        margin = 3,
                ),
               widget.GroupBox(font="FontAwesome",
                        **decor,
                        fontsize = 16,
                        #margin_y = -1,
                        #margin_x = 0,
                        #padding_y = 6,
                        #padding_x = 5,
                        borderwidth = 0,
                        disable_drag = True,
                        active = colors[9],
                        inactive = colors[17],
                        rounded = False,
                        highlight_method = "text",
                        this_current_screen_border = colors[2],
                        foreground = colors[2],
                        background = colors[16]
                        ),
               #widget.Sep(
                        #linewidth = 1,
                        #padding = 10,
                        #foreground = colors[2],
                        #background = colors[0]
                        #),
               widget.CurrentLayoutIcon(
                        **decor_left,
                        font = "RobotoMono Nerd Font Bold",
                        scale = .6,
                        foreground = colors[5],
                        background = colors[16]
                        ),
                widget.CurrentLayout(
                        **decor_right,
                        font = "RobotoMono Nerd Font Bold",
                        foreground = colors[5],
                        background = colors[16]
                        ),               
                #widget.Sep(
                        #linewidth = 1,
                        #padding = 10,
                        #foreground = colors[2],
                        #background = colors[0]
                        #),
                widget.Spacer (),
                widget.Systray(
                        background=colors[16],
                        icon_size=20,
                        padding = 4
                        ),
                widget.Spacer (),
                #widget.TextBox(
                #        **decor,
                #        font="FontAwesome",
                #        text="  ",
                #        foreground=colors[6],
                #        background=colors[16],
                #        #padding = 0,
                #        fontsize=16
                #        ),
                widget.Wttr(
                        **decor,
                        font = "RobotoMono Nerd Font",
                        fontsize = 12,
                        lang = 'en',
                        format='   %l: %c%m 🌡%t/%f',
                        location = {'Miami': 'Miami'},
                        units = 's',
                        update_interval = 300,
                        foreground = colors[5],
                        background = colors[16],
                        #padding = 0,
                        ),
                #widget.Sep(
                        #linewidth = 1,
                        #padding = 10,
                        #foreground = colors[2],
                        #background = colors[16]
                        #),
                #widget.TextBox(
                #        font="FontAwesome",
                #        text="  ",
                #        foreground=colors[9],
                #        background=colors[0],
                #        padding = 0,
                #        fontsize=16
                #        ),
                widget.CheckUpdates(
                        **decor,
                        font="RobotoMono Nerd Font",
                        fontsize=12,
                        distro='Arch_checkupdates',
                        update_interval=60,
                        display_format='  Updates: {updates}',
                        no_update_string='  No Updates',
                        foreground=colors[2],
                        background=colors[16],
                        colour_have_updates=colors[9],
                        colour_no_updates=colors[2],
                        #padding = 0,
                        ),
                #widget.Sep(
                        #linewidth = 1,
                        #padding = 10,
                        #foreground = colors[2],
                        #background = colors[16]
                        #),
                #widget.TextBox(
                #        **decor,
                #        font="FontAwesome",
                #        text="  ",
                #        foreground=colors[3],
                #        background=colors[16],
                        #padding = 0,
                #        fontsize=16
                #        ),
                widget.Net(
                        **decor,
                        font="RobotoMono Nerd Font",
                        fontsize=12,
                        format="  {interface}:  {up}  {down}",
                        interface="eno1",
                        foreground=colors[6],
                        background=colors[16],
                        ),
                #widget.Sep(
                        #linewidth = 1,
                        #padding = 10,
                        #foreground = colors[2],
                        #background = colors[16]
                        #),
               # # do not activate in Virtualbox - will break qtile
               # widget.ThermalSensor(
               #          foreground = colors[5],
               #          foreground_alert = colors[6],
               #          background = colors[1],
               #          metric = True,
               #          padding = 3,
               #          threshold = 80
               #          ),
               # # battery option 1  ArcoLinux Horizontal icons do not forget to import arcobattery at the top
               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               # arcobattery.BatteryIcon(
               #          padding=0,
               #          scale=0.7,
               #          y_poss=2,
               #          theme_path=home + "/.config/qtile/icons/battery_icons_horiz",
               #          update_interval = 5,
               #          background = colors[1]
               #          ),
               # # battery option 2  from Qtile
               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               # widget.Battery(
               #          font="RobotoMono Nerd Font",
               #          update_interval = 10,
               #          fontsize = 12,
               #          foreground = colors[5],
               #          background = colors[1],
	           #          ),
                #widget.TextBox(
                #        **decor,
                #        font="FontAwesome",
                #        text="  ",
                #        foreground=colors[6],
                #        background=colors[16],
                #        #padding = 0,
                #        fontsize=16
                #        ),
                widget.CPU(
                        **decor,
                        format="  {freq_current}GHz {load_percent}%",
                        background=colors[16],
                        core = "all",
                        ),
                #widget.Sep(
                        #linewidth = 1,
                        #padding = 10,
                        #foreground = colors[2],
                        #background = colors[16]
                        #),
                #widget.TextBox(
                #        **decor,
                #        font="FontAwesome",
                #        text="  ",
                #        foreground=colors[4],
                #        background=colors[16],
                #        #padding = 0,
                #        fontsize=16
                #        ),
                widget.Memory(
                        **decor,
                        font="RobotoMono Nerd Font",
                        format='  {MemUsed: .0f}{mm}/{MemTotal: .0f}{mm}',
                        update_interval = 1,
                        fontsize = 12,
                        foreground = colors[3],
                        background = colors[16],
                       ),
                #widget.Sep(
                        #linewidth = 1,
                        #padding = 10,
                        #foreground = colors[2],
                        #background = colors[16]
                        #),
                #widget.TextBox(
                #        **decor,
                #        font="FontAwesome",
                #        text="  ",
                #        foreground=colors[3],
                #        background=colors[16],
                #        #padding = 0,
                #        fontsize=16
                #        ),
                widget.Clock(
                        **decor,
                        foreground = colors[5],
                        background = colors[16],
                        fontsize = 12,
                        format="  %Y-%m-%d %H:%M"
                        ),
               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               # widget.Systray(
                        #background=colors[0],
                        #icon_size=20,
                        #padding = 4
                        #),
              ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, opacity=0.8)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, opacity=0.8))]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

#
# assign apps to groups/workspace
#
@hook.subscribe.client_new
def assign_app_group(client):
    d = {}

    # assign deez apps
    d[group_names[0][0]] = ['Alacritty', 'xfce4-terminal', 'kitty', 'Navigator', 'brave-browser', 'midori', 'qutebrowser']
    d[group_names[1][0]] = ['code', 'geany']
    d[group_names[2][0]] = ['pcmanfm', 'thunar']
    d[group_names[3][0]] = ['org.remmina.Remmina', 'Microsoft Teams - Preview']
    d[group_names[4][0]] = ['vlc', 'obs', 'mpv', 'mplayer', 'lxmusic', 'darktable', 'ART']
    d[group_names[5][0]] = ['cantata']
    d[group_names[6][0]] = ['lxappearance', 'gpartedbin', 'lxtask', 'lxrandr', 'arandr', 'pavucontrol', 'xfce4-settings-manager']
    d[group_names[7][0]] = ['virt-manager']
    d[group_names[8][0]] = ['Ultimaker-Cura', 'superslicer']
    d[group_names[9][0]] = ['thunderbird', 'TelegramDesktop', 'discord']

    wm_class = client.window.get_wm_class()[0]
    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            client.togroup(group)
            client.group.cmd_toscreen(toggle=False)




main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='archlinux-logout'),
    Match(wm_class='xfce4-terminal'),
    Match(wm_class='Protonvpn'),
    Match(wm_class='proton-bridge'),
    Match(wm_class='Msgcompose'),

],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"
