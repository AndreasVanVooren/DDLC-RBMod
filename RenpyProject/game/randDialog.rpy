label n_randPainInTheNeck:
    play music m1
    # $del availableCharacters[cidy]
    # $del availableCharacters[cids]
    # $del availableCharacters[cidm]
    # $ availableCharacters[cidy] = 5
    # $ availableCharacters[cids] = 6
    # $ availableCharacters[cidm] = 7
    show natsuki 1x zorder 3 at f42
    $ hasChars = False
    if(cidy in availableCharacters.keys()):
        show yuri 1a zorder 2 at t43
        $ hasChars = True
    if(cidm in availableCharacters.keys()):
        show monika 1a zorder 2 at t41
        $ hasChars = True
    if(cids in availableCharacters.keys()):
        show sayori 1a zorder 2 at t44
        $ hasChars = True
    n 1x "Agghh..."
    show natsuki zorder 2 at t42
    if(cidy in availableCharacters.keys()):
        show yuri zorder 3 at f43
        y 1f "Is something bothering you?"
        show yuri zorder 2 at t43
    elif(cidm in availableCharacters.keys()):
        show monika zorder 3 at f41
        m 1d "Something wrong?"
        show monika zorder 2 at t41
    elif(cids in availableCharacters.keys()):
        show sayori zorder 3 at f44
        s 2b "What's wrong, Natsuki?"
        show sayori zorder 2 at t44
    else:
        sim "What's the matter?"
    show natsuki zorder 3 at f42
    n 5f "My neck is really stiff right now, and it's killing me."
    if(cidy in availableCharacters.keys()):
        n 5k "N-No offense."
        show natsuki zorder 2 at t42
        show yuri zorder 3 at f43
        y 1b "None taken."
        show yuri zorder 2 at t43
        if(cids in availableCharacters.keys()):
            show sayori zorder 3 at f44
            s 1x "It's okay. I'm getting used to it."
            show sayori zorder 2 at t44
    elif(cids in availableCharacters.keys()):
        n 5k "N-No offense."
        show natsuki zorder 2 at t42
        show sayori zorder 3 at f44
        s 1x "It's okay. I'm getting used to it."
        show sayori zorder 2 at t44
    show natsuki zorder 3 at f42
    n 5f "Ughh... this is so annoying..."
    n 5s "..."
    n crackn "Hang on, if I just..."
    show natsuki crackn
    pause 1.5
    stop music
    play sound "sfx/crack.ogg"
    show natsuki crackr
    if(cidy in availableCharacters.keys()):
        show yuri 3p at h43
    if(cids in availableCharacters.keys()):
        show sayori 4m at h44
    if(cidm in availableCharacters.keys()):
        show monika 1d at h41
    pause 0.75
    show natsuki crackn
    pause 0.75
    play sound "sfx/crack.ogg"
    show natsuki crackl
    pause 0.75
    show natsuki crackn
    pause 0.75
    n 4z "Aaahhhh... much better."
    play music m1
    n 4a "..."
    n 1h "What?"
    show natsuki zorder 2 at t42
    sim "Yowza, that sounded horrifying!"
    if(cidm in availableCharacters.keys()):
        show monika zorder 3 at f41
        m 2d "Did you seriously just do that?"
        show monika zorder 2 at t41
    if(cidy in availableCharacters.keys()):
        show yuri zorder 3 at f43
        y 3p "That sounded really painful, are you alright?"
        show yuri zorder 2 at t43
    if(cids in availableCharacters.keys()):
        show sayori zorder 3 at f44
        s 4n "Oh my god, are you okay, Natsuki?"
        s 4m "Natsuki?"
        show sayori zorder 3 at hf44
        s 4p "Natsukiiiiiiiiiiii!"
        show sayori 4n zorder 2 at t44
    show natsuki zorder 3 at f42
    n 1p "I-I'm fine! I do that pretty often!"
    if(hasChars):
        n 1g "You look like you've seen a ghost or something!"
    else:
        n 1g "It doesn't sound that horrible does it?"
    show natsuki zorder 2 at t42
    if(cidy in availableCharacters.keys()):
        show yuri 3g
    if(cids in availableCharacters.keys()):
        show sayori 2k
    if(cidm in availableCharacters.keys()):
        show monika 2o
    "..."
    hide sayori
    hide natsuki
    hide yuri
    hide monika
    return
