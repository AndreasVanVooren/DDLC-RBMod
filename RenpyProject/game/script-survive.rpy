
screen survive_ui:
    id "survive_ui"
    window:
        id "Surufaiffu"
        style "window_Null"
        grid 4 4 spacing -10 xalign 1.0 yalign 0.5 xoffset -100:
            style_prefix "slot"
            for i in range(16):
                if( i < len(game_files) ):
                    #hard coded values because of course
                    $ path = GetBGIDFromFileName(game_files[i])
                    button action Return(game_files[i]) xsize 180 ysize 136:
                        has fixed xsize 160 ysize 90
                        add path size (160, 90)xalign 0.5

                        text game_files[i] style "slot_time_text" xalign 0.5 yalign 1.0
                else:
                    button action () xalign 0.5 yalign 0.0 xsize 180 ysize 136:
                        has fixed xsize 160 ysize 90

                        text "null" style "slot_time_text" xalign 0.5 yalign 1.0



init python:
    global game_files
    global selectedFile
    surviveStarted =  False

    stest1 = BattleCharacter(
    name = "Monkia",
    team = playerteam,
    lvl = 25,
    insane = 0,
    hp_bonus = 20,
    atk_bonus = 20,
    def_bonus = 20,
    spd_bonus = 20,
    resist_bonus = 20,
    atk_list = [ Attack( name = "Spark", damage = 15 ), Attack( name = "Glitch", damage = 40, cost = 25 )],
    img_id="m_sticker"
    )
    stest2 = BattleCharacter(
    name = "Yaoi",
    team = playerteam,
    lvl = 25,
    insane = 1,
    hp_bonus = 20,
    atk_bonus = 20,
    def_bonus = 20,
    spd_bonus = 20,
    resist_bonus = 20,
    atk_list = [ Attack( name = "Unstab", damage = 20, ApplyFunc=DefaultHeal, icon_path = "mod/icons/heal.png" ), Attack( name = "Insanity", damage = 40, cost = 25 )],
    fxFlags = 2,
    )
    stest3 = BattleCharacter(
    name = "Sayonara",
    team = playerteam,
    lvl = 25,
    insane = 1,
    hp_bonus = 20,
    atk_bonus = 20,
    def_bonus = 20,
    spd_bonus = 20,
    resist_bonus = 20,
    atk_list = [ Attack( name = "Strangle", damage = 15 ), Attack( name = "Bind", damage = 40, cost = 25 )],
    fxFlags = 2,
    img_id="s_sticker"
    )

    def DoesFileContainBulli(f):
        for tag in sayori_negatags:
            if(f.count(tag) > 0):
                return True
        return False

    # keep these functions deterministic, so that we can actually anticipate these things and change behaviour accordingly
    def GetAssocFromFileName(f):
        m_points = s_points = y_points = n_points = 0

        #loop over the extensions, extensions can give points for multiple chars, so we can't break when we've found one
        for ext in sayori_extensions:
            if f.endswith(ext):
                s_points += 10
                break   #minor optimization : a file can only have one extension
        for ext in natsuki_extensions:
            if f.endswith(ext):
                n_points += 10
                break
        for ext in yuri_extensions:
            if f.endswith(ext):
                y_points += 10
                break
        for ext in monika_extensions:
            if f.endswith(ext):
                m_points += 10
                break
        #loop over the tags, ame deal as with extensions
        for tag in sayori_tags:
            count = f.count(tag)
            s_points += count * 3
        for tag in sayori_negatags:
            count = f.count(tag)
            s_points -= count * 3   #TODO events when file contains bulli
        for tag in natsuki_tags:
            count = f.count(tag)
            n_points += count * 3
            s_points += count       #sayori is a god damn happiness leecher
        for tag in monika_tags:
            count = f.count(tag)
            m_points += count * 3
            s_points += count
        for tag in yuri_tags:
            count = f.count(tag)
            y_points += count * 3
            s_points += count

        max_points = max(s_points, y_points, m_points, n_points)
        # max point order check in order of best girl
        if(max_points == 0):    #the file doesn't have any noteworthy tags
            return cid0
        elif(max_points == y_points):
            return cidy
        elif(max_points == s_points):
            return cids
        elif(max_points == n_points):
            return cidn
        elif(max_points == m_points):
            return cidm

    def GetBGPathFromFileName(f):
        returnVal = GetAssocFromFileName(f)
        if(returnVal == cid0):
            arr = null_bgpaths
        elif(returnVal == cids):
            arr = sayori_bgpaths
        elif(returnVal == cidn):
            arr = natsuki_bgpaths
        elif(returnVal == cidm):
            arr = monika_bgpaths
        elif(returnVal == cidy):
            arr = yuri_bgpaths
        rand = hash(f)
        rand %= len(arr)
        return arr[rand]

    def GetBGIDFromFileName(f):
        returnVal = GetAssocFromFileName(f)
        if(returnVal == cid0):
            arr = null_bgids
        elif(returnVal == cids):
            arr = sayori_bgids
        elif(returnVal == cidn):
            arr = natsuki_bgids
        elif(returnVal == cidm):
            arr = monika_bgids
        elif(returnVal == cidy):
            arr = yuri_bgids
        rand = hash(f)
        rand %= len(arr)
        return arr[rand]

    def SurviveLoop():
        global game_files
        global surviveStarted
        # test_files = [ "helloworld.cs", "natsukiisbae.jpg", "sayori.php", "nicebook.pdf", "totallynotavirus.exe", "isgoodhentias.pdf", "Shieet.cpp", "Shieet.txt" ]
        # game_files = test_files #TODO : Replace this with the actual recycle bin get code.
        if not surviveStarted:
            surviveStarted = True
            UpdateFilesInRecycleBin()
            game_files = GetRecycleBinFiles()
            #remove the dokis out of the list, otherwise weird shit might happen
            while(game_files.count("yuri.chr") > 0):
                game_files.remove("yuri.chr")
            while(game_files.count("sayori.chr") > 0):
                game_files.remove("sayori.chr")
            while(game_files.count("monika.chr") > 0):
                game_files.remove("monika.chr")
            while(game_files.count("natsuki.chr") > 0):
                game_files.remove("natsuki.chr")
            game_files = game_files[:16]
        while True:
            t = ui.interact()
            if not t is None:
                SelectFile(t)
                break
    def EndSurvive():
        renpy.hide_screen("survive_ui")
        renpy.jump("TestSurviveEnd")


    def SelectFile(file):
        global game_files
        global selectedFile
        game_files.remove(file)
        selectedFile = file

        renpy.hide_screen("survive_ui")

        charCount = 0
        lvlSum = 0
        charList = []
        for k,v in availableCharacters.iteritems():
            charList.append(v.battlechar)
            lvlSum += v.battlechar.lvl()
            charCount += 1
        charList += ReturnEnemies(charCount, lvlSum/charCount)

        renpy.call("Battle", filename=selectedFile, characters = charList, bgi=GetBGIDFromFileName(selectedFile), tune= "mod/peppersteak.ogg")

# game flow : Dialog -> Survival -> Possible Dialog -> Fights -> Survival -> More dialog
# consume items in recycle bin (TODO: figure out how to)

label Survive(bgi=None, tune = None):
    hide sayori
    hide yuri
    hide monika
    hide natsuki
    window hide
    if(tune != None):
        play music tune
    show screen survive_ui
    $ SurviveLoop()
    if(lastBattleWon):
        if(len(game_files) > 0):
            python:
                for i,c in availableCharacters.iteritems():
                    c.battlechar.hp += 10
                    c.battlechar.mp += 10
                    if c.battlechar.hp > c.battlechar.maxhp():
                        c.battlechar.hp = c.battlechar.maxhp()
                    if c.battlechar.mp > c.battlechar.maxmp():
                        c.battlechar.mp = c.battlechar.maxmp()
            call Survive(bgi, tune) from _call_Survive
            return

        else:
            $ surviveStarted = False
            #jump TestSurviveEnd
            return
    else:
        "That went poorly..."
        $ surviveStarted = False
        #jump TestSurviveEnd
        return

label PostSurvive:
    # TODO Better way of checking this
    if(cidn in availableCharacters.keys()):
        call n_randPainInTheNeck
    return

label TestSurvive:
    "Oh hey looks like you want to survive and shit"
    "You cant you'll die lol"
    call Survive(tune="<loop 0>bgm/m1.ogg") from _call_Survive_1
    return
label TestSurviveEnd:
    "fuck you survived"
    return
