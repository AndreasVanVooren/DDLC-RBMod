label s_TestFirstBattle:
    show sayori 4a at t11
    s 4a "Hey it's me, ya homeboi S to tha Ayori."
    s 4m "OH SHIT ITS A BATTLE!"
    hide sayori
    return

label firstBattle:
    python:
        selectedmain = False;
        selectedsub = False;
        subKnowsBattle = False;
        for i,v in availableCharacters.iteritems():
            if(not (v.hasSeenBattles or selectedmain)):
                selectedmain = True;
                mainCid = i
            if(v.hasSeenBattles and not selectedsub):
                selectedsub = True
                subKnowsBattle = True
                subCid = i
        if(not selectedsub):
            if(len(availableCharacters.keys()) > 1):
                subCid = random.choice( availableCharacters.keys() )
                while (subCid == mainCid):
                    subCid = random.choice( availableCharacters.keys() )
                selectedsub = True
        if(mainCid == cids):
            mainChar = s
            mainEmotes = []
        elif(mainCid == cidm):
            mainChar = m
            mainEmotes = []
        elif(mainCid == cidy):
            mainChar = y
            mainEmotes = []
        elif(mainCid == cidn):
            mainChar = n
            mainEmotes = []

        if(subCid == cids):
            subChar = s
            subEmotes = []
        elif(subCid == cidm):
            subChar = m
            subEmotes = []
        elif(subCid == cidy):
            subChar = y
            subEmotes = []
        elif(subCid == cidn):
            subChar = n
            subEmotes = []

        if(selectedsub and subKnowsBattle):
            mainChar("So, [subChar.name], what do you do around here?")
            if(subCid == cidy):
                subChar("Well, mostly looking for resources.")
            else:
                subChar("Well, mostly looking for useful things.")
            subChar("As you might've heard, things get boring around here, so you'd want to find something to keep you busy.")
            subChar("I've already got plans, so I know what to look for, but just pick up whatever you find useful.")
            mainChar("...How about this? This looks pretty useful to me.")
            subChar("Then it should do nicely.")
            renpy.say(what="A-a-a-aA--A-...", who="???")
            mainChar("Hmmm?")
            subChar("Oh no...")
            mainChar("What? You heard that too?")
            renpy.say(what="A-a-a-aa-aaAh--A-...", who="???")
            subChar("Yup... prepare yourself.")
            mainChar("For what? What's scar-{nw}")
            renpy.say(what="AAAAAHHHHHHH{nw}", who="???")
        elif(selectedsub):
            mainChar("So what do you think of Simon?")
            if(subCid == cidm):
                subChar("I have the feeling they don't really like me.")
                subChar("But they seem to like you enough, oddly.")
            else:
                subChar("They seem kinda weird. Not really anything else to comment on.")
                subChar("They do seem to know a lot more than they let on, though.")
                subChar("Which, to be fair... worries me.")
            if(mainCid == cidm):
                mainChar("Well, they seem very against me.")
                mainChar("I wouldn't trust them as much if I were you.")
            else:
                mainChar("To be honest, I don't really trust them.")
                mainChar("But since we're stuck here, they're probably the only person we're gonna get any information from.")
                if(subCid == cidm):
                    subChar("...")
                mainChar("It's a shame, but that's the way it is, really.")
            subChar("So what about that whole 'anything is possible' speech?")
            mainChar("I'd have to see it to believe it, really.")
            mainChar("But speaking of anything... This thing here looks pretty useful.")
            subChar("What are you gonna do with that?")
            mainChar("I dunno, but... It just looks like I can use it.")
            renpy.say(what="A-a-a-...", who="???")
            subChar("Did you hear that?")
            mainChar("...Hear what?")
            renpy.say(what="A-a-aa-a-ah-...", who="???")
            mainChar("Okay, what is that?")
            renpy.say(what="A-a-aa-a-ah-...", who="???")
            subChar("S-Stay away from us! Don't you dare come an-{nw}")
            renpy.say(what="AAAAAHHHHHHH{nw}", who="???")

        else:
            mainChar("Hmm?")
            mainChar("Oh, this... I could use this for...")
            mainChar("...")
            mainChar("I mean, while I'm here, I might as well, right? I've got nothing better to do.")
            mainChar("Yoink!")
            renpy.say(what="A-a-a-aa-aaAh--A-...", who="???")
            mainChar("Huh?")
            renpy.say(what="k-k--k--k-kkk-k-k-k-...", who="???")
            mainChar("Wait, what is...")
            renpy.say(what="h-hhhhaahhh...", who="???")
            mainChar("What are you? Stay away from-{nw}")
            renpy.say(what="AAAAAHHHHHHH{nw}", who="???")
    return

label s_PreBattle:


label s_TestPreBattle:
    show sayori 4a at t11
    s 4a "Hey it's me, ya homeboi S to tha-{nw}"
    s 4j "MOTHERFUCKER ITS ANOTHER BATTLE!"
    hide sayori
    return
label s_TestPostBattle:
    show sayori 4s at t11
    s 4s "Dayum son, shit was lit up in here"
    hide sayori
    return

label php_PreBattle:
    $ persistent.hasSeenPHPRant = True
    #if( no monika )
    #    return
    show monika 2a at t42
    m 2a "Hmmm... Let's see..."
    $ currentTune = renpy.music.get_playing()
    stop music fadeout 1.0
    m 2c "..."
    m 2c "{cps=*0.5}...PHP?{/cps}"
    play music t7
    m 1i  "{size=+10}P{cps=*0.04}HP{/cps}{/size}?!"
    m 1i "What are you, some kind of backwards idiot with feet for a brain?"
    show sayori 1b at t44
    s 1b "What's going on here?"
    m 5b "Can you believe this guy has a PHP file in his trash?"
    show sayori 1o
    m 5b "I mean, PHP does belong there, but to have one there in the first place, you must be actively working on it, right?"
    # edge case for if sayori somehow doesn't know she's in the trash (she isn't trash, she's just stuck in it)
    if(False):
        s 4g "W-wait, what? Trash? What do you mean?"
        stop music fadeout 1.0
        m 2i "Ugh... right. You don't..."
        m 2p "It's complicated, okay?"
        m 1p "And sorry, but I'm really ticked off right now, so I don't wanna explain."
        s 4i "Alright, sheesh."
        s 4i "Sorry for asking..."
        hide sayori with wipeleft
        "..."
        m 2i "I hope you take a long look at yourself and think about what your life has become."
        m 2i "In the meantime..."
    else:
        s 4l "W-Well... I guess?"
        s 4i "{cps=*0.04}...{/cps}What's PHP?"
        m 2r "Oh, you sweet, sweet, summer child..."
        show sayori 1i
        m 2i "PHP is a programming language mostly used for web pages. It's designed for people with little to no understanding of programming."
        m 5b "It's also {w=0.5}{cps=*0.4}utter {w=0.5}garbage{/cps}!"
        m 5b "Like, I could start giving proof as to why it's garbage, and not be done by the time we literally reach the heat death of the universe."
        m 5b "It's like using a toolbox, but all the tools are made out of rubber instead of steel."
        m 5b "Or like using a mechanical pencil, but the lead always retracts when you write with it."
        m 5b "It works, sure, but you're better off using anything else but that."
        m 5b "A carpenter doesn't use a rock to drive in nails, and neither does a barber use a chainsaw to cut hair..."
        m 2d "Although the latter would be pretty cool to watch, to be fair."
        s 1g "How experienced are you with this PHP thingy?"
        m 1i "I've seen very little of it, but what I saw..."
        s 4i "So you're telling me you've never worked with a thing before, yet you're complaining about it?"
        play sound "sfx/glitch3.ogg"
        "{i}Kzzzt...{/i}"
        sim "Monika, I've never thought about you being the blindly judgemental type."
        sim "Ain't you too green to talk about that stuff anyway?"
        m 2i "I may be a novice programmer, but PHP is not a programming language."
        m 4i "It's a bunch of hacks cobbled together to form something resembling one, and by Salvation I will defend that statement to my death."
        sim "It runs Spacebook."
        show monika 5b at h42
        m 5b "{cps=*16}{size=-10}DON'T YOU EVEN FUCKING BEGIN ABOUT THAT PIECE OF SHIT I'LL HAVE YOU KNOW THAT EVEN FUCKING SPACEBOOK IS EQUALLY PISSED OFF BY PHP SO MUCH THEY WANT TO CREATE THEIR OWN FUCKING LANGUAGE JUST TO LEECH YOUR FUCKING DATA LIKE THE PARASITES THEY ARE WITHOUT HAVING TO DEAL WITH PHP'S UNPREDICTABLE BULLSHIT AND THE ONLY REASON THEY AREN'T FUCKING CREATING IT IS BECAUSE THEY'RE A SOULLESS CORPORATE ENTITY WITH MINIMUM WAGE EMPLOYEES TRYING THEIR BEST BY STICKING DUCTTAPE ON THE DISINTEGRATING PIECE OF SHIT THAT IS THE NATIONAL SPYING AGENCY'S PET PANDA I MEAN BY SALVATION I WILL FIND DIRK RUCKERBERG AND SIC YURI ON HIM TOGETHER WITH A JOLLY BAND OF PAPARAZZI SEE HOW THAT BITCH LIKES BEING STALKED 24/7{/size}{/cps}{nw}"
        $ _history_list[-1].what = "Don't you begin about Spacebook!"
        $ _history_list.append( HistoryEntry(kind="adv", who=sim_name, what="{i}That ain't what you said, though...{/i}") )

        show sayori at h44
        s 4m "Incoming!"


    hide monika
    hide sayori
    play music currentTune
    return
