


label start:


    $ anticheat = persistent.anticheat


    $ chapter = 0


    $ _dismiss_pause = config.developer


    $ sim_name = "???"
    #$ s_name = "???"
    #$ m_name = "???"
    #$ n_name = "???"
    #$ y_name = "???"

    $ quick_menu = True
    $ style.say_dialogue = style.normal
    $ in_sayori_kill = None
    $ allow_skipping = True
    $ config.allow_skipping = True

    scene black
    if(persistent.playername == "Jojo"):
        stop music
        $ renpy.call_screen("dialog", "You expect Jojo to be your first kiss.\nBUT IT WAS ME, DIO!", ok_action=Return())
        $ persistent.playername = player = "Dio"

    call mod_boot from _call_mod_boot
    #call s_FirstBoss
    #jump FUCKINGRAW
    #call TestSurvive
    #call TestBattle
    return

label endgame(pause_length=4.0):
    $ quick_menu = False
    stop music fadeout 2.0
    scene black
    show end
    with dissolve_scene_full
    pause pause_length
    $ quick_menu = True
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
