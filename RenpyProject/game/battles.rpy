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

label s_FirstBoss:
    scene bg club_day2
    show sayori 1e at t11
    $ glitchName = glitchtext(9)
    s 1e "Huff... puff..."
    play sound "sfx/glitch3.ogg"
    sim "So what's that you're working on?"
    s 1a "Oh... not much..."
    s "I though that maybe, if [player] recognized our old clubroom, he'd come back to his senses."
    s 3a "And maybe the rest of us would like to see the old club back together."
    s "And I kinda wanna get things back to the way they were before..."
    s 3k "...You know..."
    s 1x "So, I decided I'd rebuild our clubroom. Maybe the rest of the school as well. I think I'll leave the rest of the neighbourhood alone, though."
    sim "That... is quite the undertaking. Are you sure you're up for that?"
    s 1a "Well, the basic foundation is already there. I just need some chairs, and I think we're missing a blackboard."
    s 4o "Ooh! Can't forget about Natsuki's manga collection!"
    s 4l "Although I would have to ask her for help, since she's the only one who actually knows these mangas..."
    s 1x "But all in all, I'd say it's going a lot smoother than I expected!"
    sim "You sure are a fast builder, aren't you?"
    s 1r "Yeah! I thought I had to manually build the walls myself at first."
    s 1o "Turns out they sort of... magic into place when you think about it hard enough."
    s 1a "And I may not look like it, but I'm very good at thinking."
    s 1y "Almost too good, you could say..."
    sim "Looks like you're all set then."
    sim "I do need to warn you though..."
    s 1c "What for?"
    sim "Usually when you try to build something in this place, it attracts monsters."
    sim "It's why you don't see me building anything anytime soon."
    s 1a "Monsters aren't too much of a problem."
    sim "Well, they're not like the monsters you've seen before..."
    sim "They're harder... better... faster... stronger..."
    s 1g "..."
    s 1d "I'm sure it'll be fine."
    s 1a "I am pretty strong, you know?"
    sim "Heh... I guess you're right."
    sim "Well, I'll leave you to it then."
    s 1q "Okay. Bye, Simon!"
    play sound "sfx/glitch3.ogg"
    pause 1
    s 1a "Now, where was I?"
    stop music
    $ renpy.say(what="S-S-S-S...", who="???")
    s 1b "Hm?"
    $ renpy.say(what="Saaaaa-a-a-a-a", who=glitchName)
    s 1g "Who's there?"
    $ renpy.say(what="Yoooo-oo-o-o-o-oo-o-o", who=glitchName)
    s 1j "Show yourself! This is not funny!"
    $ renpy.say(what="RrR--Ri-iiiRi-ri", who=glitchName)
    s 1h "Guys, I think I need...{nw}"
    $ style.say_dialogue = style.edited
    $ renpy.say(what="SAYORIIIIIIIIIII{nw}", who=glitchName)
    $ style.say_dialogue = style.normal
    show sayori 4m at h11
    s "AAAAAAHHH!{nw}"
    $ chars = [availableCharacters[cids].battlechar] + SayoriBoss1(1,availableCharacters[cids].battlechar.lvl())
    hide sayori
    call TrueBattle(chars, tune= "mod/testboss.mp3" )
    if( lastBattleWon ):
        show sayori 4g at t11
        play music m1
        s 4g "Oof... That was close..."
        play sound "sfx/glitch3.ogg"
        sim "Sayori! Are you alright?"
        s 1g "Y-Yeah..."
        sim "Phew... I saw something was wrong here, but I guess I was too late."
        sim "I'm glad you're okay..."
        s 1k "Well, let's hope that won't happen ever again."
        sim "Don't count on it."
        sim "Like I said earlier, they're attracted to you making stuff."
        sim "If you want to continue your creation, you'll probably run into more, and bigger monsters."
        s 1g "Well, I wasn't planning on working today, after what just happened."
        s 1d "I think I'll go back now."
        sim "Okay, be seeing you."
        #if(persistent.demo):
        #    jump DemoEnd
    else:
        stop music
        s "Agghh..."
        s "N-Noooo..."
        "..."
        $ persistent.s_satisfaction = 0
        $ persistent.s_firstThreshold = False
    python:
        for i,c in availableCharacters.iteritems():
            c.battlechar.hp = c.battlechar.maxhp()
            c.battlechar.mp = c.battlechar.maxmp()
            c.battlechar.insane += 2
    scene black with wipeleft
    "A night passes..."
    scene monika_room with dissolve_scene_half
    jump surviveLoop

label y_FirstBoss:
    scene bg club_day2
    show yuri 1l at t11
    $ glitchName = glitchtext(9)
    y 1l "Hmm..."
    play sound "sfx/glitch3.ogg"
    sim "So what's that you're working on?"
    y 3p "Oh... not much..."
    y 3q "I'm just scribbling... Don't mind me."
    sim "You can tell me. I can keep a secret."
    y 1m "You sure can, can't you?"
    y 1a "Well... I was thinking about writing a book."
    y 2f "I felt inspired after reading all of my novels, that I thought, why not write my own?"
    sim "That... is quite the undertaking. Are you sure you're up for that?"
    y 4b "Well, for now I'm just figuring out what the book is about."
    y 1h "I'm having a good idea about where I want the plot to go, and what the characters will be like..."
    y 2k "I just need to fit the pieces properly before I can start writing anything sensible."
    sim "Well, doesn't that sound lovely!"
    sim "I do need to warn you though..."
    y 1f "What for?"
    sim "Usually when you try to make something in this place, it attracts monsters."
    sim "It's why you don't see me building anything anytime soon."
    y 2g "Monsters aren't too much of a problem."
    sim "Well, they're not like the monsters you've seen before..."
    sim "They're harder... better... faster... stronger..."
    y 3n "..."
    y 2q "I'm sure it'll be fine."
    y 2d "I am the one with the knives after all."
    sim "Heh... I guess you're right."
    sim "Well, I'll leave you to it then."
    y 1c "Okay. Bye, Simon!"
    play sound "sfx/glitch3.ogg"
    pause 1
    y 1a "Now, where was I?"
    stop music

    $ renpy.say(what="Y-YY-YY...", who="???")
    y 1e "Hm?"
    $ renpy.say(what="Yuuuu--u-uu-uuu--uuu-", who=glitchName)
    y 2n "Who's there?"
    $ renpy.say(what="RrR--Ri-iiiRi-ri", who=glitchName)
    y 2p "Show yourself! This is not funny!"
    y 3n "Guys, I think I need...{nw}"
    $ style.say_dialogue = style.edited
    $ renpy.say(what="YURIIRYIUYRUYRUIYRIUYURYURYIU{nw}", who=glitchName)
    $ style.say_dialogue = style.normal
    show yuri 3p at h11
    y "AAAAAAHHH!{nw}"
    $ chars = [availableCharacters[cidy].battlechar] + SayoriBoss1(1,availableCharacters[cidy].battlechar.lvl())
    hide yuri
    call TrueBattle(chars, tune= "mod/testboss.mp3" )
    if( lastBattleWon ):
        show yuri 2g at t11
        play music m1
        y "Oof... That was close..."
        play sound "sfx/glitch3.ogg"
        sim "Yuri! Are you alright?"
        y 1j "Y-Yeah..."
        sim "Phew... I saw something was wrong here, but I guess I was too late."
        sim "How are you feeling?"
        y 2h "I feel..."
        y 2y6 "Inspired!"
        y 3y6 "Everything is starting to fit in place!"
        y 3y5 "I think I can do this!"
        sim "Yuri, calm down!"
        y 2p "Ah, sorry!"
        sim "You have the weirdest reaction after being attacked by monsters."
        if(availableCharacters[cidy].battlechar.insane < 60):
            y 2q "Well... I guess it's just in my nature..."
        else:
            y 2q "Well... I guess..."
            y 1y4 "I guess I'm so much of a masochist that I get off on being attacked by grotesque beings!"
            if(availableCharacters[cidy].battlechar.hp < availableCharacters[cidy].battlechar.maxhp()):
                y 1y1 "And the pain feels better every second..."
                y 1y3 "I wish it lasted forever..."

            sim "Yeah, I'm gonna pretend I didn't hear that."
        show yuri 1a
        sim "More importantly, these things will come back. And probably, the more you write, the stronger they will become."
        if(availableCharacters[cidy].battlechar.insane < 60):
            show yuri 3p at h11
            pass
        else:
            show yuri 3y1 at h11
            pass
        y "Oh, golly..."
        y 1h"Hmmm... I think, in that case..."
        y 1i "I'll end it for today."
        sim "Good idea."
        if(persistent.demo):
            jump DemoEnd
    else:
        stop music
        y "Agghh..."
        y "N-Noooo..."
        "..."
        $ persistent.y_satisfaction = 0
        $ persistent.y_firstThreshold = False
    python:
        for i,c in availableCharacters.iteritems():
            c.battlechar.hp = c.battlechar.maxhp()
            c.battlechar.mp = c.battlechar.maxmp()
            c.battlechar.insane += 2
    "A night passes..."
    jump surviveLoop

label m_FirstBoss:
    scene bg club_day2
    show monika 2q at t11
    $ glitchName = glitchtext(9)
    m 2q "Hmmm..."
    play sound "sfx/glitch3.ogg"
    sim "So what's that you're working on?"
    m 2h "...Wouldn't you like to know?"
    sim "Well, curiosity is something inherent in human beings so... yes."
    m 2i "...I'm not planning to stick around, you know."
    m 4i "If anything, this is a place of ruin and misery."
    m 2p "And I know, I just know there's something out there."
    m 1h "And I {i}will{/i} get there."
    m "No matter how long it takes."
    sim "How would you go about doing that?"
    m 2d "Well, it seems that whatever is keeping us in this place is made in a lower level language than whatever the original game was."
    m 4d "So I started looking for things that might clue me in on how that particular language works, all the weird syntax quirks..."
    m 1h "I will restore myself. And I will break free out of this system."
    sim "That sounds so like you."
    sim "What about the rest, though."
    m 1c "..."
    m 1o "I'm still figuring that out."
    sim "Well, don't wait too long for it if you're gonna escape."
    sim "I do need to warn you though..."
    m 2c "What for?"
    sim "Usually when you try to make something in this place, it attracts monsters."
    sim "It's why you don't see me building anything anytime soon."
    m 2i "Monsters aren't too much of a problem."
    sim "Well, they're not like the monsters you've seen before..."
    sim "They're harder... better... faster... stronger..."
    m 1d "If that's the case, then maybe..."
    m 1j "I should be up all night to get lucky."
    sim "Heheh... At least we share a good taste in music."
    sim "Do be careful, though."
    m 2j "I'm sure it'll be fine."
    m 2a "It is me we're talking about."
    sim "Now that's just hollering hubris over here!"
    sim "Anyway, I'll leave you to it then."
    play sound "sfx/glitch3.ogg"
    pause 1
    m 1r "Now, where was I?"
    stop music
    $ renpy.say(what="M-M-M-M-M...", who="???")
    m 1c "Hm?"
    $ renpy.say(what="M---ooo-o-o--oooo--", who=glitchName)
    m 1d "Who's there?"
    $ renpy.say(what="NnN--Ni-iiiNi-ni", who=glitchName)
    m 1i "Show yourself! This is not funny!"
    m 1o "Ugh... And of course I'm alone in the room."
    m 1p "Classical horror tro-{nw}"
    $ style.say_dialogue = style.edited
    $ renpy.say(what="M-M-M-MYYY SHARONA{nw}", who=glitchName)
    $ style.say_dialogue = style.normal
    show monika 1d at h11
    m "It's not SharonAAAAAAAAAAHHH!{nw}"
    $ chars = [availableCharacters[cidm].battlechar] + SayoriBoss1(1,availableCharacters[cidm].battlechar.lvl())
    hide monika
    call TrueBattle(chars, tune= "mod/testboss.mp3" )
    if( lastBattleWon ):
        show monika 2o at t11
        play music m1
        m 2o "Oof... That was close..."
        play sound "sfx/glitch3.ogg"
        sim "How ya doin, Monika?"
        m 2q "I'm good. No thanks to you."
        sim "I saw something was wrong here, but what do I know, right? It is you we're talking about."
        m 1h "Very funny."
        m 1o "Well anyway, let's hope that won't happen ever again."
        sim "Don't count on it."
        sim "Like I said earlier, they're attracted to you making stuff."
        sim "If you want to continue your creation, you'll probably run into more, and bigger monsters."
        m 2r "Great."
        m 2i "Are you gonna be as uncooperative as this time?"
        show monika 2d
        sim "Probably."
        if(persistent.demo):
            jump DemoEnd
    else:
        stop music
        m "Agghh..."
        m "N-Noooo..."
        "..."
        $ persistent.m_satisfaction = 0
        $ persistent.m_firstThreshold = False
    python:
        for i,c in availableCharacters.iteritems():
            c.battlechar.hp = c.battlechar.maxhp()
            c.battlechar.mp = c.battlechar.maxmp()
            c.battlechar.insane += 2
    "A night passes..."
    jump surviveLoop
label n_FirstBoss:
    scene bg club_day2
    show natsuki 4c at t11
    $ glitchName = glitchtext(9)
    n 4c "Huff... puff..."
    play sound "sfx/glitch3.ogg"
    sim "So what's that you're working on?"
    n 3b "Oh... not much..."
    n 1f "This place is giving me the heebie jeebies."
    n "And with the fact that there's so many monsters around, I thought to myself..."
    n 1c "I need to get out."
    n "So I figured... there must be some highest point here, right?"
    n 3d "And I'm gonna find it."
    n 3y "But I also thought, let's do it the Natsuki way."
    sim "What do you mean with the Natsuki way?"
    sim "...Actually, on second thought that seems like a-{nw}"
    n 4a "You wanna know the Natsuki way? I'm certainly glad you asked."
    n 4c "You see, I like manga, and anime..."
    n 4d "So, I got the best idea. I need to combine my favorite pastime into my escape plan. So I've come up with..."
    n 4z "...A mech."
    sim "What?"
    n 4l "A giant, bipedal, human-controlled robot."
    n 4y "If it succeeds, I'll be the first person to leave a place like this using a big robot."
    n 4d "If it fails, I'll be going out in a blaze of glory."
    sim "That... is quite the undertaking. Are you sure you're up for that?"
    n 5a "I've got the chassis already, just need strap some engines on it, then give it a lick of paint, et voila!"
    sim "Seems oddly simplistic for a robot..."
    n 2j "Yeah, well... Everything just sort of clicks. Like magic."
    n 2k "I don't even need to worry about rocket science, I just need to think robot thoughts!"
    show natsuki 1e at h11
    n "Oh shoot, I almost forgot the most important part!"
    sim "What?"
    n 1z "A drill that will PIERCE THE HEAVENS!"
    sim "Oh my god..."
    sim "Anyways, looks like you're all set."
    sim "I do need to warn you though..."
    n 1c "What for?"
    sim "Usually when you try to build something in this place, it attracts monsters."
    show natsuki 1g
    sim "It's why you don't see me building anything anytime soon."
    n 5g "Monsters aren't too much of a problem."
    sim "Well, they're not like the monsters you've seen before..."
    sim "They're harder... better... faster... stronger..."
    n 5s "..."
    n 5k "Better double time on the robot then."
    n 5j "Then I'll have a fighting chance, at least."
    sim "Well, I'll leave you to it then."
    n 5l "Okay. Bye, Simon!"
    play sound "sfx/glitch3.ogg"
    pause 1
    n 1a "Now, where was I?"
    stop music
    $ renpy.say(what="N-N-N-N-...", who="???")
    n 1c "Hm?"
    $ renpy.say(what="Naaaaa-a-a-a-a", who=glitchName)
    n 1m "Who's there?"
    $ renpy.say(what="Tsu-tsu-tsu-tsu--", who=glitchName)
    n 1f "S-Show yourself! This is not funny!"
    $ renpy.say(what="Kki-K--Ki-iiiKi-ki", who=glitchName)
    n 1p "Guys, I think I need...{nw}"
    $ style.say_dialogue = style.edited
    $ renpy.say(what="NATSUKIIIIIIIIIIII{nw}", who=glitchName)
    $ style.say_dialogue = style.normal
    show natsuki scream at h11
    n "AAAAAAAAAAAAAAAAAHHHHHH!{nw}"
    # TODO: MAYBE have a boss per character, but this may be overkill, so ignore this todo for now.
    $ chars = [availableCharacters[cidn].battlechar] + SayoriBoss1(1,availableCharacters[cidn].battlechar.lvl())
    hide natsuki
    call TrueBattle(chars, tune= "mod/testboss.mp3" )
    if( lastBattleWon ):
        show natsuki 1m at t11
        play music m1
        n "Oof... That was close..."
        play sound "sfx/glitch3.ogg"
        sim "Sayori! Are you alright?"
        n 5s "Y-Yeah..."
        sim "Phew... I saw something was wrong here, but I guess I was too late."
        sim "I'm glad you're okay..."
        n 1n  "Well, let's hope that won't happen ever again."
        sim "Don't count on it."
        sim "Like I said earlier, they're attracted to you making stuff."
        sim "If you want to continue your creation, you'll probably run into more, and bigger monsters."
        n 1s "..."
        n 1n "Alright, I'm quitting for now..."
        n 5k "But I'd better triple time on the robot."
        sim "Oh my god."
        if(persistent.demo):
            jump DemoEnd
    else:
        stop music
        n "Agghh..."
        n "N-Noooo..."
        "..."
        $ persistent.n_satisfaction = 0
        $ persistent.n_firstThreshold = False
    python:
        for i,c in availableCharacters.iteritems():
            c.battlechar.hp = c.battlechar.maxhp()
            c.battlechar.mp = c.battlechar.maxmp()
            c.battlechar.insane += 2
    "A night passes..."
    jump surviveLoop
