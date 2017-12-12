init python:
    def ReturnEnemies(charAmount, avgLvl):
        noose = BattleCharacter(
        name = "Noose",
        team = "Team Sludge",
        lvl = avgLvl,
        insane = 1,
        hp_bonus = 0,
        atk_bonus = 0,
        def_bonus = 0,
        spd_bonus = 0,
        resist_bonus = 0,
        atk_list = [ Attack( name = "Strangle",  damage = 15 ), Attack( name = "Bind",  damage = 20, cost = 0 )],
        img_id = "noose"
        )

        nooseA = BattleCharacter(
        name = "Noose A",
        team = "Team Sludge",
        lvl = avgLvl,
        insane = 1,
        hp_bonus = 5,
        atk_bonus = 0,
        def_bonus = 5,
        spd_bonus = 0,
        resist_bonus = 0,
        atk_list = [ Attack( name = "Strangle",  damage = 15 ), Attack( name = "Bind",  damage = 20, cost = 0 )],
        img_id = "noose"
        )
        nooseB = BattleCharacter(
        name = "Noose B",
        team = "Team Sludge",
        lvl = avgLvl,
        insane = 1,
        hp_bonus = 0,
        atk_bonus = 5,
        def_bonus = 0,
        spd_bonus = 5,
        resist_bonus = 0,
        atk_list = [ Attack( name = "Strangle",  damage = 15 ), Attack( name = "Bind",  damage = 20, cost = 0 )],
        img_id = "noose"
        )
        nooseC = BattleCharacter(
        name = "Noose C",
        team = "Team Sludge",
        lvl = avgLvl,
        insane = 1,
        hp_bonus = 0,
        atk_bonus = 0,
        def_bonus = 5,
        spd_bonus = 5,
        resist_bonus = 0,
        atk_list = [ Attack( name = "Strangle",  damage = 15 ), Attack( name = "Bind",  damage = 20, cost = 0 )],
        img_id = "noose"
        )

        handyman = BattleCharacter(
        name = "Hand",
        team = "Team Sludge",
        lvl = avgLvl,
        insane = 1,
        hp_bonus = 0,
        atk_bonus = 0,
        def_bonus = 0,
        spd_bonus = 0,
        resist_bonus = 0,
        atk_list = [ Attack( name = "Slap",  damage = 20 ), Attack( name = "Pinch",  damage = 15, cost = 0 )],
        img_id = "hand"
        )

        handymanA = BattleCharacter(
        name = "Hand",
        team = "Team Sludge",
        lvl = avgLvl,
        insane = 1,
        hp_bonus = 5,
        atk_bonus = 5,
        def_bonus = 0,
        spd_bonus = 0,
        resist_bonus = 0,
        atk_list = [ Attack( name = "Slap",  damage = 20 ), Attack( name = "Pinch",  damage = 15, cost = 0 )],
        img_id = "hand"
        )
        handymanB = BattleCharacter(
        name = "Hand B",
        team = "Team Sludge",
        lvl = avgLvl,
        insane = 1,
        hp_bonus = 0,
        atk_bonus = 5,
        def_bonus = 5,
        spd_bonus = 0,
        resist_bonus = 0,
        atk_list = [ Attack( name = "Slap",  damage = 20 ), Attack( name = "Pinch",  damage = 15, cost = 0 )],
        img_id = "hand"
        )
        handymanC = BattleCharacter(
        name = "Hand C",
        team = "Team Sludge",
        lvl = avgLvl,
        insane = 1,
        hp_bonus = 0,
        atk_bonus = 0,
        def_bonus = 5,
        spd_bonus = 5,
        resist_bonus = 0,
        atk_list = [ Attack( name = "Slap",  damage = 20 ), Attack( name = "Pinch",  damage = 15, cost = 0 )],
        img_id = "hand"
        )

        if(charAmount <= 2):
            val = random.randrange(3)
            if(val == 0):
                return [noose]
            elif (val == 1):
                return [handyman]
            elif (val == 2):
                return [noose, handyman]

        else:
            val = random.randrange(5)
            if(val == 0):
                return [noose, handyman]
            elif (val == 1):
                return [handymanA, handymanB, handymanC]
            elif (val == 2):
                return [noose, handymanA, handymanB]
            elif (val == 3):
                return [nooseA, nooseB, handyman]
            elif (val == 4):
                return [nooseA, nooseB, nooseC]

    def SayoriBoss1(charAmount, avgLvl):
        idunno = BattleCharacter(
            name = "Hoosand",
            team = "Team Sludge",
            lvl = avgLvl,
            insane = 1,
            hp_bonus = 5 + 5*charAmount,
            atk_bonus = 5*charAmount,
            def_bonus = 4*charAmount,
            spd_bonus = 6*charAmount,
            resist_bonus = 0,
            atk_list = [
                Attack( name = "Slap",  damage = 11 ),
                Attack( name = "Pinch",  damage = 7, cost = 0 ),
                Attack( name = "Strangle",  damage = 13 ),
                Attack( name = "Constrict",  damage = 17, cost = 0 ),
                Attack( name = "Loosen up",  damage = 21, cost = 0, preferredForTeam=True, ApplyFunc=DefaultHeal),
                ],
            img_id = "hoosand"
        )
        return [idunno]



init python:
    curAngle = 0
    def HoosandTransform(st, at):
        curAngle = st * 15
        img = At(LiveComposite(
            (0720,0720),    #for some reason 0720 works, but 720 doesn't? (you can't explain this shit)
            (0,0),At("hand", Transform(xoffset=-170*math.sin(math.radians(0)  ), yoffset=170*math.cos(math.radians(0)),  yalign=0.5, yanchor=0.5,xalign=0.5, xanchor=0.5, rotate=0)),
            (0,0),At("hand", Transform(xoffset=-170*math.sin(math.radians(60)), yoffset=170*math.cos(math.radians(60)),yalign=0.5, yanchor=0.5,xalign=0.5, xanchor=0.5, rotate=60)),
            (0,0),At("hand", Transform(xoffset=-170*math.sin(math.radians(120)), yoffset=170*math.cos(math.radians(120)),yalign=0.5, yanchor=0.5,xalign=0.5, xanchor=0.5, rotate=120)),
            (0,0),At("hand", Transform(xoffset=-170*math.sin(math.radians(180)), yoffset=170*math.cos(math.radians(180)),yalign=0.5, yanchor=0.5,xalign=0.5, xanchor=0.5, rotate=180)),
            (0,0),At("hand", Transform(xoffset=-170*math.sin(math.radians(240)), yoffset=170*math.cos(math.radians(240)),yalign=0.5, yanchor=0.5,xalign=0.5, xanchor=0.5, rotate=240)),
            (0,0),At("hand", Transform(xoffset=-170*math.sin(math.radians(300)), yoffset=170*math.cos(math.radians(300)),yalign=0.5, yanchor=0.5,xalign=0.5, xanchor=0.5, rotate=300)),
        ),Transform(xalign = 0.5, yalign=0.5, xanchor = 0.5, yanchor = 0.5, rotate= curAngle))
        return img, 0.01


image hoosand:
    truecenter
    subpixel  False
    DynamicDisplayable(HoosandTransform)

label testBoss:
    "Here have boss"
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
        atk_list = [ Attack( name = "Spark",  damage = 15 ), Attack( name = "Glitch",  damage = 40, cost = 25 )],
        img_id="m_sticker"
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
        atk_list = [ Attack( name = "Unstab", damage = 20,icon_path = "mod/icons/heal.png",ApplyFunc=DefaultHeal ), Attack( name = "Insanity",  damage = 40, cost = 25 )],
        fxFlags = 2,
        )
        chars = [test1, test2] + SayoriBoss1(2,2)
    call Battle("", chars, "monika_room", "mod/testboss.mp3" )
    "gg no re"
