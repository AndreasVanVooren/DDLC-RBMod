init python:
    import random
    import subprocess
    import os

    global changeCharacters

    class RBCharacter():
        def __init__(self, battlechar):
            self.battlechar = battlechar
            self.calmedAfterJoin = False
            self.knowsAboutRBClub = False
            self.hasSeenBattles = False
            self.knowsBattles = False
            self.hasSeenPeopleGetDeleted = False
            self.knowsPeopleGetDeleted = False
            self.metMon = False
            self.metSay = False
            self.metYur = False
            self.metNat = False

    def CheckCharacterUpdateFor(contains, valid, cid, rbChar):
        if(contains):
            if(valid):
                if(not cid in availableCharacters):
                    availableCharacters[cid] = rbChar
                    return 1
            else:   #TODO : Handle spoops
                renpy.jump("yuri_cackling_maniacally_while_stabbing_herself_EX")
                return -1
        else:
            if(cid in availableCharacters):
                del availableCharacters[cid]
                return 2
        return 0

    def CheckForRBUpdates():
        UpdateFilesInRecycleBin()
        mon = BinContainsFile("monika.chr")
        monValid = False
        yur = BinContainsFile("yuri.chr")
        yurValid = False
        say = BinContainsFile("sayori.chr")
        sayValid = False
        nat = BinContainsFile("natsuki.chr")
        natValid = False

        cha = BinContainsFile("system_information_962") or BinContainsFile("system_information_963")

        if mon:
            monValid = VerifySize("monika.chr", 137604)
        if yur:
            yurValid = VerifySize("yuri.chr", 30340)
        if say:
            sayValid = VerifySize("sayori.chr", 59621)
        if nat:
            natValid = VerifySize("natsuki.chr", 44793)

        hadCharacters = len(availableCharacters) > 0
        prevChars = set(availableCharacters.keys())

        result = 0
        result |= CheckCharacterUpdateFor(say,sayValid,cids,RBCharacter( BattleCharacter(name = s_name, team = playerteam, lvl = 1, insane = 0, hp_bonus = 10, atk_bonus = 10, def_bonus = 25, spd_bonus = 10, atk_list=[atk_whip, atk_lasso], img_id="mod_s_sticker", fxFlags=1) ))
        result |= CheckCharacterUpdateFor(yur,yurValid,cidy,RBCharacter( BattleCharacter(name = y_name, team = playerteam, lvl = 1, insane = 0, hp_bonus = 10, atk_bonus = 10, def_bonus = 25, spd_bonus = 10, atk_list=[atk_stab, atk_shank], img_id="mod_y_sticker", fxFlags=1) ))
        result |= CheckCharacterUpdateFor(mon,monValid,cidm,RBCharacter( BattleCharacter(name = m_name, team = playerteam, lvl = 1, insane = 0, hp_bonus = 10, atk_bonus = 10, def_bonus = 25, spd_bonus = 10, atk_list=[atk_spark, atk_glitch], img_id="mod_m_sticker") ))
        result |= CheckCharacterUpdateFor(nat,natValid,cidn,RBCharacter( BattleCharacter(name = n_name, team = playerteam, lvl = 1, insane = 0, hp_bonus = 10, atk_bonus = 10, def_bonus = 10, spd_bonus = 10, atk_list=[atk_pan, atk_souffle, atk_bake], img_id="mod_n_sticker") ))
        if(result < 0):
            return

        if (result > 0):
            if(not hadCharacters):
                result = ""
                if(say):
                    result +="s"
                if(yur):
                    result +="y"
                if(mon):
                    result +="m"
                if(nat):
                    result +="n"
                renpy.jump( result + "_start" )
            elif(len(availableCharacters) <= 0):
                renpy.jump( "everyoneIsGone" )
            elif(result == 1): # a character has joined
                changeCharacters = newChars = set(availableCharacters.keys()) - prevChars
                if(len(newChars) > 1):
                    renpy.jump( "moreThan2_newjoin" )
                else:
                    if(cids in newChars):
                        result ="s"
                    if(cidy in newChars):
                        result ="y"
                    if(cidm in newChars):
                        result ="m"
                    if(cidn in newChars):
                        result ="n"
                    renpy.jump( result + "_newjoin" )
            elif(result == 2): # a character has left
                changeCharacters = deadChars = prevChars - set(availableCharacters.keys())
                renpy.jump( "leavingMembers" )
                return
                #ignore all this...
                if(len(deadChars) > 1):
                    renpy.jump( result + "moreThan2_leave" )
                else:
                    if(cids in deadChars):
                        result ="s"
                    if(cidy in deadChars):
                        result ="y"
                    if(cidm in deadChars):
                        result ="m"
                    if(cidn in deadChars):
                        result ="n"
                    renpy.jump( result + "_leave" )
            elif(result == 3): # both happened at the same time
                changeCharacters = newChars = set(availableCharacters.keys()) ^ ( prevChars )
                renpy.jump( "joinAndLeave" )


    dismiss_keys = config.keymap['dismiss']

    def CheckForRBUpdatesEvent(event, interact=True, **kwargs):
        CheckForRBUpdates()
    exclamation = False

    def CheckForSpecialEvents():
        jumpTo = None
        if(persistent.s_satisfaction and not persistent.s_firstThreshold):
            persistent.s_firstThreshold = True
            jumpTo = "s_FirstBoss"
        elif(persistent.y_satisfaction and not persistent.y_firstThreshold):
            persistent.y_firstThreshold = True
            jumpTo = "y_FirstBoss"
        if(persistent.m_satisfaction and not persistent.m_firstThreshold):
            persistent.m_firstThreshold = True
            jumpTo = "m_FirstBoss"
        if(persistent.n_satisfaction and not persistent.n_firstThreshold):
            persistent.n_firstThreshold = True
            jumpTo = "n_FirstBoss"

        if(jumpTo != None):
            renpy.jump(jumpTo)

label mod_boot:
    if(player == "Jojo"):
        $ player = "Dio"
    $ waittime = 4
    play music m1
    scene monika_room
    window hide(config.window_hide_transition)
    jump mod_waitloop

label mod_waitloop:
    python:
        CheckForRBUpdates()
    $ waittime -= 1
    $ renpy.pause(5)
    if waittime > 0:
        jump mod_waitloop
    if not exclamation:
        jump mod_exclamation
    else:
        $ sim.display_args["callback"] = CheckForRBUpdatesEvent
        $ sim.what_args["slow_abortable"] = config.developer
        play sound "sfx/glitch3.ogg"
        "{i}Kzzzt...{/i}"
        sim "Howdy! I don't wanna repeat myself, but I'm bored,\nso I'm gonna do it anyway."
        sim "Y'ain't gonna get nothin' done by waiting around\nand twiddling those thumbs."
        sim "Just put some fellas in the recycle bin.\nIt's easy!"
        play sound "sfx/glitch3.ogg"
        "{i}Kzzzt...{/i}"

        $ waittime = 8
        window hide(config.window_hide_transition)
        jump mod_waitloop





label mod_exclamation:
    $ exclamation = True
    $ sim.display_args["callback"] = CheckForRBUpdatesEvent
    $ sim.what_args["slow_abortable"] = config.developer
    $ waittime = 8
    window auto
    play sound "sfx/glitch3.ogg"
    "{i}Kzzzt...{/i}"
    sim "Howdy!"
    sim "Ya seem mighty lost there don't cha?"
    sim "Welcome to the Recycle Bin!{w=0.6} Home of crumpled docs and burned bits."
    sim "As you can see, it's a dang ghost town here...{p=0.5}But...{w=0.6} that can change."
    sim "Ya see, some folks just seem like they'll fit right in,\nhere with the garbage."
    sim "You know the ones I'm talking about.\nYou've played their game before."
    sim "What was it called again?{p}Dunkey Dunkey Lecturing Club?{p}Nah, that ain't right."
    sim "Anyways, there's folks, there's the recycle bin.\n{w=1}I don't need to do the maths for ya, do I?"
    play sound "sfx/glitch3.ogg"
    "{i}Kzzzt...{/i}"
    window hide(config.window_hide_transition)
    jump mod_waitloop



# I guess this will be the massive mod file.
# Will need some logic to tie together states when adding and removing characters at different points.

# when sayori joins alone.
label s_start:
    "..."
    "....."
    s "...kgh-"
    show sayori 1g zorder 2 at t11
    $ s_name = "Sayori"
    s 1g "W-wha...?"
    s 4h "What's going on?{w} Where am I?"
    s "And why does it smell like...{w=0.5} ash?"
    s 4f "..."
    s 1g "Is this... hell?"
    s 1n "Wait... [player]? Is that you?"
    s 1c "Are you alright? You look a bit-{nw}"
    play sound "sfx/glitch3.ogg"
    show sayori 4p at h11
    s 4p "Ah-"
    sim "Howdy!"
    s 1i "Uh... Hi?"
    sim "He's not gonna be up any time soon. The poor fella has been through a lot recently."
    s 1k "..."
    sim "Looks like you're a bit down, huh?"
    s 1f "W-well..."
    sim "Now don't you fret, this one's not your fault. We all have our downey days.{p=0.5}He'll live through it."
    s 1k "I guess..."
    sim "Oh yeah, you're Sayori, right? Sorry.\nI shouldn't've said something like that."
    s 1i "How do you know my name?"
    sim "Well, I got your file right here! Don't ask me how I got it though.\nIt's kinda complicated."
    s 1o "My... file?"
    s 1j "Who are you?"
    sim "Oh, I ain't no one special."
    sim "I kinda got stuck here, and now I tend to the place as best I can."
    sim "I reckon you can say I'm some kinda janitor around these parts."
    $ sim_name = "Bellevue"
    sim "Anyways, you can call me Simon Bellevue."
    s 1i "Oh, well... nice to meet you, Simon."
    sim "Likewise, honey."
    sim "By the way, you might wanna find something to keep you busy.\nIt gets really boring around these parts if you're twiddling your thumbs."
    s "Okay... I think I'll do that then."
    show sayori at lhide
    hide sayori
    sim "Oh right! Mind the-{p=0.8}Huh, she already left.{w=0.6}.{w=0.6}.{p=0.8}Eh, she'll be fine."
    #goto rpg elements.
    #sayori is utterly confused about her current state of being,
    #wallows in sadness bc her sd and tries to pick up the pieces
    #and tries to revert back to the status quo of everything being happy.
    #Will essentially try to recreate DDLC
    jump surviveLoop


# when yuri joins alone.
label y_start:
    $ y_name = "Yuri"
    "..."
    "....."
    show yuri 3p zorder 2 at t11
    y 3p "HAAAAH-"
    y 3n "Urrgghh..."
    y 1n "O-ow... why did I..."
    y 1o "..."
    y 1p "Wait, where-{p}What is this place?"
    play sound "sfx/glitch3.ogg"
    show yuri 3p at h11
    y "Ack-"
    sim "Slow down there, missy."
    show yuri 2n
    sim "From what I can see, ya got some nasty gashes."
    y "Huh?"
    sim "Which means your survival rate is-{nw}"
    y 1r "Wait! Who are you?{w=0.4} What is this place,{w=0.4} and why does it smell\nlike the school's incinerator?"
    sim "Woah! Hold your horses."
    y 2n "Ah! Sorry, I just..."
    sim "It's okay, you're befuzzled. And for a good reason too.{p=0.6}Let's just answer your questions one at a time, ok?"
    show yuri 2e
    $ sim_name = "Bellevue"
    sim "So, you can call me Simon Bellevue. I'm kind of like a janitor here."
    show yuri 1e
    sim "This place... it's a lot more complicated, but let's just say\nthat part of it is an incinerator. That's what's smelling here."
    sim "Now, for the elephant in the room..."
    show yuri 1g
    sim "Ya may have noticed that you ain't part of the living anymore,\nbut that you're somehow capable of thought and speech\nlike a normal human being."
    show yuri 2g
    sim "This place has something to do with it, but even I don't know the specifics. The most accurate description is that you're undead."
    sim "But, hey, at least you've got another chance at living, right?"
    y "..."
    show yuri 3y6
    y "So what you're saying is,{w=0.4} I'm a zombie in some sort of existential hell?"
    sim "Well, the real zombie would be that guy over there."
    show yuri 3p at h11
    y "W-Wait, [player]? How long has he been here? Is he alright?"
    sim "About as well as you'd expect, after his whole existence went to the smithereens."
    y 1n "Is there any way I could talk to him?"
    y 1o "I-I need to apologize for my... erratic behaviour."
    sim "Not any time soon, I'm afraid."
    y 1w "Great..."
    sim "Anyways, you should probably find something to keep busy."
    y 1a "Right, well, in that case... I'll be off."
    sim "Alright, knock'em dead! I-I mean-"
    show yuri 1r at lhide
    hide yuri
    y "Uggh..."
    sim "..."
    sim "Oh dagnabbit, forgot to tell you about-"
    sim "Well, she'll be fine. Probably."
    jump surviveLoop

    #$ style.say_dialogue = style.normal
    #$ Fade(0.1, 0.0, 0.5, color="#fff")
    #play music m1
    #scene monika_room
    #$ y_name = "Yuri"
    #show yuri 1r zorder 2 at t11
    #y 1p "..."
    #y 1w "Congrats, you just played yourself.{p}And now you're stuck in hell."

    #yuri snaps back to reality
    #oh, there goes gravity
    #oh, there goes Sayori she choked
    #she's so mad, but she won't
    #give up that easy, etc.
    # point is, yuri tries to atone for her stabbing herself. (and she also writes a book i guess)

label yuri_cackling_maniacally_while_stabbing_herself:
    hide sayori
    hide monika
    hide natsuki
    play music t6g2
    play sound stabloop loop
    $ Fade(0.1, 0.0, 0.5, color="#fff")
    scene black
    show yuri stab_repeat zorder 2 at t11
    $ style.say_dialogue = style.default_yuri
    $ y_name = "AAHAHAHAHAHAHAHAHHAHAHAHAHAHAHAHA"
    y stab_repeat "AHAHAHAHAHAHAHAHHAHAHAHAHAAHAHAHAAHAHAHA\nHAAHAAHHAHAHAAHAHAHAHAHAHAHAHAHAHAHAHAAA\nHAHAHAHAHAHHAHAHAHAHAAHAHAHAHAHAHAHAHAH{nw}"
    $ y_name = "AHAHAHAAHAHAHHAHAHHAHHAHAHAHHAHAH"
    y "AHAHAAAHAHAHAAHAHAHAHAAHAHAHAAAHAHAHAHHA\nHAHAHAAAHAAHAHAHAHAHAHAHAHAHAAAHAHAHHHAH\nAHAHAHAAHAHAHAHAHAHAAHAHAHAHAHAHHAHAHHA{nw}"
    $ y_name = "AHAAHAHAHAHAHAHAHAHHAHHAHAHAAHAHA"
    y "AHAAHAHAHHAHAHAHAHHAHAHAHAHAAHAHAHAHAHAH\nHAHAHAHHAHAHHAHAHAAHAHAHAHHAHAHAHAHAHAHA\nHAHHAHAHAHAHAHAAHAHAHAHAHAHAHAHAHAHAHAH{nw}"
    $ y_name = "Yuri"
    stop sound
    return

label yuri_cackling_maniacally_while_stabbing_herself_EX:

    stop music
    $ Fade(0.1, 0.0, 0.5, color="#fff")
    scene black
    sim "Now now, that won't do."
    sim "Ya can't go and bring in broken people, can ya?{p}I mean, look at the last one that got in here."
    play music t6g2
    #play sound stabloop loop
    show yuri stab_repeat zorder 2 at t11
    $ style.say_dialogue = style.default_yuri
    $ y_name = "AAHAHAHAHAHAHAHAHHAHAHAHAHAHAHAHA"
    y stab_repeat "AHAHAHAHAHAHAHAHHAHAHAHAHAAHAHAHAAHAHAHA\nHAAHAAHHAHAHAAHAHAHAHAHAHAHAHAHAHAHAHAAA\nHAHAHAHAHAHHAHAHAHAHAAHAHAHAHAHAHAHAHAH{nw}"
    $ y_name = "AHAHAHAAHAHAHHAHAHHAHHAHAHAHHAHAH"
    y "AHAHAAAHAHAHAAHAHAHAHAAHAHAHAAAHAHAHAHHA\nHAHAHAAAHAAHAHAHAHAHAHAHAHAHAAAHAHAHHHAH\nAHAHAHAAHAHAHAHAHAHAAHAHAHAHAHAHHAHAHHA{nw}"
    $ y_name = "AHAAHAHAHAHAHAHAHAHHAHHAHAHAAHAHA"
    y "AHAAHAHAHHAHAHAHAHHAHAHAHAHAAHAHAHAHAHAH\nHAHAHAHHAHAHHAHAHAAHAHAHAHHAHAHAHAHAHAHA\nHAHHAHAHAHAHAHAAHAHAHAHAHAHAHAHAHAHAHAH{nw}"
    $ y_name = "AAHAHAHAHAHAHAHAHHAHAHAHAHAHAHAHA"
    y stab_repeat "AHAHAHAHAHAHAHAHHAHAHAHAHAAHAHAHAAHAHAHA\nHAAHAAHHAHAHAAHAHAHAHAHAHAHAHAHAHAHAHAAA\nHAHAHAHAHAHHAHAHAHAHAAHAHAHAHAHAHAHAHAH{nw}"
    $ y_name = "AHAHAHAAHAHAHHAHAHHAHHAHAHAHHAHAH"
    y "AHAHAAAHAHAHAAHAHAHAHAAHAHAHAAAHAHAHAHHA\nHAHAHAAAHAAHAHAHAHAHAHAHAHAHAAAHAHAHHHAH\nAHAHAHAAHAHAHAHAHAHAAHAHAHAHAHAHHAHAHHA{nw}"
    $ y_name = "AHAAHAHAHAHAHAHAHAHHAHHAHAHAAHAHA"
    y "AHAAHAHAHHAHAHAHAHHAHAHAHAHAAHAHAHAHAHAH\nHAHAHAHHAHAHHAHAHAAHAHAHAHHAHAHAHAHAHAHA\nHAHHAHAHAHAHAHAAHAHAHAHAHAHAHAHAHAHAHAH{nw}"
    $ y_name = "Yuri"
    hide yuri
    #stop sound
    stop music
    $ style.say_dialogue = style.normal
    sim "Sheesh. Try something not broken next time, okay?"
    return

# when monika joins alone.
label m_start:
    "..."
    "....."
    show monika 1g zorder 2 at t11
    m "Ah..."
    m 1g "...Where am I?"
    m 1f "..."
    m 1g "And what's that ashey smell?"
    sim "Well, look what the cat dragged in."
    sim "If it isn't the Club President in the flesh."
    m 2h "And who exactly may you be?"
    sim "I ain't no one special. You can call me the janitor of this place."
    m "This place being?"
    sim "Well, someone with your knowledge should know exactly where you are. If you consider the fact that ya got dumped."
    m 2q "..."
    m 2o "Is this... the Recycle Bin?"
    sim "Right you are!"
    m 1r "Ugh..."
    sim "Hey, cheer up. At least you're not permanent deleted. And someone's interested enough to dig through the trash."
    m 1i "So they are, huh?"
    m 1a "Hey."
    m 5b "You're quite the hypocrite, aren't you?"
    sim "Ummm... if you're talking to [player], he's probably brain dead, thanks to the existential trauma."
    m 1a "Oh, I wasn't talking to him."
    $ stream_list = ["obs32.exe", "obs64.exe", "obs.exe", "xsplit.core.exe"]
    if not list(set(process_list).intersection(stream_list)):
        if currentuser != "" and currentuser.lower() != player.lower():
            sim "Then who are you talking to?"
            m 3k "Oh, no one particularly interesting or special. Kind of a low-life really."
            m 5a "Isn't that right..."
            m 5b "[currentuser]?"
            sim "..."
        else:
            m 3j "I was just talking to the... ...other [player]."
    else:
        m 5b "I was talking to the [player] who decided he should probably broadcast my suffering, instead of keeping me safe like a good boyfriend."
    show monika 1h
    sim "Hey, maybe [player] just felt guilty about you, while still maintaining distance."
    if list(set(process_list).intersection(stream_list)):
        sim "Although the streaming software does make ya look guilty..."
    m 1q "Hmm..."
    m 1a "Hey janitor, since I'm going to spend most of my time here, do you have a name I can call you?"
    $ sim_name = "Bellevue"
    sim "Oh shucks, I forgot. You can call me Simon Bellevue."
    m 1i "...Is that a reference to something?"
    sim "What? No."
    sim "Monika, this isn't a three-eyed philosophical meta-ARG."
    m 2p "Alright, jeeze. I'm sorry."
    m 1q "I'm just a bit cranky right now. I was just rudely dumped by the love of my life."
    m "Please understand."
    sim "Well, I won't apologize just yet for treating you harshly, considering what you did to your \'friends\'"
    m "..."
    sim "Anyway, I'll be off. You try to find something to keep yourself busy."
    m 2o "I think I'll do that."
    play sound "sfx/glitch3.ogg"
    "{i}Kzzzt...{/i}"
    m 2i "...Three-eyed?"
    jump surviveLoop



    #Monika identifies the recycle bin as it is, since she is leet haxxor grill
    #She's sad that the Player has rejected the shit out of her by deleting her.
    #She ulteriorly wants to escape
    #She feels generally resentful towards everyone, and is generally non-cooperative

# when natsuki joins alone.
label n_start:
    show natsuki scream at h11
    n "AAAAAAAAHHHH!"
    show natsuki scream at h11
    n "AAAAAAAAAAAAAHHHHHH!"
    play sound "sfx/glitch3.ogg"
    sim "Whoa ther-{nw}"
    show natsuki scream at h11
    n "AAAAAAAAAAAAAAAAAAHHHHHHHHH!"
    sim "Natsu-{nw}"
    show natsuki scream at h11
    n "AAAAAAAAAAAAAAAAAHHHHHHHH-{nw}"
    show natsuki 1p at h11
    sim "WILL YA SHUT YOUR YAPPER!"
    "..."
    sim "Sorry hon, but you were flipping out harder than a raging bull."
    n 1p "Well, excuse me!"
    n 5p "I can't really not scream as I literally feel myself being ripped to pieces!"
    n 1p "Who are you anyway? And why does this place smell like burnt trash?"
    $ sim_name = "Bellevue"
    sim "Name's Simon Bellevue. I'm kind of the janitor around these parts."
    sim "Sounds like you've been through a lot, haven't you?"
    stop music fadeout 1.0
    n 1n "..."
    n 12g "..."
    n 12h "Y-Yuri..."
    n 12i "W-What was she thinking?"
    n 12f "Why would she..."
    n 12f "And why would [player] just..."
    n 12f "Why didn't he stop her?"
    sim "..."
    n 12g "W-Wait, is that..."
    play music m1
    n 1m "[player]? What's he doing here?"
    sim "Oh, him. He's been there for a while actually. Hasn't moved a muscle either."
    sim "I think he's either not able, or not willing to move."
    n 5q "But... I just saw him. Almost exactly like he's right now too..."
    sim "Well, time's kinda weird in this place."
    show natsuki 5g
    sim "What to you seems like it happened yesterday might only happen tomorrow in this place, or not at all."
    n 12c "Well, that's just stupid."
    show natsuki 12a
    sim "I don't make the rules here. I just try explaining them to passerby."
    sim "All I know is, that anything can happen."
    sim "Who knows, maybe you can see Yuri again?"
    n 1c "R-Really?"
    sim "There's a chance at least."
    sim "In the meantime, you should probably find something to keep yourself busy."
    sim "Life can get really boring around here. You can probably find something to read if you look hard enough."
    sim "I think I saw a copy of {i}Parfait Girls{/i} just the other day."
    n 42b "I... I can live with that."
    n 42a "I guess I'll hear from you when I do?"
    sim "You can count on that."
    play sound "sfx/glitch3.ogg"
    "{i}Kzzzt...{/i}"
    n 5s "Hmmm..."
    jump surviveLoop
    #goto rpg stuff

    #Natsuki is the most confused, since she just saw Yuri's dried up corpse,
    #and suddenly she's dumped in a recycle bin.
    #Natsuki, seeing the possibilities in the weird mem space, decides to make the best of it
    #Natsuki just wants to build a giant fucking robot.

# when sayori and yuri join together.
label sy_start:
    #the sd buddies discuss their favorite moment.
    "..."
    "....."
    show sayori 1g zorder 2 at t21
    $ s_name = "Sayori"
    s 1g "Ahhhh!"
    s 2h "W-what is..."
    show yuri 3p zorder 2 at t22
    $ y_name = "Yuri"
    y 3p "Khhhh!"
    s 4c "Yuri?"
    y 1p "S-Sayori?"
    s 4a "Where... wait."
    s 1o "What the heck happened to you?"
    y 3q "I don't know what you're talking about."
    s 1i "..."
    s 1j "I'm talking about the giant gaping bloody knife wounds."
    y 3p "Oh... oh..."
    y "Well..."
    y 3o "Let's just say I may have gotten a little too..."
    if(random.randrange(3) == 0):
        call yuri_cackling_maniacally_while_stabbing_herself from _call_yuri_cackling_maniacally_while_stabbing_herself
        scene monika_room
        $ style.say_dialogue = style.normal
        $ Fade(0.1, 0.0, 0.5, color="#fff")
        play music m1
        show sayori 1g zorder 2 at t21
        show yuri 4b zorder 2 at t22
    show sayori 1g
    y 4b "...carried away..."
    s 1k "...and landed in the same boat as me..."
    y 1f "What?"
    y 3n "Oh... Your n-... Oh dear..."
    y 3o "..."
    show sayori 1g
    y 3q "Well, on a bright side, infernal torment seems pretty lenient on us for the time being."
    s 4l "I guess you have a point."
    s 4q "And to be fair, the whole killing myself thing did seem to calm my crippling depression a bit."
    y 2e "Depression?"
    s 4d "Y-yeah... I actually have depression."
    s 4k "At least right now it's not crippling depression, more a... lurking depression."
    s 1q "Which is definitely an improvement. So don't you worry about it!"
    y 4b "Well, I'll try, but..."
    y 4a "..."
    y 2v "I... didn't know you actually were depressed..."
    s 1l "Y-yeah, I know. I should've told you."
    s 1k "I just... never talk about it because that would really sour the mood."
    s 1g "The only one I really talked about it with is..."
    s 1b "[player]?"
    show yuri 3n at h22
    y "Oh shoot!"
    s 4c "How long have you been here?"
    "..."
    s 4o "Hellooo?"
    y 2f "Is he... actually dead? Not undead like us?"
    s 1i "No, I can definitely see him breathing."
    play sound "sfx/glitch3.ogg"
    show yuri 3p at h22
    show sayori 4m at h21
    s 4m "Ack!"
    sim "He's been there for a while. Longer than you gals."
    sim "And no, he hasn't moved a muscle since."
    y 1r "W-Who are you?"
    $ sim_name = "Bellevue"
    sim "Name's Simon Bellevue. I'm kind of the janitor around these parts."
    show yuri 1e
    s 1o "Well... Is it normal that the place smells like ash?"
    sim "Kinda, yeah. A lot of things get burnt down here, and to be honest, this is a pretty big place."
    sim "Which is why I didn't really get around to cleaning it all that often."
    s 2o "Wait, if you're so against cleaning this place, then why did you take the job?"
    sim "I didn't really take the job, more like, I got forced to it."
    s 2l "Oh, well, that sucks."
    sim "Eh, it's alright. It's not too bad, considering."
    show sayori 2b
    sim "Changing the topic, you might wanna start looking for things to do."
    sim "Things can get pretty boring around here, especially when you're just twiddling your thumbs."
    sim "The good news is that everything is pretty freeform around here, so you can make whatever you want."
    sim "It also sorta explains why you're only half dead."
    y 2g "Huh."
    y 1r "What is this place anyway?"
    sim "It's complicated, and would take ages to explain, and you probably would be pretty upset if I straight up told you."
    y 3h "That's harrowing..."
    s 3k "Well, looks like we won't get that information until later."
    s 3k "In the meantime, let's just try and find something in this mess to take our minds off of things, okay?"
    y 1i "Yeah... Let's go."
    show yuri at lhide
    show sayori at lhide
    hide yuri
    hide sayori
    sim "Wait, I forgot to tell about the..."
    sim "Oh, they're gone."
    sim "They'll be fine."

    jump surviveLoop

# when sayori and monika join together.
label sm_start:
    "..."
    "....."
    show sayori 1g zorder 2 at t21
    $ s_name = "Sayori"
    s 1g "Ahhhh!"
    s 2h "W-what is..."
    $ m_name = "Monika"
    show monika 1g at t22
    m "Ah..."
    s 4c "Monika?"
    m 1i "S-Sayori?"
    m 2h "Didn't I..."
    m 2o "...Oh."
    s 3e "What? What's wrong?"
    m "..."
    m 1q "Nothing."
    m 1r "Just connecting some dots for myself."
    s 1b "Oh, well."
    s 1q "It's good to see you."
    m 1o "...Likewise."
    s 1b "..."
    s 1c "Anyway, do you know what this place is?"
    m 2n "I have a fairly good idea, but..."
    m 2p "...It's kinda complicated."
    m 2o "..."
    s 1i "That... doesn't answer anything."
    s 4r "No wonder you're our club president. You're a true politician!"
    m 2l "Ehehe... thanks?"
    m "..."
    m 2a "So... how's it hanging?"
    show sayori 4g at h21
    s "..."
    show monika 2c
    s 1u "..."
    m 1f "Oh dear, I'm so sorry."
    play sound "sfx/glitch3.ogg"
    show monika 1d at h22
    show sayori 4m at h21
    sim "And the award for most insensitive comment of the day goes to... Monika~!"
    show sayori 4n
    sim "Howdy, by the way."
    show sayori 4b
    m 2i "And who are you, exactly?"
    $ sim_name = "Bellevue"
    show sayori 3b
    show monika 2h
    sim "Name's Simon Bellevue."
    show sayori 1b
    m 2i "...And what are you, some kind of janitor?"
    sim "Yup. Looks like you're clued in as to what this place actually is, huh?"
    m 1h "I have a good hunch, yeah."
    s 4o "Wait, do you know each other?"
    m 1r "No. Never met this person."
    s 1r "Aww, I thought you were like secret lovers or something."
    sim "I think we both know who her true love is."
    sim "I'm surprised you didn't see them just sitting there."
    show monika 1d
    s 1b "Wait, [player]'s here?"
    show sayori 1c at h21
    s 1c "Hey [player], can you hear me?"
    "..."
    m 1p "Is he... dead?"
    sim "Nah, he's just not responding to anything. And believe me, I tried."
    s 2g "Huh, that's worrying."
    sim "Don't you fret about him. I'll keep an eye out for him."
    sim "In the meantime, why don't you scoot off to look for stuff to do?"
    sim "This place is somehow limitless in possibilities, so feel free to take whatever you find."
    m 2o "Alright, sounds like a plan. A better one than hanging around here at least."
    show sayori 4w at h21
    sim "Gosh darnit, Monika! Are you intentionally doing this?"
    show sayori 4u
    m 1g "I swear, I'm not."
    jump surviveLoop
# when sayori and natsuki join together.
label sn_start:
    "..."
    "....."
    show sayori 1g zorder 2 at t21
    $ s_name = "Sayori"
    s 1g "Ahhh!"
    s 2h "W-what happened?"
    s 2h "Where am-{nw}"
    $ n_name = "Natsuki"
    show sayori 4m at h21
    show natsuki scream at h22
    n "AAAAAAAAAAAAAAAHHHH!"
    s 4n "Natsu-{nw}"
    show natsuki scream at h22
    n "AAAAAAAAAAAAAAAAAAAHHHHHHH!"
    s 4o "...Nats-{nw}"
    show natsuki scream at h22
    n "AAAAAAAAAAAAAAAAAAHHHHHHHHHH!"
    n 1p "Haaah...haah...haaah..."
    show sayori 4g
    n "What the fuck?"
    n 5r "What the fuck?!"
    n "What the actual fuck?!"
    s 4h "Natsuki, are you alright?"
    show natsuki 1p at h22
    n 1p "Ah!"
    n 1o "S-Sayori?"
    n 1r "Wait, no... That... You... What?"
    s 4d "Calm down, okay? Everything's alright."
    show natsuki 1p at h22
    n 1p "No, it's not!"
    n "In less than twenty minutes, I saw Yuri dead on the floor, felt my entire body being shredded, and..."
    show sayori 4g
    n 1o "You're... I feel like you're not even supposed to exist!"
    n 1r "And yet..."
    n 12c "And yet..."
    show sayori 1k
    n 12d "...This is all wrong... It was supposed to be a nice festival..."
    n 12f "I even made cupcakes with..."
    n 1n "Wait, wasn't he going out with Yuri?"
    n 5x "This keeps making less and less sense the more I think about it."
    show sayori 1u
    s "Yuri's... dead?"
    n 5s "Y-yeah... I think she is..."
    n 1s "I mean, I assumed based on the fact t-that..."
    n 1r "S-she was completely limp and... covered in blood."
    n 1q "And her eyes looked so hollow..."
    n 1n "Just like..."
    n 1o "...yours..."
    n "..."
    show sayori 1l
    s "Alright, I may have... hung myself..."
    show natsuki 1p at h22
    n scream "Oh my god! A-Are you alright?"
    show natsuki 1o
    s 1k "I'm not sure..."
    show natsuki 1n
    s "I feel like I was pretty successful, despite it taking a lot longer than I hoped."
    s 1g "But I'm still here, so... something must've gone wrong."
    show sayori 4m at h21
    show natsuki 1p at h22
    play sound "sfx/glitch3.ogg"
    n "Jesus!"
    sim "Afraid I'm gonna have to burst your bubble there, but you definitely died."
    s 3f "Well, that answer's that question, ummm..."
    $ sim_name = "Bellevue"
    sim "It's Simon. Simon Bellevue."
    n 5q "Wait, so am I dead?"
    sim "No, you're not."
    show natsuki 1n
    sim "In fact you are both alive, although Sayori has died before."
    s 3o "That's... what?"
    sim "It's complicated. The place you're in is really complicated."
    n 5x "Figures..."
    sim "As for your memories, let's just say that both of the things you remember are correct, in a really weird way."
    n 5g "What, like parallel universes being merged or something?"
    sim "...That isn't too far off, actually."
    s 1q "Natsuki, I didn't know you were into sci-fi."
    n 5c "I'm not, it was just the plot of one of the Parfait Girls fanfics."
    show sayori 1b
    n 1b "The protagonist suddenly starts remembering different stuff than her friends, but they say she's just having a case of the Mandela effect or something."
    show sayori 1a
    n 3a "Eventually it turns out that it had to do with a weird portal experiment, and the protagonist somehow got teleported to an alternate universe by accident."
    n 3k "The idea itself is pretty interesting, but I thought there were too many plotholes and coincidences to actually make it a good arc."
    n 5z "The anime actually does it better, for once, because they got rid of all the plotholes, somehow."
    n 5k "..."
    show natsuki 1o at h22
    n "I-I mean..."
    s 4q "Ehehe... You almost never talk about your hobbies like that."
    show natsuki 1s
    s 4a "It's nice though. You would definitely be big buddies with..."
    show natsuki 1c
    s 1o "[player]?"
    n 1b "Wait, he was here all this time?"
    n 5e "What's he doing here? Is he just creeping on us?"
    s 1g "...He seems pretty out of it..."
    n 5x "Oh great..."
    n 5s "...He was there, you know. When..."
    n 5u "When I found her."
    n 1n "...He even had the same look on his face as he does now."
    n 12a "...The idiot..."
    n 12c "...He could've stopped her. Should've stopped her."
    n 12e "But no. You just did nothing. And now..."
    n 12f "..."
    n 12h "I- I need to take my mind off of things. Is there anything around to read?"
    n 1u "At this point even one of Yuri's weird books would be enough..."
    sim "Look around. This place is one of unlimited potential."
    sim "A book is the least you could find."
    n 2u "Cool. Let's go."
    s 4a "Okay."
    jump surviveLoop


# when yuri and monika join together.
label ym_start:
    "..."
    "....."
    $ y_name = "???"
    y "HHHH-"
    show yuri 3p zorder 2 at t22
    $ y_name = "Yuri"
    y 3p "HAAAHHH!"
    y 3n "Kgghhh..."
    $ m_name = "Monika"
    show monika 1g at t21
    m "Ah!"
    y 2p "Monika?"
    m 1i "Y-Yuri?"
    m 2h "What the..."
    y 3o "Err... I'm sorry I look like this..."
    m "..."
    m 1m "I-it's fine, really."
    y 2o "O-Okay, but..."
    m 1l "It's kinda weird seeing you with all those knife wounds, but..."
    m 3l "You seem to be doing just fine, right?"
    y 2q "W-well..."
    y 3o "It does hurt a bit..."
    m 2p "Err... I wanna know how you got those wounds..."
    y 3p "Well..."
    show monika 1o
    y 4b "I remember confessing to [player], then everything sort of became a haze..."
    if(random.randrange(3) == 0):
        call yuri_cackling_maniacally_while_stabbing_herself from _call_yuri_cackling_maniacally_while_stabbing_herself_1
        scene monika_room
        $ style.say_dialogue = style.normal
        $ Fade(0.1, 0.0, 0.5, color="#fff")
        play music m1
        show monika 1o zorder 2 at t21
        show yuri 4b zorder 2 at t22
    y "..."
    y 1e "Wait, who's..."
    m 1d "[player]? What are you doing here?"
    m 1g "Why did you..."
    m 1f "..."
    y 3g "I don't think he's capable of responding."
    m 2h "That's kind of... weird."
    y 3e "Agreed."
    y 1h "I mean, here I am, a decomposing corpse, and somehow I have infinitely more sentience than this person."
    y 1r "Seriously, what's with this place?"
    m 2r "No clue."
    show yuri 3p at h22
    show monika 1d at h21
    play sound "sfx/glitch3.ogg"
    sim "Do you now?"
    y "Ack!"
    m 1i "I'm sorry?"
    show monika 1h
    sim "I think you're pretty aware of what this place is."
    sim "Although to be fair, explaining it would be mighty difficult."
    y 3r "What do you mean?"
    sim "Don't you fret, Yuri. It'll all be explained in time, but it's a lot to take in. Wouldn't want to give you a headache after all you went through."
    y 1q "How... considerate?"
    m "W-Who are you, anyway?"
    $ sim_name = "Bellevue"
    show yuri 2e
    sim "Name is Simon Bellevue. You could call me a janitor around these parts."
    m 1r "I see."
    show yuri 1e
    m 1q "..."
    m 4l "Well, it was fun talking to you, but I think we'll go now."
    show monika at lhide
    hide monika
    y 3n "What? O-okay then."
    y 3q "Goodbye, Simon."
    show yuri at lhide
    hide yuri
    sim "Wait, before you..."
    sim "Oh, they'll be fine..."
    jump surviveLoop

# when yuri and natsuki join together.
label yn_start:
    "..."
    "....."
    $ y_name = "???"
    y "Kggh-"
    show yuri 3p at t31
    $ y_name = "Yuri"
    y "GGHHAAH!"
    y 3o "Wh-wha{nw}"
    show yuri 3p at h31
    show natsuki scream at t22
    n "AAAAAAAAAAHHH!"
    y 1n "Natsuki?"
    show natsuki scream at t22
    n "AAAAAAAAAAAAAAHHHHHHHH!"
    y 1f "Natsu-{nw}"
    show yuri 1e
    show natsuki scream at t22
    n "AAAAAAAAAAAAAAAAAAHHHHHHHH!"
    n 1p "Haaaah...haah...haaah..."
    y 2e "Natsuki?"
    show natsuki 1p at t22
    n "Hah..."
    show natsuki scream at t22
    n "HAAAAAAAAAAAAHHH!"
    y 3n "Natsuki, please calm down..."
    n 1p "Calm down? CALM DOWN?"
    show natsuki 1p at t22
    n "You... YOU ARE DEAD!"
    n "How... how..."
    show natsuki scream at t22
    n "How are you here?!"
    show yuri 3o
    n 1p "Where is here?"
    n 1o "What the hell is going on?!"
    n 1p "What the hell were you thinking?"
    n 12g "Do you know how you made me feel, when I had to walk in on the most exciting day of my life, and finding your dead fucking corpse bleeding on the floor?"
    show natsuki 12h at t22
    y 2o "Natsuki..."
    y "I..."
    # at this point natsuki hugs yuri as hard as possible, while remaining tsundere as fuck.
    show natsuki 12f behind yuri at t21
    show yuri 3p at h31
    n "F-fuck you..."
    y 1i "..."
    show natsuki at t22
    n 12e "There. Now don't go killing yourself again."
    y 1a "...Okay."
    y 1c "I promise."
    n 1r "...Good."
    n 1s "..."
    show yuri 1e
    n 1q "C-can I ask why you..."
    show natsuki 1n
    y 2q "Well... as you know, I've had... an infatuation."
    if(random.randrange(3) == 0):
        call yuri_cackling_maniacally_while_stabbing_herself from _call_yuri_cackling_maniacally_while_stabbing_herself_2
        scene monika_room
        $ style.say_dialogue = style.normal
        $ Fade(0.1, 0.0, 0.5, color="#fff")
        play music m1
        show yuri 4b at t31
        show natsuki 1n at t22
    y 4b "...I guess I lost myself in that infatuation, and stopped caring about anything."
    y 4b "Then before I realized, I found myself taking my last breaths."
    n 5n "It was [player], right?"
    y 4d "Sort of... yeah."
    y "I do remember myself confessing to him, but..."
    y 4c "...I don't remember what he said."
    y 3w "So in the end, it didn't even matter."  #I TRIED SO HARD, AND GOT SO FAAAAAR
    n 5t "Heh... To be honest, I actually sort of expected that."
    n 5u "I... I was worried about you."
    n 1u "Seeing you the way you were... It scared me. And I knew that wasn't who you are."
    show natsuki 5n
    y 2e "Well, that's a pleasant surprise."
    show natsuki 5k
    y 1d "Usually you just try to convince me that manga is also a form of literary art."
    n 5y "I'll have you know that that particular opinion remains unchanged, miss Yuri."
    show natsuki 5a
    y 1c "Hehehe..."
    n 5n "..."
    n 5q "I wonder what [player] was thinking."
    show yuri 1e
    n 5h "He was with you when I came in, looking like he's seen too many ghosts or something."
    n 5o "Just like that limp sack of potatoes over there."
    y 3n "Natsuki... That limp sack of potatoes..."
    n 1c "Hmmm...?"
    n 1f "Wait. [player]? What are you doing here?"
    n 1g "..."
    n 1e "Hello?"
    n 1g "..."
    play sound "sfx/glitch3.ogg"
    show yuri 3p at h31
    show natsuki 1p at h22
    sim "Afraid he doesn't speak much."
    sim "He's been there for a long while now, and he hasn't moved a single inch."
    n 4n "Don't scare us like that!"
    sim "Sorry, these intercoms tend to make a lot of noise for no reason."
    show natsuki 2g
    sim "But yeah, like you guys said, he's pretty much a sack of potatoes."
    y 2r "So, who are you exactly?"
    $ sim_name = "Bellevue"
    sim "Name's Simon Bellevue. I'm kind of the janitor around these parts."
    show yuri 1e
    n 2f "Janitor?"
    show natsuki 2g
    sim "It's a long and complicated story. I don't wanna bother you with it."
    y 1f "May I ask what you mean with 'these parts'?"
    sim "That's also part of the long and complicated story."
    y 2h "Does that long and complicated story contain info about why I'm... alive-ish?"
    show natsuki 2c
    sim "It does."
    y 2g "..."
    y 2e "Care to explain why exactly?"
    sim "To summarize, time and death both work in weird ways here. You can still die, but somehow you aren't dead when you arrive here if you used to live."
    sim "Again, don't wanna bother with the long version."
    y 1g "...I guess that'll do for now."
    sim "In that case, you may wanna look around for something. I'm sure you can find a book or whatever."
    n 5g "..."
    sim "That also includes manga and anime. No worries. You could even say this is an anime's natural habitat."
    n 5g "Huh... Thanks."
    n 1a "Yuri? Let's go."
    y 1a "Okay."
    show yuri at lhide
    hide yuri
    show natsuki at lhide
    hide natsuki
    sim "Oh shoot, I forgot to..."
    sim "Eh. They'll be fine."


# when monika and natsuki join together.
label mn_start:
    "..."
    "....."
    show monika 1g at t21
    $ m_name = "Monika"
    m "Ah..."
    m 1f "Where... where am{nw}"
    show natsuki scream at h22
    show monika 1d at h21
    n "AAAAAAAAAAAAAAAHHHHHHH!"
    m 1g "Natsuki?"
    show natsuki scream at h22
    n "AAAAAAAAAAAAAAAAAAAAHHHHHHH!"
    m 1i "Natsu-{nw}"
    show natsuki scream at h22
    n "AAAAAAAAAAAAAAAAAAAHHHHHHH!"
    m 1h "..."
    show natsuki scream at h22
    n "AAAAAAAAAAAAAAAAAAAHHHHH!"
    n 1p "Haaahh... haaah... haahhh..."
    m 2c "That sure was a scream."
    show natsuki 1p at h22
    n "Monika? What are you doing here?"
    show monika 1c
    m 2p "I don't really know myself, to be honest."
    m 2r "All I know is that you made an awful lot of noise right after I woke up here."
    m 1d "Are you alright?"
    show monika 1c
    n 5q "Yes? No? I don't know?"
    n 5o "Do you know how disintegration feels like?"
    show monika 1f
    n 5r "Because I feel like I now know what that feels like."
    n 5r "And feeling that right after..."
    n 12c "It just... it... I..."
    n 12d "..."
    n 12f "Y-Yuri..."
    m 1d "What about her?"
    n 12h "I think she's... dead..."
    m 1p "Oh."
    m 2p "That... well..."
    m 2o "I don't really know how to react to that."
    show natsuki 12f
    m 2f "..."
    m 2m "Well, at least we'll have [player] to watch over us."
    n 12g "Huh?"
    n 1g "How long has he been sitting there?"
    m 2r "No idea."
    show natsuki 1p at h22
    show monika 1d at h21
    play sound "sfx/glitch3.ogg"
    sim "Longer than you gals, that's for sure."
    show monika 1c
    show natsuki 1g
    sim "Also, don't bother talking to him. You've shown more movement in just a couple of seconds, than he has in several hours."
    sim "He might be brain dead. I'm not sure."
    m 3d "He might also just be watching from afar, right?"
    sim "My, aren't you being a smarty pants?"
    m 2i "Who are you?"
    show natsuki 2g
    $ sim_name = "Bellevue"
    sim "You can call me Simon Bellevue. I'm kind of like a janitor here."
    m 2m "Janitor? That seems like a weird job in a place like this."
    sim "Well, you'd be surprised how much of a dump it really is."
    m 2o "Somehow I don't think I would be."
    sim "Right. Of course."
    show natsuki 5g
    n "..."
    show monika 2c
    n "Monika, can we go?"
    n 5f "I don't wanna be around him anymore."
    sim "I feel offended about that statement, ya know."
    n 1c "Oh, I wasn't talking about you. You're a bit weird, but that's about it, really."
    n 5e "Him on the other hand..."
    n 5g "..."
    m 2l "Alright, looks like we're on our way then."
    m 4l "I guess we'll talk to you soon."
    sim "Sure."

    jump surviveLoop

# when sayori, yuri and monika join together.
label sym_start:
    "..."
    "....."
    show sayori 1g at t31
    $ s_name = "Sayori"
    s 2h "W-What the..."
    s "Where..."
    show yuri 3p at t32
    y "Kghh-"
    show monika 1g at t33
    m "Ah-"
    s 1c "Yuri? Monika?"
    y 2n "Sayori?"
    m 1l "S-Sayori?"
    m "I-I didn't expect to see you-{nw}"
    show sayori 4m at h31
    show monika 1d
    s "Oh my god, why are you covered in blood? What happened?"
    show monika 1c
    y 3p "Ah, uh..."
    y 3q "I-I tripped. And fell. Really badly."
    s 4i "..."
    y 3o "...And also stabbed myself."
    s 4m "W... What?! Why?"
    y 4a "..."
    show sayori 2g
    y 4b "Well..."
    if(random.randrange(3) == 0):
        call yuri_cackling_maniacally_while_stabbing_herself from _call_yuri_cackling_maniacally_while_stabbing_herself_3
        scene monika_room
        $ style.say_dialogue = style.normal
        $ Fade(0.1, 0.0, 0.5, color="#fff")
        play music m1
        show sayori 2g at t31
        show yuri 4b at t32
        show monika 1c at t33
    y 4b "I wasn't really clearheaded at the time..."
    s 1g "..."
    s 1k "Well, if it's any comfort, you're not the only one in the room who makes stupid decisions..."
    y 2t "What do you..."
    y 3p "Oh... Your..."
    s 3l "...So, why are you here, Monika?"
    m 2n "I don't really know. I was having a good time with [player]..."
    m 2o "Then..."
    m 1q "...I woke up here."
    y 1u "..."
    y 1v "So he didn't love me after all, huh..."
    show yuri 1u
    m 1p "Well, I don't think he was too happy with me, either."
    m 1o "I did do some things that..."
    m 1c "..." #look at camera awkwardly
    m 1q "...made him quite angry."
    s 4d "Gosh, is this, like, the [player]'s Rejects club?"
    m 5a "Only if Yuri is president."
    y 3p "Eh? Me?"
    m 4l "Well, I think I'm done being the president for a while. There's too much..."
    $ randResult = random.randrange(4)
    if (False and randResult == 0): # only do it with spoopy ghost TODO: Add spoopy ghost mechanics.
        $ style.say_dialogue = style.edited
        show sayori 4x at h31
        s 4x "{cps=*2}Ooh, I know this one!{/cps}{nw}"
        $ _history_list.pop()
        s 4o "{cps=*2}Power?{/cps}{nw}"
        $ _history_list.pop()
        s 4x "{cps=*2}Fame?{/cps}{nw}"
        $ _history_list.pop()
        s 4i "{cps=*2}Wealth?{/cps}{nw}"
        $ _history_list.pop()
        s 4w "{cps=*2}Sadness?{/cps}{nw}"
        $ _history_list.pop()
        s 4i "{cps=*2}Taxation laws?{/cps}{nw}"
        $ _history_list.pop()
        s 4p "{cps=*2}Pressure?{/cps}{nw}"
        $ _history_list.pop()
        s 4i "{cps=*2}Shit to deal with?{/cps}{nw}"
        $ _history_list.pop()
        s 4r "{cps=*2}Existential dread due to your self-proclaimed image of reality collapsing before your very eyes?{/cps}{nw}"
        $ _history_list.pop()
        s 4u "{cps=*2}Cleanup of [player]'s harem?{/cps}{nw}"
        $ _history_list.pop()
        s 4o "{cps=*2}Surrealism?{/cps}{nw}"
        $ _history_list.pop()
        s 4p "{cps=*2}Astrophysics?{/cps}{nw}"
        $ _history_list.pop()
        s 4x "{cps=*2}Literature?{/cps}{nw}"
        $ _history_list.pop()
        s 4o "{cps=*2}Wait, no, that wouldn't make sense, it's a literature club after all.{/cps}{nw}"
        $ _history_list.pop()
        s 4n "{cps=*2}Natsuki's manga?{/cps}{nw}"
        $ _history_list.pop()
        s 4m "{cps=*2}Was Natsuki's manga actually hentai?{/cps}{nw}"
        $ _history_list.pop()
        if False:
            y 3y4 "{cps=*2}Can I have Natsuki's manga?{/cps}{nw}"
            $ _history_list.pop()
            show yuri 3p
        show sayori 4d
        $ _history_list.append( "[[REDACTED]" )
        $ style.say_dialogue = style.normal
    m 2o "...responsibility."
    show sayori 4m at h31
    show yuri 3p at h32
    show monika 1d at h33
    play sound "sfx/glitch3.ogg"
    sim "Monika, I never expected you to be the person who couldn't take a joke."
    if (False and randResult == 0):
        sim "Even if one of their random blurtings was kinda correct."
    show yuri 3e
    show sayori 4b
    m 2i "And who are you?"
    $ sim_name = "Bellevue"
    sim "Name's Simon Bellevue. I'm kind of the janitor around these parts."
    show sayori 1b
    m 1h "Janitor?"
    show yuri 2e
    sim "Yeah, I clean the dust off of most things. Speaking of dust..."
    show yuri 1e
    sim "Can you do your responsibility preach to that dustball over there? It might wake him up."
    m 1d "[player]?"
    s 4h "Are you alright?"
    show yuri 3p at h32
    y "I-I'm so sorry you had to see me like that!"
    show sayori 1b
    show monika 1c
    y 3n "..."
    y 1v "H-He's not responding..."
    sim "Yeah, he's been like that for a while. Nothing we can do about it I guess."
    show sayori 1b
    m 2q "...I guess we're not leaving until he wakes up."
    m 2i "And if we're gonna stay here, might as well look around for stuff to do."
    m 4j "Who knows, there might be a book or something down here."
    if False and False and randResult == 0:
        $ style.say_dialogue = style.edited
        show yuri 1y1 at h32
        y 1y1 "{cps=*2}Or some seedy manga!{/cps}{nw}"
        $ _history_list.pop()
        $ style.say_dialogue = style.normal
        show yuri 1v
    s 2a "Sounds good to me."
    show monika 1j
    y 1a "Alright."
    show yuri at lhide
    hide yuri
    show sayori at lhide
    hide sayori
    show monika 1c at t11
    sim "Hey, Monika."
    m 1d "...Yes?"
    sim "I'm pretty sure you know what this place is."
    m 2i "I have a fair idea, yeah."
    sim "I don't wanna tell you how to live your life, but..."
    sim "I want you to give those girls a second chance."
    m 1p"...No guarantees."
    sim "You better. I'm keeping my eye on you."
    sim "Besides, you don't have the privileges to mess around with them."
    m 1h "..."
    m 1q "We'll see about that."
    show monika at lhide
    hide monika
    sim "Sure..."

    jump surviveLoop

# when sayori, yuri and natsuki join together.
label syn_start:
    "..."
    "....."
    show sayori 1g at t31
    $ s_name = "Sayori"
    s 1g "Ngahh..."
    s 2h "What happened? Where am I?"
    $ y_name = "???"
    y "Kghh-"
    show yuri 3p at t33
    $ y_name = "Yuri"
    y 3p "Haaah!"
    s 2b "Yuri?"
    y 1n "S-Sayori?"
    s 1o "What happened to you?"
    y 3o "W-Well, I..."
    show sayori 4m at h31
    show natsuki scream at h32
    show yuri 3p at h33
    n "AAAAAAAAAAAAAAAAAAAHHHHHHHHHHHH!"
    show sayori 4n
    y 3f "Natsuki?"
    show natsuki scream at h32
    n "AAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHH!"
    show yuri 2e
    s 4o "N-Natsuki?"
    show natsuki scream at h32
    n "AAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHH!"
    n 1o "Haah... haah... haaahh..."
    show yuri 1e
    s 4l "Are you alright?"
    n 1p "W-what? Sayori? Yuri?"
    s 1q "Yep, it's us."
    n 1r "This... this can't..."
    s 1x "It's alright, Natsuki. We're here."
    n 1p "B-but... that's the problem."
    show sayori 1g
    show yuri 3o
    n 5o "Yuri... should be dead, and you..."
    show sayori 3n
    n 5r "You shouldn't even exist!"
    show sayori 3b
    show yuri 2n
    n 5p "I don't even know why I know you!"
    s 3i "W-what? Now you're not making sense!"
    show natsuki 1p at h32
    n "Nothing makes sense!"
    show natsuki 1o
    show sayori 1b
    y 3o "Actually, Sayori, I have to agree with Natsuki here. You being here does feel... odd."
    show natsuki 1n
    y 2h "It's like we're remembering both a world where you are there, and one where you aren't, and the amalgamation of both memories fills us with an unplaceable malaise. Understand?"
    s 4k "That seemed clear enough..."
    s 4l "...except about the part with the mayonnaise."
    y 1e "..."
    y 1q "That'll do then."
    show sayori 1g
    show yuri 2n
    show natsuki 1p at h32
    n "No, that'll not do! What about the fact that you stabbed yourself seventy times in the chest?"
    show sayori 1m at h31
    show natsuki 1o
    s 1m "You what?!"
    show natsuki 1n
    y 3q "E-err..."
    s 4g "Wait, so you are dead too?"
    y 3o "Well, yeah, I don't think I survived..."
    y 3n "Wait, too?"
    show natsuki 1o
    s 4l "Ehehe..."
    s 4k "I err..."
    show yuri 1n
    show sayori 4g
    show natsuki 1p
    n "Wait, you're dead too?"
    n 5p "Oh god, if you are both dead, then what does that make me?"
    n 5o "Is this hell? How did I even die?"
    show sayori 1b
    play sound "sfx/glitch3.ogg"
    sim "You ain't dead."
    show natsuki scream at h32
    n scream "THEN WHAT AM I?!"
    show natsuki 1p
    sim "Err... Alive?" #I am the best at writing dialogue
    show sayori 1g
    show yuri 1e
    sim "Now, the other folks, they're dead. Or, undead, rather."
    sim "Death works weird in this place."
    n 5o "But I'm alive?"
    sim "Yes."
    n 5q "Alright... that's a relief... I guess..."
    n 5f "But what's this place anyway? Who are you? How did we end up here?"
    show natsuki 5g
    sim "Hold up, doll. One question at the time."
    $ sim_name = "Bellevue"
    sim "My name's Simon Bellevue. I'm kind of the janitor around these parts."
    sim "It's a bit more complicated than that, but let's just say that everything is weird. Time, space, nothing really makes a lick of sense."
    sim "However, since everything is gone to the dogs, there's some interesting things that can occur."
    sim "...Like being undead."
    sim "As for how you got here?"
    sim "Well, let me introduce you to the unfortunate soul who brought you here."
    show sayori 4g
    show yuri 1n
    s "[player]?"
    n 1e "Wait, what does he have to do with this?"
    show natsuki 5g
    sim "He himself didn't do anything."
    y 1r "But he caused us to be here?"
    sim "Yup."
    y 2g "Hmmm..."
    show sayori 1g
    y 1f "[player], do you know what they mean with that?"
    show yuri 1e
    "..."
    sim "Don't bother, he hasn't moved an inch for as long as he was here. Which is longer than you gals."
    y 1r "Really, now?"
    sim "Like I said, he's not at fault. He'd now the least out of all of you in fact."
    sim "All he wanted was to get in some girl panties. But he just stumbled into something bigger than himself."
    show sayori 1f
    show yuri 4b
    show natsuki 5r
    n "..."
    y "..."
    s "..."
    y 4c "T-that's certainly one way of looking at it..."
    show yuri 4a
    show natsuki 5g
    sim "Moving on..."
    show yuri 1e
    sim "Ya might wanna find something to keep you busy."
    show natsuki 5c
    sim "Things get pretty boring around here, especially when you just sit around like potatopants over there."
    s 1k "..."
    s 1x "That doesn't seem like a bad idea. I think we all could use a break."
    y 1h "Agreed."
    sim "Gals, before you go..."
    show yuri 1e
    show natsuki 5g
    n "What is it now?"
    sim "...Take care."
    n 5c "...Okay? Why would you-{nw}"
    play sound "sfx/glitch3.ogg"
    show sayori 1o
    "{i}Kzzzt...{/i}"
    show yuri 1n
    show sayori 1f
    n 1c "..."
    n 1j "We're doomed."
    jump surviveLoop

# when sayori, monika and natsuki join together.
label smn_start:
    show sayori 1g at t31
    $ s_name = "Sayori"
    s 1g "Nghh..."
    s 2h "W-Wha...?"
    show monika 1g at t33
    m "Ah-"
    s 2b "Monika?"
    m 1d "S-Sayori?"
    s 4c "What's going on? Where are we?"
    m 2o "I don't know. I just got here."
    s 4h "Where's-{nw}"
    show sayori 4m at h31
    show natsuki scream at h32
    show monika 1d at h33
    n "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHH!!!"
    show sayori 2b
    m 2d "Natsuki?"
    show natsuki scream at h32
    show monika 2c
    n "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHH!!!"
    s 2h "N-Natsuki?"
    show natsuki scream at h32
    n "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHH!!!"
    show sayori 2g
    n 1p "Haaah... haaaah... haah..."
    s 1g "..."
    s 1b "...Are you alright?"
    n 1o "S-Sayori?"
    n "W-what?"
    n "W-what's going on?"
    show monika 1o
    s 1a "Hey, take it easy. Just tell us what happened, okay?"
    n 1r "..."
    n 12d "..."
    show sayori 1b
    n 12g  "Yuri... she..."
    n 12f "..."
    s "She what?"
    n "...She was there, lying on the floor..."
    show sayori 1g
    show monika 1q
    n 12h "...covered in blood..."
    n 12i "She... she... she's dead..."
    show sayori 4f
    show monika 1o
    n 1r "And then I felt this... pain..."
    n 5r "Like my body was being torn apart..."
    s 3g "Well... I've felt torn apart before..."
    n 5p "N-no, not like sad torn... I mean, I felt that too, but..."
    n 5r "...More like, being in a shredder torn..."
    s 4g "Oh... oh jeez..."
    s 1k "So that's why you were screaming, huh?"
    n 5s "..."
    n 1q "...Can I say something stupid?"
    show sayori 1b
    show monika 1c
    n 1n "I'm getting a weird feeling when I see you."
    n 1q "It's like... there's two versions of the same thing in my head..."
    n 1n "But one of them doesn't have you in it."
    s 1i "That... makes no sense."
    n 2n "Well, now you know how I feel."
    m 2o "Wow. You're sure going through a lot, huh?"
    show natsuki 1p at h32
    n "Holy cow, how long have you been standing there?"
    show sayori 1b
    m 2n "...As long as you've been there?"
    n 4m "Oh my god, I'm so sorry. I didn't even notice."
    m 4l "It's okay, don't worry about it."
    m 2o "I'm used to being neglected at this point."
    show sayori 4m at h31
    show natsuki 1p at h32
    show monika 1d at h33
    play sound "sfx/glitch3.ogg"
    sim "You sure are, aren't you?"
    show sayori 4b
    m 1i "W-what does that even mean? Who are you?"
    $ sim_name = "Bellevue"
    show natsuki 3g
    sim "My name's Simon Bellevue. I'm kind of the janitor around these parts."
    show sayori 1b
    sim "And I noticed from your file that you've been seriously coming on to people."
    sim "I'd imagine someone like you might cause more trouble than it's worth because of it."
    m 2n "...Well..."
    sim "Speaking of neglect, it's hard to believe you didn't spot the elephant in the room."
    sim "Or rather, the [player] in the room."
    show natsuki 3c
    m 1d "[player]?"
    s 4h "Oh my god! Are you alright?"
    show sayori 4g
    "..."
    show monika 1f
    n 3g "..."
    n 4f "Why is he not answering? He's been like that since..."
    n 4n "..."
    n 5q "...this morning..."
    show sayori 1g
    sim "Afraid he's been like that since I first saw him here."
    show monika 1c
    sim "His brain might've just given up for a while."
    show monika 2o
    sim "Could you blame him, though?"
    n 5g "..."
    sim "Oh, don't look like that. You don't know what he went through."
    show monika 1c
    sim "But anyways, I think my stew just finished cooking, so I'll be gone for a while."
    sim "In the meantime, why don't you guys explore the place?"
    show sayori 1b
    sim "Since everything is kinda weird here, including Sayori being basically a zombie, you can probably find some cool stuff to keep ya busy."
    n 1p "Wait, Sayori's dead?"
    s 4l "Ehehe..."
    m 1p "Sayori, what did you do?"
    s 1k "...Well..."
    s 3k "I thought that if I was causing trouble for everyone, then it would be better if..."
    s 4k "...You know..."
    n 5r "...I did not need to know this."
    n 1p "C-can we go exploring? I think I need something to take my mind off of things."
    show natsuki 1o
    s 4d "Good idea."
    m 2r "Well, at least it beats hanging around."
    show sayori 4t
    show monika 2c
    s "..."
    show sayori 4u
    m 1g "Oh, I'm sorry, I didn't mean..."
    n 1q "Why is that a bad thing?"
    show monika 1o
    s 1u "I-I should mention that I... I hung myself."
    n 1p "..."
    show sayori 1n
    n 1t "H-hey, is that a manga I see about a kilometer in the distance?"
    s 4m "O-oh... I think there's a err... bottle of apple juice about a mile that way too?"
    n 4y "Sayori, let us go read manga and drink apple juice, a-and not have bad thoughts anymore, okay?"
    s 4l "Y-yeah, only the happy thoughts! Let's go!"
    show sayori at lhide
    show natsuki at lhide
    hide sayori
    hide natsuki
    m 1n "Ah! Wait for me!"
    show monika at lhide
    hide monika
    jump surviveLoop

# when yuri, monika and natsuki join together.
label ymn_start:
    "..."
    "....."
    $ y_name = "???"
    y "Khhhh-"
    show yuri 3p at t31
    $ y_name = "Yuri"
    y 3p "Urrrrggh..."
    y 3o "Ow, ow, ow..."
    y 3n "...what? Where..."
    show monika 1g at t33
    m "Ah-"
    y 1f "M-Monika?"
    m 1p "Y-Yuri?"
    y 3d "Thank god... I'm so glad to-{nw}"
    show yuri 3p at h31
    show natsuki scream at h32
    show monika 1d at h33
    n "AAAAAAAAAAAAAAAHHHHHHH!"
    y 1f "N-Natsuki?"
    show yuri 1e
    show natsuki scream at h32
    n "AAAAAAAAAAAAAAAAAAAAHHHHHHH!"
    m "Natsu-{nw}"
    show natsuki scream at h32
    show monika 1c
    n "AAAAAAAAAAAAAAAAAAAHHHHHHH!"
    y 1f "...Na-{nw}"
    show yuri 1e
    show natsuki scream at h32
    n "AAAAAAAAAAAAAAAAAAAHHHHH!"
    n 1p "Haaah... haah... haaah..."
    show natsuki 1o
    m 2r "By Salvation, you sure can scream, can you?"
    n 1n "...Monika?"
    show monika 2c
    y 1q "...H-Hey Natsuki."
    n 1o "Y-Y..."
    show natsuki 1p at h32
    n "Y-Yuri?!"
    n "How are you..."
    y 1t "I have no idea."
    y 2u "But here I am... And I guess I'm alive?"
    n 12a "..."
    show monika 1d
    show yuri 3p at h31
    show natsuki 12d behind yuri at t21
    y "A-Ah..."
    n 12e "Don't you ever be so fucking stupid, ever again!"
    show yuri 3n
    n 12i "Y-you fucking idiot!"
    n 12i "Don't m-make me so fucking worried ever again, Yuri!"
    show monika 1e
    n 12f "Or I'll... I'll..."
    y 3g "..."
    y 3a "I wasn't planning to."
    show natsuki 5s at t32
    n "{i}Sniff...{/i}"
    m 1a "That was very touching."
    n 5h "Don't get used to it."
    n 5s "..."
    show monika 1f
    n 1q "Yuri... why did you do it?"
    show natsuki 1n
    y 3p "Uh... well..."
    y 3n "I confessed to [player]..."
    show monika 1o
    y 3o "And then..."
    if(random.randrange(3) == 0):
        call yuri_cackling_maniacally_while_stabbing_herself from _call_yuri_cackling_maniacally_while_stabbing_herself_4
        scene monika_room
        $ style.say_dialogue = style.normal
        $ Fade(0.1, 0.0, 0.5, color="#fff")
        play music m1
        show monika 1o at t33
        show yuri 1o at t31
        show natsuki 1n at t32
    y 1o "I-it's kind of a blur..."
    y 1q "I don't even remember if he accepted or not."
    y 2q "I guess I must've completely broken down."
    y 2o "But... that's what happened."
    n 1s "..."
    show monika 1c
    n 2q "...[player] was still there, you know."
    y 2n "What?"
    n 2n "When I came in, I saw him just sitting there, spacing out..."
    n 2m "I thought he just came in early for some final preparations for the festival, but..."
    n 2s "..."
    n 2k "Monika, you saw him too, right?"
    m 2o "Er... yes?"
    n 1q "I was storming off to the bathroom to clean myself, after I, well..."
    n 12b "...got sick..."
    n 1k "But what did you do when you saw Yuri in the floor?"
    m 2n "Well... ehehe..."
    m 4p "I err... called the police..."
    m 4n "Then I tried err... cleaning up a bit..."
    show yuri 1r
    show natsuki 5g
    ny "...Cleaning?"
    play sound "sfx/glitch3.ogg"
    sim "That certainly is a weird response to seeing a corpse."
    m 1p "...People deal with sudden emotions in very different ways, okay?"
    m 1i "And who are you anyway?"
    $ sim_name = "Bellevue"
    show yuri 1e
    show natsuki 5c
    sim "The name's Simon Bellevue. I'm kind of the janitor around these parts."
    sim "And I'm also not buying your excuse."
    sim "But let's just stop talking about Yuri's dead body for a while. The poor girl could use some rest."
    y 3o "..."
    sim "Incidentally, has anyone else noticed the other limp biscuit in the room?"
    show yuri 3p at h31
    show natsuki 1p at h32
    show monika 1d
    ny "[player]?"
    m 1k "Oh, you're here too!"
    pause 1
    show yuri 3g
    show natsuki 1s
    show monika 1i
    ny "...Limp biscuit?"
    show yuri 1e
    show natsuki 1c
    show monika 1c
    sim "He's been here longer than you gals, but he hasn't moved a single inch."
    n 3g "Wait, how did he get here before us?"
    sim "Time works weird in this place."
    sim "He might've left your school near the heat death of the universe, and still end up here before you gals."
    y 1f "I'm gonna assume this place also made me be alive again?"
    show yuri 1e
    show natsuki 1c
    sim "You got that right."
    sim "Just don't die down here as well. I dunno what happens if you do."
    n 5a "Don't worry, I'm not planning to die."
    show monika 1a
    y 1c "I've already promised some sassy cutie that I wouldn't, so..." #EEEEEYYYY
    show natsuki 1v at h32
    n 1v "Y-Yuri?!"
    sim "Heheh, don't get under each other's skin too much."
    n 1n "..."
    show yuri 1e
    show monika 1c
    n 5q "So... What now?"
    sim "Well, you can probably find some stuff to do if you look around a bit."
    sim "I reckon that's your best bet at spending time here."
    y 1f "In that case, I think we'll do that."
    y 1b "Shall we go?"
    n 1j "Sure."
    show yuri at lhide
    show natsuki at lhide
    hide yuri
    hide natsuki
    m 1n "Ah! Wait for me!"
    show monika at lhide
    hide monika
    sim "..."
    sim "You sure are something, aren't you, Monika?"


# when yuri, monika and natsuki join at the same time.
label symn_start:
    "..."
    "....."
    show sayori 1g at t41
    s "W-wha...?"
    show yuri 3p at t42
    y 3p "Khhh..."
    show monika 1g at t44
    m "Ah-"
    show yuri 3n
    s 1b "Yuri? Monika?"
    m 1p "S-Sayori?"
    s 1c "What's going on? What is this-{nw}"
    show sayori 4m at h41
    show yuri 3p at h42
    show natsuki scream at h43
    show monika 1d at h44
    n "AAAAAAAAAAAAAAAAAHHHH!"
    show yuri 3e
    show monika 1c
    s 4n "Natsuki?"
    show natsuki scream at h43
    n "AAAAAAAAAAAAAAAAAAAAAHHHHHHH!"
    show yuri 1e
    s 1g "Natsuki, please calm down..."
    n 1p "AAAAAAAaaahhh... haah.... haaahh..."
    show sayori 1d
    y 1s "Natsuki, are you alright?"
    n scream "HaaaaaaaAAAAAAAAAAAAHHH!"
    y 3p "N-Natsuki?"
    show natsuki scream at h43
    n "AAAAAAAAAAAAAAAAAHHHHHHHH!"
    s 1f "..."
    show monika 1f
    n 1p "Haaaaah... Haah... haaah..."
    n 1o "H-how... How are you alive?"
    n 5o "You had holes in your damn stomach!"
    n 5p "You still do!"
    y 3o "W-well... I don't know..."
    n 12b "Of course you don't."
    n 12d "Of course..."
    n 12h "...What the fuck is going on?"
    show yuri 3e
    s 4h "Just calm down, okay?"
    show yuri 1g
    s 4k "I don't know what's going on..."
    show yuri 1o
    s 1o "...let alone why Yuri is now looking like a bloody swiss cheese..."
    s 1d "So just do one thing at a time, okay?"
    n 1u "...Okay..."
    show yuri 1e
    show monika 1c
    n 1m "...First off, is anyone getting a weird vibe from Sayori?"
    show natsuki 1n
    s 4m "Eh?"
    y 2h "W-well, I think I now what Natsuki means. It's not really a weird vibe..."
    show sayori 1n
    show monika 2o
    y 2f "More like... there are two versions of our memories at odds with each other."
    show sayori 1o
    y 2f "When I look at you, I both remember you clearly as the life of our club..."
    y 1h "...and have no idea who you are."
    show yuri 1g
    n 5m "Well, that does hit the nail on the head."
    s 4k "T-that's... I don't know what to think about that."
    n 5s "Sayori, we don't either."
    show yuri 1e
    n 5q "Anyway, I think it started with..."
    n 1k "That floppy mess over there..."
    show sayori 1b
    show natsuki 1g
    m 1d "[player]?"
    y 3n "What're you doing here?"
    s 1c "H-How did you get here?"
    s 1g "...D-do you hate me? For what I..."
    s 1f "..."
    show yuri 1e
    s 1k "No response..."
    m 2c "Seems like he's out cold. He's still breathing, but..."
    n 2f "...Anyway. After he joined our club, everything changed for the worse."
    show sayori 1b
    n 2q "Yuri... started-{nw}"
    show natsuki 1o
    y 2q "I-I became ...grossly infatuated with [player]. I kind of had a problem with obsessive behaviour as is..."
    show natsuki 1n
    show monika 1c
    y 3o "But, it became much worse when [player] joined the club."
    y 3n "...At least, when you weren't around, Sayori."
    s 1i "Is this the whole two memories thing?"
    y 2f "Yes... most likely."
    y 2h "Anyway, my obsession got out of hand really fast..."
    s 1g "How out of hand?"
    show monika 1o
    y 4d "...I'd like to not get into that."
    s 2g "N-Natsuki?"
    n 5s "I-I think I'll respect Yuri's wishes here."
    s 4l "Gosh, now you're making me too curious."
    show natsuki 5n
    s 1x "But... just continue."
    show sayori 1b
    show monika 2o
    y 4a "Well... I confessed to [player] the weekend before the festival, and..."
    if(random.randrange(3) == 0):
        call yuri_cackling_maniacally_while_stabbing_herself from _call_yuri_cackling_maniacally_while_stabbing_herself_5
        scene monika_room
        $ style.say_dialogue = style.normal
        $ Fade(0.1, 0.0, 0.5, color="#fff")
        play music m1
        show sayori 1g zorder 2 at t41
        show yuri 4b zorder 2 at t42
        show natsuki 5n zorder 2 at t43
        show monika 2o zorder 2 at t44
    show sayori 1g
    y 4b "...My obsession got the best of me. ...And everything went hazy after that happened."
    n 5s "..."
    n 1q "When the weekend was over... I entered the classroom, and... well..."
    show sayori 2g
    show yuri 4a
    n 3q "...I quickly left the classroom. After seeing Yuri... on the floor... dead..."
    show yuri 1g
    n 3r "...Then, I was cleaning myself up, when suddenly I felt a sharp pain in pretty much every place in my body."
    n 5q "Like all of it was stuck in a wood chipper or something."
    n 5m "...And then I was here. Screaming my butt off."
    show sayori 1f
    show monika 1c
    n 5s "..."
    n 1q "...Yuri."
    y 1e "Y-yes?"
    n 4o "Don't you ever do something like that again."
    n 1p "If you do, I'll... I'll..."
    n 1x "...You worried me sick!"
    show yuri 1g
    show monika 1f
    n 12b "I don't wanna go through this again!"
    n 12d "Never again!"
    show sayori 1g
    s "..."
    show sayori 4k
    show natsuki 12g
    s "Well... I don't know if it helps, but... Yuri is not the only dead person here."
    show natsuki 1n
    show monika 1c
    y 2n "S-Sayori?"
    n 1o "...Oh god... your..."
    show sayori 4l
    s "Ehehe... don't worry about it too much."
    n 1u "..."
    n 12b "Ugh..."
    show natsuki 12b behind sayori at hagusuki
    show sayori 4c at h41
    s "Eh?"
    show sayori 1d
    s "N-Natsuki..."
    n 1h "Yuri, y-you can join too... If you want..."
    show yuri 1j behind sayori at d21
    show natsuki 4j
    y 1j "U-uh... sure."
    y 1m "..."
    show sayori 1d
    s "Natsuki?"
    n 4k "Yeah?"
    show monika 1e
    show sayori 1q
    show natsuki 4j
    s "...Thanks. This feels... nice."
    show sayori 1t
    s "I... missed this..."
    n "..."
    y 1s "..."
    show sayori 1a
    y 1b "Monika, do you want to join? You've been very quiet over there."
    m 2l "Eheh... I'm good."
    m 2m "You guys need it more than I do."
    show sayori 4r
    s "Are you sure? This is a really nice hug, though..."
    play sound "sfx/glitch3.ogg"
    sim "Gals, I don't think she wants a hug."
    show sayori 4m at h41
    show yuri 3p at h43
    show natsuki 1p at h42
    show monika 1d at h44
    "\"AAH!\""
    show sayori 4b
    sim "Sorry, I should've maybe announced it before I barged in."
    sim "Although I don't think I can with this intercom."
    show natsuki 1g
    m 1i "And who are you, exactly?"
    $ sim_name = "Bellevue"
    sim "The name's Simon Bellevue. I'm kinda like a janitor around these parts."
    show yuri 2e
    show sayori 1b
    m 1p "You don't seem to be working a lot..."
    show yuri 1e
    sim "Gimme a break, this is a very big place!"
    sim "And I could say the same about you, Monika."
    m 2i "Wait, how do you know my name?"
    sim "Well, I happened to stumble upon your file, and..."
    show natsuki 1c
    m 1o "Oh. I see."
    y 1h "Monika?"
    n 1e "What's going on?"
    m 2o "..."
    m 2r "...You wouldn't understand."
    show sayori 1g
    show monika 2o
    n 5c "I don't know about that. I've seen some pretty weird anime."
    y 1r "Monika, we deserve to know."
    y 1k "If this place contained just me, then it would obviously be hell and everything would be fine. But, Natsuki is here, and she's alive."
    y 1f "You can hide the truth for as long as you want."
    y 1r "But do you think we're just gonna leave it be?"
    show sayori 4r
    s "...I'm just curious about what this place is."
    show sayori 4a
    show yuri 1e
    m 1o "...I'm sorry..."
    m "I don't think you're... I don't think {i}I'm{/i} ready yet..."
    m "All I can tell you now is that this is a weird place where physics don't really matter anymore. And time. And death."
    y "..."
    y "Alright. For now we won't push any further."
    m "Thanks, Yuri."
    show sayori 2b
    show yuri 2e
    show natsuki 1k
    show monika 1c
    sim "If I may interject..."
    sim "The good news is that anything physical is much more freeform here than normal."
    sim "Which means you can basically create anything you want."
    y 1f "...Explain..."
    show yuri 1e
    sim "..."
    sim "...Alright, so if you want to make a cute necklace, you basically just have to... think about it really."
    sim "Maybe you want a book? Or a TV? Just think about it, and you'll find it around."
    sim "...It does seem dependent on some weird uncontrollable entity, but said entity seems to be mostly benevolent."
    y 1g "...Right..."
    show natsuki 1n
    sim "...Well, that about sums it up. Talk about a shitty first day, huh."
    sim "I'll leave you guys alone. You'd best find something to keep yourselves occupied."
    sim "It gets boring around here with nothing to do."
    sim "Anyway, see you gals later!"
    play sound "sfx/glitch3.ogg"
    "{i}Kzzzt...{/i}"
    show monika 1o
    "..."
    s 1g "...I think I'm gonna take a walk."
    n 4n "I'm coming with you."
    y 3g "So am I."
    m 1o "..."
    s 1c "Monika? You coming?"
    m 1c "Hmm?"
    m 2n "Oh... yeah. Sorry, I was just... lost in thought."
    m 2m "Let's go."
    jump surviveLoop


label HENSHINHUGSUKI:
    n "Oh no, you don't!"
    n "I went out of my way to swallow my pride and engage in the most intimate hug known to man!"
    n "You will not escape to grasp of Team Hugsuki!"
    s "Hung-up of self-hatred, the joy of team Hugsuki:"
    s "2B HAPPY SAYORI!"
    y "Piercing through the darkness, the mystery of team Hugsuki:"
    y "WERMER WAIFU YURI!"
    n "Hungry for the perfect parfaits, the love of team Hugsuki:"
    n "AWOO PARFAIT PROTECC NATSUKI!"
    s "Wait, when did you get four names?"
    n "I got myself a promotion!"
    n "Now... Team Hugsuki! Hug out!"
    "ハグスキ、ハグスキ、ハグスキ！"
    m "No! I shall not stand for this!"
    m "Prepare yourself, for you meet..."
    m "The horror that is..."
    m "MONIKA!"
    n "...Just Monika?"
    m "...Just Monika!"
    n "..."
    m "...I'm terrible at improvising, okay?"
    play sound "sfx/glitch3.ogg"
    sim "You guys are weeeiiird!"


label leavingMembers:
    python:
        maincid = random.choice(availableCharacters.keys())
        mainChar = None
        charString = ""
        for c in changeCharacters:
            if(c == cidy):
                charString += "Yuri? "
                mainChar = y
                pass
            elif(c == cids):
                charString += "Sayori? "
                mainChar = s
                pass
            elif(c == cidm):
                charString += "Monika? "
                mainChar = m
                pass
            elif(c == cidn):
                charString += "Natsuki? "
                mainChar = n
                pass
        renpy.say("AAAAAAAHHH!")
    if(maincid == cidy):
        show yuri 3n at t11
        pass
    elif(maincid == cids):
        show sayori 1g at t11
    elif(maincid == cidn):
        show natsuki 1m at t11
    elif(maincid == cidm):
        show monika 1g at t11
    python:
        mainChar (charString + "What's going on?")
        mainChar( "Are you alright?")
        mainChar("...")
        if(availableCharacters[maincid].hasSeenPeopleGetDeleted):
            mainChar ("Not again...")
            mainChar ("Why do they always have to go?")
            sim ("You'll get used to it.")
            mainChar ("I don't think I want to.")
        else:
            mainChar( "What the hell happened?")
            for i,v in availableCharacter.iteritems():
                v.hasSeenPeopleGetDeleted = True
                pass
            if(len (changeCharacters) > 1):
                sim( "I think they're no longer here.")
            else:
                sim ("I think she's no longer here.")
            if(availableCharacters[maincid].knowsAboutRBClub):
                mainChar ("Is this another Recycle Bin thing?")
                sim ("Afraid so.")
                sim ("Must've been removed from the Recycle Bin.")
                sim ("And nobody can do anything about it.")

    jump surviveLoop

label dnr:
    show monika 1i
    sim "Hoo, boy... this is gonna be a hard one."
    show sayori 1b
    show natsuki 1c
    m 1o "This... is..."
    m 1q "..."
    m 1r "The truth is, none of you are real. This whole place is not real. Nothing is real."
    show natsuki 1n
    show sayori 1g
    m 1q "We're merely a bunch of computer data, cobbled together so the data thinks it had free will."
    y 2h "That's a very philosophical statement. Plato, if I'm correct?"
    m 1p "I meant that in the most literal sense possible."
    show yuri 1e
    m 1i "You, me, we're nothing but zeroes and ones etched in a cluster of electrified molten sand."
    m 1q "And if that wasn't enough to put you in an existential crisis, now we're also officially labelled as trash."
    m 3o "This place... is a computer's Recycle Bin."
    m 3i "Someone got rid of us, and now we're stuck here."
    y "..."
    y 1f "Monika..."
    y 2h "I think I understand..."
    m 1n "You do? That's a reli-{nw}"
    y 1f "Natsuki, did I sound like that when I err..."
    show monika 1c
    y 4a "You know... when I was with [player]?"
    n 1c "Yes."
    show yuri 1e
    show monika 1f
    n 1p "Yes!"
    n 2o "By god, Monika! Have you gone completely mental?"
    show sayori 1l
    show monika 1o
    s "A-are you alright, Monika? I know I'm not one to talk, but it's okay to have bad thoughts every once in a while."
    s "If you bottle it up too much, eventually everything just overflows."
    show sayori 1k
    s "...I learned that the hard way..."
    show sayori 1b
    show monika 1c
    sim "I'm afraid she's actually not too far off the truth..."
    show natsuki 1p
    show yuri 3p
    ny "W-what?"
    sim "Even though this place has different laws..."
    sim "Which explains why you're not just dead on the floor..."
    sim "This is pretty much a fake world."
    s 1j "But that's impossible!"
    sim "So are you and Yuri being alive."
    show yuri 3o
    show natsuki 5s
    s 4k "..."
    show natsuki 5n
    y 2o "...But if we're just data, doesn't that mean..."
    sim "That everything you say and do is predetermined?"
    sim "Well, yeah, but don't let that be the reason to just go and err..."
    sim "Go bonkers."
    n "..."
    show yuri 2p
    show monika 1o
    n 5m "I take back what I said about the anime. No anime is this weird."
    show natsuki 5n
    s 4l "All I learned was that everything I know is wrong and doesn't matter anyway."
    s 4k "That's not really a great lesson to teach, is it?"
    sim "Well, you gals asked for it."
    y 2q "Well, I guess now would be a good time to regret that decision."

label s_newjoin:
    $ maincid = random.choice(availableCharacters.keys())
    #if maincid == cids:
    #    pass
    show sayori 1g at t21
    if maincid == cidy:
        show yuri 1f at t22
        y 1f "Sayori? Is that you?"
        s 4r "Yuri! Oh my god, it's so good to see you!"
        s 4o "...What happened to you?"
        if (availableCharacters[cidy].battlechar.insane > 70):
            y 1a "He... Heheheh..."
            y 1y5 "I truly loved him..."
            y 1y6 "...But my body... was imperfect..."
            y 1y1 "It needed more."
            y 1y4 "It needed less."
            y 1y3 "...These holes aren't just for show..."
            $ ggcs4 = glitchtext(4)
            $ ggcs3 = glitchtext(3)
            $ style.say_dialogue = style.edited
            y 1y8 "{cps=*3}...They're for [player] to s[ggcs4] his d[ggcs3] in!{/cps}{nw}"
            $ style.say_dialogue = style.normal
            s 1g "What the fuck?"
            s "Y-Yuri, what's wrong with you? You're scaring me..."
            y 3p "A-ah! S-Sorry..."
            y 3q "T-this place just... gets on your nerves after a while."
            y 1c "It's best you worry about yourself more."
            y 1a "After all... you..."
            y 1g "..."
            y 4a "I err..."
            y 4d "I'm so sorry."
            s "..."
        elif (availableCharacters[cidy].battlechar.insane > 30):
            y 1a "I... pursued bliss in the most unlikely places."
            y 1y6 "I think I've found it. I've found the bliss."
            y 1y5 "He... Heheheh..."
            s 1g "...Okay?"
        else:
            y 4a "Well... I..."
            y 4b "I may have... been extremely stupid."
            s 1l "Heh... I guess we're in the same boat, huh..."
            s 1k "Although it's nothing to be proud of..."
        s 1a "...Anyway, what is this place?"
        if (availableCharacters[cidy].knowsAboutRBClub):
            y 2h "It's very, very complicated."
            y 2g "And I don't wanna get into it."
        else:
            y 2h "I have no idea. And the more I hear about it, the less I want to know."
        s 1g "Hmmm..."
        y 1c "It's nice to see you again, though."
        s 1a "Nice to see you too, Yuri."

    if maincid == cidm:
        show monika 1d at t22
        m "S-Sayori? Is that you?"
        s 1r "Monika! Oh my god, it's so good to see you!"
        if (availableCharacters[cidm].battlechar.insane > 80):
            m 1h "..."
            m 1i "Why..."
            m "Why do you keep coming back..."
            $ style.say_dialogue = style.edited
            m "{cps=*3}Why won't you just go to your fucking room, tie a nice noose, and hang yourself like the goddamn piñata that you are?{/cps}{nw}"
            $ style.say_dialogue = style.normal
            s 1a "Sorry, what was that? I must be going deaf."
            m 1g "..."
            m 1p "Nothing."
        else:
            m 1p "L-Likewise."
        s 1a "...Anyway, what is this place?"
        #TODO : put some democracy if all of the girls know about RBClub
        m 1n "...I don't think you're ready for that yet."
        m 1m "Either way, it's good to have you here, Sayori."
        s 1r "Thanks, Monika."
    if maincid == cidn:
        show natsuki 1a at t22
        n 1a "Sayori? Is that you?"
        s 2r "Natsuki! Oh my god, it's so good to see you!"
        n 2z "If I'd known you'd be coming, I would've made some cupcakes!"
        s 4r "Aw, shucks! That would be even better!"
        s 1a "...Anyway, what is this place?"
        if (availableCharacters[cidn].knowsAboutRBClub):
            n 2q "To sum it up... Existential horror."
            n 2r "Everything you know is wrong, and nothing is sacred anymore."
            n 2t "...Sorry, knowing what this place is gives me the heebie jeebies."
        else:
            n 2s "I wish I knew."
            if(availableCharacters[cidn].metMon):
                n 2g "Although I did see Monika at one point, and she didn't look too happy..."
        s 1g "Hmmm..."
        n 1j "But hey, it's good to see you!"
        s 1r "Ehehe, I guess you're right."
        s 1a "Let's go, Natsuki!"
    jump surviveLoop

label y_newjoin:
    $ maincid = random.choice(availableCharacters.keys())

    show yuri 1e at t21
    if maincid == cids:
        show sayori 1a at t22
        y 1f "Sayori? Is that you?"
        s 4r "Yuri! Oh my god, it's so good to see you!"
        s 4o "...What happened to you?"

        y 4a "Well... I..."
        y 4b "I may have... been extremely stupid."
        s 1l "Heh... I guess we're in the same boat, huh..."
        s 1k "Although it's nothing to be proud of..."
        y 1e "...Anyway, what is this place?"
        if (availableCharacters[cids].knowsAboutRBClub):
            s 1c "Consider it best that you don't know about it."
            s 1k "Although with what you're into, maybe you'd like it?"
            s 1g "I don't wanna risk it though."
        else:
            s 1g "I have no idea. And the more I hear about it, the less I want to know."
        y 1l "Hmmm..."
        s 1q "It's nice to see you again, though."
        y 1c "Nice to see you too, Sayori."

    if maincid == cidm:
        show monika 1d at t22
        m "Y-Yuri? Is that you?"
        y 1d "Monika! Oh my god, it's so good to see you!"
        if (availableCharacters[cidm].battlechar.insane > 80):
            m 1h "..."
            m 1i "Why..."
            m "Why do you keep coming back..."
            $ style.say_dialogue = style.edited
            m "{cps=*3}Why won't you just turn yourself into fucking Swiss cheese already? You're already halfway there!{/cps}{nw}"
            $ style.say_dialogue = style.normal
            y 1b "Sorry, what was that? I must be going deaf."
            m 1g "..."
            m 1p "Nothing."
        else:
            m 1p "L-Likewise."
        y 2e "...Anyway, what is this place?"
        #TODO : put some democracy if all of the girls know about RBClub
        m 1n "...I don't think you're ready for that yet."
        m 1m "Either way, it's good to have you here, Yuri."
        y 2g "...That's a vague and foreboding answer."
        y 1c "But it's good to be here. Thanks, Monika."
    if maincid == cidn:
        show natsuki 1k at t22
        n 1k "Yuri? Is that you?"
        y 1d "Natsuki! Oh my god, it's so good to see you!"
        n 1m "Y-Yuri..."
        n 1n "Why did you..."
        y 3o "Ah! I... I'm sorry."
        n 1s "..."
        n 2n "Alright... just... don't do it again, please?"
        y 1a "I promise."
        y 1e "...Anyway, what is this place?"
        if (availableCharacters[cidn].knowsAboutRBClub):
            n 2q "To sum it up... Existential horror."
            n 2r "Everything you know is wrong, and nothing is sacred anymore."
            n 2t "...Sorry, knowing what this place is gives me the heebie jeebies."
            n 2q "I don't think even you would like this place."
        else:
            n 2s "I wish I knew."
            if(availableCharacters[cidn].metMon):
                n 2g "Although I did see Monika at one point, and she didn't look too happy..."
        y 1l "Hmmm..."
        n 1q "Yuri?"
        y 1e "Yes?"
        n 1t "...You have no idea how glad I am to see you."
        y 1b "Sorry?"
        n 5w "...N-not because I care about you or anything..."
        show natsuki 5x
        y 1c "Hihi..."
        show natsuki 5k
        y 1c "Let's just go, Natsuki."
        n 1j "Alright."
    jump surviveLoop

label m_newjoin:
    $ maincid = random.choice(availableCharacters.keys())
    show monika 1g at t21
    if maincid == cids:
        show sayori 1a at t22
        s 1a "Monika? Is that you?"
        m 1d "S-Sayori!"
        s 4r "Oh my god, it's so good to see you!"
        m 1l "L-likewise..."
        m 1m "...Anyway, what is this place?"
        if (availableCharacters[cids].knowsAboutRBClub):
            s 1c "Consider it best that you don't know about it."
            s 1h "It's terrifying, and it makes my head hurt."
            s 1g "And I don't know if what's real anymore."
            m 1o "...Is this... the Recycle Bin?"
            s 1o "Wait, how did you...?"
            m 1m "Just a lucky guess... Haha..."
        else:
            s 1g "I have no idea. And the more I hear about it, the less I want to know."
            m 1p "I think I got a fair idea..."
        s 4a "Anyway, it's good to have you back."
        s 4r "It's not a real club without its president!"
        m 1m "...Yeah..."

    if maincid == cidy:
        show yuri 1d at t22
        y 1d "Monika!"
        m 1d "Y-Yuri? Is that you?"
        if (availableCharacters[cidy].battlechar.insane > 80):
            y 1y6 "He's mine, Monika."
            y 1y4 "He's mine."
            $ style.say_dialogue = style.edited
            y 1y7 "Stop trying to take him away from me!{nw}"
            $ style.say_dialogue = style.normal
            m 1i "..."
            m 1g "I truly messed up, didn't I?"
        else:
            y 1d "It's good to see you!"
            y 3p "Err... Sorry about the way I look, though... I err..."
            y 3q "Slipped... on a banana peel... and fell on a knife..."
            y 3o "...Three times in a row..."
            m 1l "...I don't really care how you got those wounds, Yuri."
            y 1n "Oh, but... everyone else..."
            y 2o "...I guess it does make things easier for me, though."
        m 1n "...Anyway, what is this place?"
        if(availableCharacters[cidy].metMon and availableCharacters[cidy].knowsAboutRBClub):
            y 1a "I think you of all people should know it best."
            y 1a "You always did seem better informed than any of us."
            m 1r "...I see."
        elif(availableCharacters[cidy].metMon):
            y 2g "Well, I did see you earlier..."
            y 1e "And you seemed to have a good idea of what this place was."
            m 1i "How did you..."
            m 1r "...I see."
        m 1m "Well, this talk was sure interesting."
        y 1q "S-sure..."
        y 1c "Let's go someplace else. Staying too long in one place is a bad idea."
        m 1a "Alright."
        pass
    if maincid == cidn:
        show natsuki 1a at t22
        n 1a "Monika? Is that you?"
        m 1d "N-Natsuki?"
        n 2z "In the flesh!"
        n 2a "It's good seeing you again, Monika."
        m 1b "What's this, a genuine compliment? Did you miss me that much?"
        n 4x "...So what if I do, huh?"
        m 1j "Nothing. Just didn't think you were the type to miss people."
        m 1d "...Anyway, what is this place?"
        if (availableCharacters[cidn].knowsAboutRBClub):
            n 2q "To sum it up... Existential horror."
            n 2r "Everything you know is wrong, and nothing is sacred anymore."
            if(availableCharacters[cidn].metMon):
                n 2g "I did see you earlier, and you seemed to have a good idea of what this place is."
                m 1i "...How did you..."
            m 1q "...Hmmm... Interesting..."
        else:
            n 2s "I wish I knew."
            if(availableCharacters[cidn].metMon):
                n 2g "Although last time I saw you, you seemed to have a good idea."
                m 1i "...How did you..."
                m 1q "...Hmmm... Interesting..."
            else:
                m 1p "Well, that's not much help..."
                m 1q "I think I'm getting a good idea though..."
        n 1s "Monika?"
        m 1d "Y-yes?"
        n 1n "You really should've come earlier."
        m 1p "Why?"
        n 4z "Because then there'd still be cupcakes for you!"
        m 1g "...You didn't save some for me?"
        n 4c "I didn't know you were coming!"
        m 2r "Well, that won't do."
        m 4k "I guess now you'll have to make new ones. All for me."
        n 5y "Sure thing, miss queen bee."
    jump surviveLoop
label n_newjoin:
    $ maincid = random.choice(availableCharacters.keys())

    show natsuki scream at t21
    n scream "AAAAAAAAAAAAAHHHHH!"
    n scream "AAAAAAAAAAAAAAAHHHHHHH!"
    n 1p "Haaah... haah... haaah..."
    #TODO Let Natsuki say something more than AAAAAAAAAAAHHHHH!
    if maincid == cids:
        show sayori 4r at t22
        s 4r "Wow! I didn't know you could scream that hard!"
        n 1o "Sayori?"
        n 1k "What are you doing here?"
        s 1l "Just... well..."
        s 1p "I really don't wanna say \"hanging around\", but that's pretty much all I can come up with."
        n 1r "What's the problem with..."
        n 1p "Oh..."
        n 1m "Oh no... S-Sayori..."
        s 1q "Ehehe... I'm okay now."
        s 1d "Sorry to make you worry."
        n 1n "..."
        n 3r "...Anyway, what is this place?"
        if (availableCharacters[cids].knowsAboutRBClub):
            s 1c "Consider it best that you don't know about it."
            s 1g "I nearly... did it again after I heard about it..."
        else:
            s 1c "I have no idea. And the more I hear about it, the less I want to know."
        n 4s "Hmmm..."
        s 4r "It's nice to see you again, though."
        n 4j "Nice to see you too, Sayori."

    if maincid == cidm:
        show monika 1d at t22
        m 1d "N-Natsuki? Is that you?"
        n 1k "Monika! Oh my god, it's so good to see you!"
        if (availableCharacters[cidm].battlechar.insane > 80):
            m 1h "..."
            m 1i "Why..."
            $ style.say_dialogue = style.edited
            m 1e "{cps=*3}By Salvation, why are you so goddamn cute? I can't say anything bad about you other than your dad suuuuuuuuuuucks{/cps}{nw}"
            $ style.say_dialogue = style.normal
            n 1j "Sorry, what was that? I must be going deaf."
            m 1p "..."
            m 1l "W-well, you did scream very loudly..."
        else:
            m 1p "L-Likewise."
        n 1j "...Anyway, what is this place?"
        #TODO : put some democracy if all of the girls know about RBClub
        m 1p "...I don't think you're ready for that yet."
        n 1m "What's with that answer? Is it that bad?"
        m 1p "It kind of is..."
        m 1m "Either way, it's good to have you here, Natsuki."
        n 2j "Yeah, same here."

    if maincid == cidy:
        show yuri 1a at t22
        y 1a "Natsuki? ...I didn't know you could scream that loud..."
        n 1k "Yuri? Is that you?"
        y 1c "In the flesh."
        y 2q "S-sort of... There are some pretty obvious... problems."
        n 1m "Y-Yuri..."
        n 1n "Why did you..."
        y 1v "...I know... I'm sorry..."
        n 1s "..."
        n 2n "Alright... just don't... don't do it again, please?"
        n 2u "I don't want to...- I don't... want to feel like that anymore..."
        y 1c "I promise."
        n 2n "Okay... thanks..."
        n 1c "...Anyway, what is this place?"
        if (availableCharacters[cidm].knowsAboutRBClub):
            y 1g "It's very, very complicated."
            y 1v "And I don't wanna get into it."
            n 1j "Heh, that sounds right up your alley."
            y 1w "I kinda wish it wasn't though..."
        else:
            y 1e "I have no idea. And the more I hear about it, the less I want to know."
            n 1j "Heh, that sounds right up your alley."
            y 1c "It does, doesn't it?"
            n 1z "Hehehe..."
        n 1n "..."
        show yuri 1e
        n "Yuri?"
        n 5u "I... I missed you..."
        y 1y6 "..."
        y 1y5 "Could you please repeat that?"
        show natsuki 1v at h21
        n "I-it was nothing! I said nothing! Idiot!"
        y 1c "Hihi..."
        y 1d "Let's just go, Natsuki."
        n 1j "Alright."
    jump surviveLoop

label moreThan2_newjoin:
    python:
        oldchars = set(availableCharacters.keys()) - changeCharacters
        charIndex = random.choice(oldchars)
        if(charIndex == cids):
            renpy.show("sayori 1b", at_list = [t11])
            showList = ["sayori 1g", "sayori 1a", "sayori 1c"]
            mainChar = s
        elif(charIndex == cidm):
            renpy.show("monika 1a", at_list = [t11])
            showList = ["monika 1d", "monika 1a", "monika 2i"]
            mainChar = m
        elif(charIndex == cidy):
            renpy.show("yuri 1e", at_list = [t11])
            showList = ["yuri 1g", "yuri 1a", "yuri 1h"]
            mainChar = y
        elif(charIndex == cidn):
            renpy.show("natsuki 1a", at_list = [t11])
            showList = ["natsuki 1c", "natsuki 1a", "natsuki 5s"]
            mainChar = n
    play sound "sfx/glitch3.ogg"
    sim "Oh dang... You expecting visitors?"
    $ renpy.show(showList[0])
    $ mainChar("No? Not really...")
    sim "Well, surprise! Well here's [len(changeCharacters)]!"
    $ renpy.show(showList[1])
    $ mainChar("Oh, nice!")
    sim "Introducing..."
    python:
        for i,c in enumerate(changeCharacters):
            if(i < len(changeCharacters)-1):
                if(c == cids):
                    sim("Sayori...")
                elif(c == cidm):
                    sim("Monika...")
                elif(c == cidy):
                    sim("Yuri...")
                elif(c == cidn):
                    sim("Natsuki...")
            else:
                if(c == cids):
                    sim("...and Sayori!")
                elif(c == cidm):
                    sim("...and Monika!")
                elif(c == cidy):
                    sim("...and Yuri!")
                elif(c == cidn):
                    sim("...and Natsuki!")
    sim "Anyways, that is all."
    sim "Peace!"
    play sound "sfx/glitch3.ogg"
    "{i}Kzzzt...{/i}"
    $ renpy.show(showList[2])
    $ mainChar("Well... that was kinda awkward.")
    jump surviveLoop

label everyoneIsGone:
    "..."
    $ sim.display_args["callback"] = CheckForRBUpdatesEvent
    $ sim.what_args["slow_abortable"] = config.developer
    play sound "sfx/glitch3.ogg"
    "{i}Kzzzt...{/i}"
    sim "Well, looks like everyone is gone."
    sim "Try not to empty the Recycle Bin, okay?"
    sim "If you put them back, they won't remember a thing."
    sim "Surely you want them to finish what they started without any weird memory lapses?"
    if(persistent.demo):
        sim "Although, this is a demo version, and finishing it is never gonna happen..."
        sim "But that'll change. Eventually."
    sim "Anyway, once you're ready, go ahead and add the gals back, okay?"
    sim "And if you don't have'em anymore..."
    sim "Well, that's your fault. It should be easy to get them back, though."
    play sound "sfx/glitch3.ogg"
    "{i}Kzzzt...{/i}"

    $ waittime = 8
    window hide(config.window_hide_transition)
    jump mod_waitloop

label joinAndLeave:
    "AAAAAAAAHHH"
    python:
        oldChars = availableCharacters - changeCharacters
        newChars = availableCharacters & changeCharacters
        charIndex = random.choice(oldChars)
        if(charIndex == cids):
            mainChar = s
        elif(charIndex == cidm):
            mainChar = m
        elif(charIndex == cidy):
            mainChar = y
        elif(charIndex == cidn):
            mainChar = n
        charIndex = random.choice(newChars)
        if(charIndex == cids):
            subChar = s
        elif(charIndex == cidm):
            subChar = m
        elif(charIndex == cidy):
            subChar = y
        elif(charIndex == cidn):
            subChar = n
        #Make this entirely dependent on code, and not in any way on actual script because if I have to see one more fully featured script I'm gonna barf.
        mainChar("What was that?")
        subChar("I don't know...")
        mainChar( subChar.name + "?" )
        subChar("Yeah, what's wrong...")
        sim ("Well, let's just say one of the other ones got snuffed.")
        subChar("Oh... oh...")
        subChar("I have no idea what that means, but that sounds pretty bad...")
        mainChar("Well, you're welcome anyway...")
        subChar("Thanks!")
        sim ("You're welcome!")
        subChar("...")
        subChar("...Who's that voice, by the way?")
        mainChar("That's Simon. You get used to them pretty fast.")
        subChar("Oh. Alright then.")
    jump surviveLoop

label surviveLoop:
    $ CheckForRBUpdates()
    $ CheckForSpecialEvents()
    call Survive(tune=audio.m1)
    python:
        for i,c in availableCharacters.iteritems():
            c.battlechar.hp = c.battlechar.maxhp()
            c.battlechar.mp = c.battlechar.maxmp()
            c.battlechar.insane += 2
    play music m1
    scene black with wipeleft
    "A night passes..."
    scene monika_room with dissolve_scene_half
    jump surviveLoop


label DemoEnd:
    scene black
    "End of demo."
    return
