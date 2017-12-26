screen battle_ui:
    id  "battle_ui"
    fixed:
        window :
            id "Batoru"
            style "window_Null"
            image "gui/textbox.png" xalign 0.5 yalign 0.0
            hbox xalign 0.5 yalign  1.0 yoffset 10 spacing 10:
                $ playerChars = filter(lambda x: x.team == playerTeam, characters)
                for i,c in enumerate(playerChars):
                    fixed xsize 200 ysize 160 yalign 1.0:
                        if(c == currentCharacter):
                            $ frameSize = 160
                        else:
                            $ frameSize = 150
                        frame xsize 200 ysize frameSize yalign 1.0 yanchor  1.0:
                            vbox xalign .5 yfill True:
                                hbox xfill True:
                                    text c.name xalign 0.0
                                    text "LV." + str(c.lvl()) xalign 1.0
                                hbox xfill True:
                                    text "HP:" xalign 0.0
                                    text str(c.hp) + "/" + str(c.maxhp()) xalign 1.0
                                hbox xfill True:
                                    text "MP:" xalign 0.0
                                    text str(c.mp) + "/" + str(c.maxmp()) xalign 1.0
            text ui_text xalign 0.0 yalign 0.0 xoffset 265 yoffset 29
            if current_state == battlestate_startturn or current_state == battlestate_text or current_state == battlestate_execAtk or current_state == battlestate_endTurn or current_state == battlestate_atkDone:
                image "gui/ctc.png" xalign 0.5 yalign 0.0 xanchor 1.0 yanchor 1.0 xoffset 400 yoffset 140
                imagebutton idle "mod/invis.png" xfill True yfill True xalign 1.0 yalign 1.0 xanchor 1.0 yanchor 1.0 action Return(0)
            elif current_state == battlestate_movSel:
                vbox xalign 0.0 yalign 0.0 xoffset 265 yoffset 65 xsize gui.text_width  spacing 5:
                    for m in currentCharacter.atk_list:
                        if(currentCharacter.lvl() > m.lvlReqs):
                            button action Return(m) :
                                style_prefix "choice"
                                #frame xfill True:
                                hbox:
                                    image m.icon_path
                                    null width 10 xalign 0.0
                                    text m.name xalign 0.0
                                    if(m.cost > 0):
                                        text str(m.cost) xalign 0.0
            elif current_state == battlestate_tgtSel:
                for c in characters:
                    imagebutton idle "mod/selector.png" xalign 0.5 yalign 0.5 xoffset c.posX yoffset c.posY action Return(c)
                    if(c.team != playerTeam):
                        text c.name xalign 0.5 yalign 0.5 xoffset c.posX yoffset c.posY -100
                button xoffset 160 action Return(-1) :
                    hover_sound gui.hover_sound
                    activate_sound gui.activate_sound
                    frame:
                        text "Back"
                #vbox xalign 0.0 yalign 1.0:
                #    hbox:

                #    hbox:
                #        for c in characters:
                #            if(c.team != playerTeam):
                #                textbutton c.name action Return(c)
                #    textbutton "Back"  action Return(-1)



init -1 python:
    import random
    from time import time
    from math import ceil
    playerTeam = "Team JM"
    playerteam = playerTeam #Ehehe...
    ui_text = ""

    # Quick inline definition of HistoryEntry, because apparently it's not exposed by default and we need to add history.
    class HistoryEntry():
        def __init__(self, what, kind="nvl", who=None):
            self.kind = kind
            self.who = who
            self.what = what
            self.who_args = { "substitute" : False }
            self.what_args = { "substitute" : False }
            self.window_args = { }
            self.show_args = { }
            self.cb_args = { }

    #CONSTANT STATE ENUM
    battlestate_startturn   = 0
    battlestate_movSel      = 1      #select what you'll do
    battlestate_tgtSel      = 2
    battlestate_execAtk     = 3
    battlestate_atkDone     = 4
    battlestate_endTurn     = 5
    battlestate_victory     = 6
    battlestate_defeat      = 7
    battlestate_spcSel      = 8
    battlestate_itmSel      = 9
    battlestate_actSel      = 10
    battlestate_text        = 11        #continue to the next screen (You're attacked by x)
    # create characters, assign team
    characters = []
    characterOrder = []
    current_state = battlestate_startturn
    turnStart = True

    global currentCharacter
    global selectedMove
    global targetCharacter
    timesHealedOpponent = 0
    lastBattleWon = False

    def AppendBadMove(result):
        persistent.timesHealedOpponent += 1
        if(persistent.timesHealedOpponent < 3):
            result += "\nIn hindsight, this was a stupid idea."
        elif (persistent.timesHealedOpponent < 7):
            result += "\nYou should really stop healing the opponent."
        elif (persistent.timesHealedOpponent < 10):
            result += "\n...Maybe you should check yourself for brain damage,\nbecause this is an unnatural amount of stupidity."
        else:
            result += "\n...Please seek help..."
        return result

    def DefaultApply(self, srcChar, tgtChar):
        truDmg = ceil( self.damage * (float(srcChar.attack())/tgtChar.defense() ) )
        tgtChar.hp -= truDmg
        if(tgtChar.hp < 0): tgtChar.hp = 0
        return tgtChar.name + " took " + str(truDmg) + " damage!"
    def DefaultHeal(self, srcChar, tgtChar):
        global timesHealedOpponent
        truDmg = self.damage
        tgtChar.hp += truDmg
        if(tgtChar.hp > tgtChar.maxhp()): tgtChar.hp = tgtChar.maxhp()
        result = tgtChar.name + " healed " + str(truDmg) + " damage!"
        if(tgtChar.team != srcChar.team and srcChar.team == playerTeam):
            result = AppendBadMove(result)
        return result
    class Attack:
        #ApplyFunc is the function that provides the actual calculation for damage. This can be used for
        def __init__(self, name, damage, cost = 0, lvlReqs = 0, img_id ="explosion", sfx_path = "mod/sfx/boom.wav", icon_path = "mod/icons/knife.png", ApplyFunc = DefaultApply, preferredForTeam=False,overrideTransform = None):
            self.name = name
            self.damage = damage
            self.preferredForTeam = preferredForTeam
            self.cost = cost
            self.img_id = img_id
            self.sfx_path = sfx_path
            self.icon_path = icon_path
            self.lvlReqs = lvlReqs
            self.ApplyFunc = ApplyFunc
            self.overrideTransform = overrideTransform



        def Apply(self, srcChar, tgtChar):
            global ui_text
            if(self.overrideTransform != None):
                atkFxTransform = self.overrideTransform
            else:
                atkFxTransform = Transform(xoffset = tgtChar.posX, yoffset = tgtChar.posY )
            renpy.show(self.img_id, at_list = [atkFxTransform], layer = "overlay")
            renpy.sound.play(self.sfx_path)
            srcChar.mp -= self.cost
            if(srcChar.mp < 0): srcChar.mp = 0

            ui_text = self.ApplyFunc(self, srcChar, tgtChar)
            _history_list.append( HistoryEntry(what = ui_text) )


    #TODO get some better level system going instead of this static shit
    def GetLevelFromXP(xp):
        return (xp / 200) + 1

    def GetXPFromLevel(lvl):
        return (lvl-1) * 200
    class BattleCharacter:
        #the first atk in atk list will be your default attack.
        def lvl(self):
            return GetLevelFromXP(self.xp)
        def maxhp(self):
            return 10 + 3*self.lvl() + self.hp_bonus
        def maxmp(self):
            return 5 + 2*self.lvl() + self.mp_bonus
        def attack(self):
            return 5 + 2*self.lvl() + self.atk_bonus
        def defense(self):
            return 4 + 2*self.lvl() + self.def_bonus
        def speed(self):
            return self.lvl() + self.spd_bonus

        def __init__(self, name, team, lvl, insane, hp_bonus, atk_bonus, def_bonus, spd_bonus, atk_list, resist_bonus = 0, fxFlags = 0, mp_bonus = 0, img_id= "y_sticker"):
            self.name = name
            self.hash = ""  #auto assigned on battle start, but needs to be defined anyways
            self.team = team
            self.xp = GetXPFromLevel(lvl)
            self.insane = insane
            self.hp_bonus = hp_bonus
            self.mp_bonus = mp_bonus
            self.atk_bonus = atk_bonus
            self.def_bonus = def_bonus
            self.spd_bonus = spd_bonus
            self.resist_bonus = resist_bonus
            self.hp = 10 + 3 * self.lvl() + hp_bonus
            self.mp = 5 + 2 * self.lvl() + mp_bonus
            self.resist = resist_bonus
            self.atk_list = atk_list
            self.effect = fxFlags
            self.img_id = img_id
            self.posX = 0
            self.posY = 0


            # fxFlags : 1 = undead          (regain full hp but also gain insanity)
            #           2 = glitch          (unable to be hit by status ailments)
            #           4 = stun            (unable to take turns)
            #           8 = slowed          (speed/2)
            #           16 = poison         (lose hp)
            #           32 = bleed          (lose hp)
            #           64 = blind          (lowered accuracy)





    def CheckAliveState():
        global characters
        availableNames = set()
        for c in characters:
            if( c.hp > 0 ):
                availableNames.add(c.team)
        if(playerTeam not in availableNames):
            #lose
            return -1
        elif ( len(availableNames) == 1 ):
            #win
            return 1
        else: return 0
    def srtcmp(x,y):
        if (x.speed()/2 if (x.effect & 8 > 0) else x.speed()) <= (y.speed()/2 if (y.effect & 8 > 0) else y.speed()):
            return -1
        else:
            return 1

    def StartRound():
        global characters
        global characterOrder
        global current_state
        global lastBattleWon

        r = CheckAliveState()
        if(r == 0):
            characterOrder = list(characters)
            characterOrder.sort(cmp=lambda x,y: srtcmp(x,y))

        elif (r == 1):
            EndBattle()
            lastBattleWon = True
            renpy.return_statement()
            return
        elif (r == -1):
            EndBattle()
            lastBattleWon = False
            renpy.return_statement()
            return


    def StartCharTurn():
        global characters
        global characterOrder
        global currentCharacter
        global current_state
        global turnStart
        global ui_text
        #restart round if necessary

        turnStart = True



        current_state = battlestate_startturn
        currentCharacter = characterOrder.pop()
        ui_text = "It's " +currentCharacter.name+"\'s turn."
        _history_list.append( HistoryEntry(what = ui_text) )

    def GoToAttackPhase():
        global currentCharacter
        global current_state
        global ui_text
        if(currentCharacter.team == playerTeam):
            current_state = battlestate_movSel
            ui_text = "What will you do?"
        else:
            current_state = battlestate_text
            AIDoTurn(character = currentCharacter)

    charToRemove = None
    def EndTurn():
        global characters
        global characterOrder
        global currentCharacter
        global current_state
        global turnStart
        global ui_text
        global lastBattleWon

        global charToRemove

        if (not charToRemove is None):
            xp = 300
            ui_text = "Gained " + str(xp) + "XP!"
            _history_list.append( HistoryEntry(what = ui_text) )
            for c in characters:
                if(c.team != charToRemove.team):
                    c.xp += xp
                else:
                    c.insane += 10
            charToRemove = None
            return

        for c in characters:
            if c.hp <= 0:
                renpy.hide(c.hash)
                ui_text = c.name + " has died!"
                _history_list.append( HistoryEntry(what = ui_text) )
                charToRemove = c
                break

        if(not charToRemove is None):
            characters.remove(charToRemove)
            if(characterOrder.count(c) > 0):
                characterOrder.remove(charToRemove)
            return

        r = CheckAliveState()
        if(r == 1):
            EndBattle()
            lastBattleWon = True
            renpy.return_statement()
            return
        elif (r == -1):
            EndBattle()
            lastBattleWon = False
            renpy.return_statement()
            return

        if (len(characterOrder) <= 0):
            StartRound()

        StartCharTurn()


    def AIDoTurn(character):
        global characters
        global characterOrder
        global current_state
        global ui_text
        global currentCharacter
        global selectedMove
        global targetCharacter
        # pick a move from the action list
        selectedMove = random.choice(character.atk_list)
        if(selectedMove.preferredForTeam == True): #do we want to cas
            targetCharacter = character
        else:
            # pick a random enemy team character, and act upon it.
            enemies = filter(lambda x: x.team != character.team, characters)
            targetCharacter = random.choice( enemies )
        current_state = battlestate_execAtk
        currentCharacter = character
        ui_text = character.name + " used " + selectedMove.name
        _history_list.append( HistoryEntry(what = ui_text) )

    def StartBattle(initialChars):
        global characters
        global characterOrder
        global currentCharacter
        global selectedMove
        global targetCharacter
        global current_state
        global ui_text
        global turnStart
        #get some random enemies
        characters = filter( lambda c: c.hp > 0, initialChars)
        for i, c in enumerate(characters):
            c.hash = str(i)

        current_state = battlestate_text
        StartRound()
        StartCharTurn()
        #game loop


        while True:
            playerChars = filter(lambda x: x.team == playerTeam, characters)
            enemyChars = filter(lambda x: x.team != playerTeam, characters)
            loop = 0
            sb = 105
            halfLen = len(playerChars) * sb
            for c in playerChars:
                lowerTransform = Transform(xalign = 0.5, yalign = 1.0, xanchor = 0.5, yanchor = 1.0, xoffset = sb + sb*loop*2 - halfLen, yoffset = -75 )
                higherTransform = Transform(xalign = 0.5, yalign = 1.0, xanchor = 0.5, yanchor = 1.0, xoffset = sb + sb*loop*2 - halfLen, yoffset = -150)
                c.posX = sb + sb*loop*2 - halfLen

                if(c == currentCharacter):
                    #ui.image("gui/poemgame/y_sticker_cut_1.png", xalign = 0.5, yanchor = 1.0, transform = hop)
                    if(turnStart == True):
                        renpy.show(c.img_id+" hop",layer = 'transient', tag = c.hash, at_list=[higherTransform], zorder = 0)
                    else:
                        renpy.show(c.img_id,layer = 'transient', tag = c.hash, at_list=[higherTransform],zorder = 0)
                    c.posY = 360-225
                else:
                    renpy.show(c.img_id,layer = 'transient', tag = c.hash, at_list=[lowerTransform],zorder = 0)
                    c.posY = 360-150
                loop += 1
            loop = 0
            halfLen = len(enemyChars) * sb
            for c in enemyChars:
                myTransform = Transform(xalign = 0.5, xanchor = 0.5, xoffset = sb + sb*loop*2 - halfLen )
                c.posX =  sb + sb*loop*2 - halfLen
                c.posY = -100
                renpy.show(c.img_id, tag = c.hash, at_list=[myTransform])
                loop += 1

            t = ui.interact()

            if not t is None:
                if(current_state == battlestate_startturn):
                    if(t == 0):
                        turnStart = False
                        GoToAttackPhase()
                elif(current_state == battlestate_text):
                    if(t == 0):
                        #continue state
                        StartCharTurn()
                elif(current_state == battlestate_movSel):
                    selectedMove = t
                    if(t.cost <= currentCharacter.mp):
                        current_state = battlestate_tgtSel
                elif (current_state == battlestate_tgtSel):
                    if(t == -1):
                        current_state = battlestate_movSel
                    else:
                        targetCharacter = t
                        current_state = battlestate_execAtk
                        ui_text = currentCharacter.name + " used " + selectedMove.name
                        _history_list.append( HistoryEntry(what = ui_text) )
                elif (current_state == battlestate_execAtk):
                    if(t == 0):
                        selectedMove.Apply(currentCharacter, targetCharacter)
                        current_state = battlestate_atkDone
                elif (current_state == battlestate_atkDone or current_state == battlestate_endTurn):
                    if(t == 0):
                        current_state = battlestate_endTurn
                        EndTurn()

    def EndBattle():
        global characters
        for c in characters:
            renpy.hide(c.name);
        renpy.hide_screen("battle_ui")

label TrueBattle(characters, bgi=None, tune=None):
    window hide
    show screen battle_ui
    # show screen quick_menu
    if(bgi != None):
        $ renpy.show(bgi)
    if(tune != None):
        play music tune
    $ StartBattle(characters)
    return

# goes to a certain bit of dialog if necessary
label PreBattle(filename, characters, bgi=None, tune=None):
    if(bgi != None):
        $ renpy.show(bgi)
    python:
        #check against several values to check certain things
        dialogLabel = None
        if(filename.endswith(".php") and not persistent.hasSeenPHPRant and (cidm in availableCharacters.keys())):
            dialogLabel = "php_PreBattle"
        else:
            needsFirstBattle = False;
            for i,v in availableCharacters.iteritems():
                if(not v.hasSeenBattles):
                    needsFirstBattle = True;
                    dialogLabel = "firstBattle"
                    break
            if (not needsFirstBattle and random.randrange(5) == 0):
                # check the availability of certain characters
                dialogLabel = "s_TestPreBattle"
                pass
        #possibility for later hard override, if we need to check a certain dialog
        if(config.developer):
            pass
        if dialogLabel != None: renpy.call(dialogLabel)
    hide sayori
    hide yuri
    hide natsuki
    hide monika
    return

label PostBattle(filename, characters, bgi=None, tune=None):
    python:
        if(lastBattleWon):
            if(filename.endswith(".php") and not persistent.hasSeenPHPRant and (cidm in availableCharacters.keys())):
                renpy.call("php_PostBattle")
                renpy.return_statement();
            forId = GetAssocFromFileName(filename)
            if  (forId == cids):
                if(not DoesFileContainBulli(filename)):
                    persistent.s_satisfaction += 0.1
                else:
                    # comment on bulli
                    if len(availableCharacters.keys()) == 1:
                        persistent.s_satisfaction += 0.05
                    else:
                        while forId == cids:
                            forId = random.choice(availableCharacters.keys())
            if(forId == cidy):
                persistent.y_satisfaction += 0.1
            elif(forId == cidm):
                persistent.m_satisfaction += 0.1
            elif(forId == cidn):
                persistent.n_satisfaction += 0.1

        else:
            pass
    return

label Battle(filename, characters, bgi=None, tune=None):
    call PreBattle(filename, characters, bgi, tune) from _call_PreBattle
    call TrueBattle(characters, bgi, tune) from _call_TrueBattle
    call PostBattle(filename, characters, bgi, tune) from _call_PostBattle
    return

label TestBattle:
    "Hey, wanna do a test battle?"
    "Let's do a test battle"
    python:
        test1 = BattleCharacter(
        name = "Monkia",
        team = playerteam,
        lvl = 25,
        insane = 0,
        hp_bonus = 20,
        atk_bonus = 20,
        def_bonus = 20,
        spd_bonus = 20,
        resist_bonus = 20,
        atk_list = [ atk_spark, atk_glitch ],
        img_id="mod_m_sticker"
        )
        test2 = BattleCharacter(
        name = "Yaoi",
        team = playerteam,
        lvl = 25,
        insane = 1,
        hp_bonus = 20,
        atk_bonus = 20,
        def_bonus = 20,
        spd_bonus = 20,
        resist_bonus = 20,
        atk_list = [ atk_stab, atk_shank ],
        fxFlags = 2,
        img_id="mod_y_sticker"
        )
        testloli = BattleCharacter(
            name = "Nutsucci",
            team = playerTeam,
            lvl = 25,
            insane = 1,
            hp_bonus = 20,
            atk_bonus = 20,
            def_bonus = 20,
            spd_bonus = 20,
            resist_bonus = 20,
            atk_list = [ atk_pan, atk_bake, atk_souffle ],
            fxFlags = 2,
            img_id="mod_n_sticker"
        )
        test5 = BattleCharacter(
        name = "Sayonara",
        team = playerteam,
        lvl = 25,
        insane = 1,
        hp_bonus = 20,
        atk_bonus = 20,
        def_bonus = 20,
        spd_bonus = 20,
        resist_bonus = 20,
        atk_list = [ atk_whip, atk_lasso ],
        fxFlags = 2,
        img_id="mod_s_sticker"
        )

        test3 = BattleCharacter(
        name = "Bulli",
        team = "Team Sludge",
        lvl = 24,
        insane = 1,
        hp_bonus = 20,
        atk_bonus = 20,
        def_bonus = 20,
        spd_bonus = 20,
        resist_bonus = 20,
        atk_list = [ Attack( name = "Strangle",  damage = 15 ), Attack( name = "Bind",  damage = 20, cost = 0 )],
        img_id = "noose"
        )

        test4 = BattleCharacter(
        name = "Hand",
        team = "Team Sludge",
        lvl = 24,
        insane = 1,
        hp_bonus = 20,
        atk_bonus = 20,
        def_bonus = 20,
        spd_bonus = 20,
        resist_bonus = 20,
        atk_list = [ Attack( name = "Slap",  damage = 20 ), Attack( name = "Pinch",  damage = 15, cost = 0 )],
        img_id = "hand"
        )
        test6 = BattleCharacter(
        name = "Hand A",
        team = "Team Sludge",
        lvl = 24,
        insane = 1,
        hp_bonus = 20,
        atk_bonus = 20,
        def_bonus = 20,
        spd_bonus = 20,
        resist_bonus = 20,
        atk_list = [ Attack( name = "Slap",  damage = 20 ), Attack( name = "Pinch",  damage = 15, cost = 0 )],
        img_id = "hand"
        )
        test7 = BattleCharacter(
        name = "Hand B",
        team = "Team Sludge",
        lvl = 24,
        insane = 1,
        hp_bonus = 20,
        atk_bonus = 20,
        def_bonus = 20,
        spd_bonus = 20,
        resist_bonus = 20,
        atk_list = [ Attack( name = "Slap",  damage = 20 ), Attack( name = "Pinch",  damage = 15, cost = 0 )],
        img_id = "hand"
        )

    call TrueBattle( [test1,test2,test3,test4,test5,testloli], "monika_room", "mod/peppersteak.ogg" ) from _call_Battle

    "Hey wanna do another testbattle?"
    "Boom!"

    call TrueBattle( [test1,test2,test6,test7,test5,testloli], "monika_room", "mod/peppersteak.ogg" ) from _call_Battle_1

    "Wow! You are really good at killing stuff!"

    return

label testVictory:
    "You won!"
    return

label testDefeat:
    "You lost!"
    return
