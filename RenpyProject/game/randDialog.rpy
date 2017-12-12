label n_randPainInTheNeck:
    play music m1
    #$del availableCharacters[cidy]
    #$del availableCharacters[cids]
    #$del availableCharacters[cidm]
    #$ availableCharacters[cidy] = 5
    #$ availableCharacters[cids] = 6
    #$ availableCharacters[cidm] = 7
    show natsuki 1x zorder 3 at f42
    if(cidy in availableCharacters.keys()):
        show yuri 1a zorder 2 at t43
    if(cidm in availableCharacters.keys()):
        show monika 1a zorder 2 at t41
    if(cids in availableCharacters.keys()):
        show sayori 1a zorder 2 at t44
    if(mainChar != None):
        $ mainChar = sim
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
    n 5f "I'm having this weird pain in the neck, and it's killing me."
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
