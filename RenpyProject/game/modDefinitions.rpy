transform mod_sticker_hop:
    yoffset 80
    easein_quad .24 yoffset -60
    easeout_quad .18 yoffset 0

image tos2g = "mod/warning2g.png"

#[TODO] Maybe add mod versions of these
image mod_m_sticker:
    "gui/poemgame/m_sticker_1.png"

image mod_s_sticker:
    "gui/poemgame/s_sticker_1.png"

image mod_n_sticker:
    "gui/poemgame/n_sticker_1.png"

image mod_y_sticker:
    "gui/poemgame/y_sticker_1.png"

image mod_s_sticker hop:
    "gui/poemgame/s_sticker_2.png"
    mod_sticker_hop
    "mod_s_sticker"

image mod_n_sticker hop:
    "gui/poemgame/n_sticker_2.png"
    mod_sticker_hop
    "mod_n_sticker"

image mod_y_sticker hop:
    "gui/poemgame/y_sticker_2.png"
    mod_sticker_hop
    "mod_y_sticker"

image mod_m_sticker hop:
    "gui/poemgame/m_sticker_2.png"
    mod_sticker_hop
    "mod_m_sticker"

transform hagusuki:
    tcommon(300)

image batoru = "mod/batoru.png"

image noose:
    "mod/enemies/noose.png"
    yalign 0
    yanchor 0
image noosekill:
    "mod/enemies/noose.png"
    xalign 0.5
    yalign 0.5

image explosion:
    xalign 0.5
    yalign 0.5
    "mod/particles/boom0.png"
    0.1
    "mod/particles/boom1.png"
    0.1
    "mod/particles/boom2.png"
    0.1
    "mod/particles/boom3.png"
    0.1
    "mod/particles/boom4.png"
    0.1
    "mod/particles/boom5.png"
    0.1
    "mod/particles/boom6.png"
    0.1
    "mod/particles/boom7.png"
    0.1
    "mod/invis.png"

# transform bouncyCake:

image whipit:
    xalign 0.5
    yalign 0.5
    "mod/attacks/whip2.png"
    xoffset -150
    yoffset 40
    rotate -30
    linear 0.3 rotate 30 xoffset 0
    "mod/attacks/whip4.png"
    yoffset 0
    xalign 0.5
    yalign 0.5
    rotate 0
    linear 0.5 zoom 1.5 alpha 0

image spark:
    xalign 0.5
    yalign 0.5
    "mod/attacks/spark1.png"
    0.1
    "mod/attacks/spark2.png"
    0.1
    "mod/attacks/spark1.png"
    0.1
    "mod/attacks/spark2.png"
    0.1
    "mod/attacks/spark1.png"
    0.1
    "mod/attacks/spark2.png"
    0.1
    "mod/attacks/spark3.png"
    0.1
    "mod/attacks/spark2.png"
    0.1
    "mod/attacks/spark1.png"
    0.1
    "mod/invis.png"

init -1 python:
    def glitchFunc(trans,st,at):
        trans.xoffset = renpy.random.randint(-5,5)
        trans.yoffset = renpy.random.randint(-5,5)
        randFloatX = renpy.random.random()*0.1 + 0.95
        randFloatY = renpy.random.random()*0.1 + 0.95
        trans.xzoom = randFloatX
        trans.yzoom = randFloatY
        return 0.02
    def rumble(trans,st,at):
        trans.xoffset = renpy.random.randint(-3,3)
        trans.yoffset = renpy.random.randint(-3,3)


image glitch:
    xalign 0.5
    yalign 0.5
    block:
        "mod/attacks/glitch1.png"
        0.1
        "mod/attacks/glitch2.png"
        0.1
        "mod/attacks/glitch3.png"
        0.1
        "mod/attacks/glitch4.png"
        0.1
        repeat 4
    parallel:
        "mod/attacks/glitch5.png"
        0.05
        "mod/attacks/glitch6.png"
        0.05
        repeat
    parallel:
        function glitchFunc
    parallel:
        2
        linear 0.3 alpha 0

image lassothecarp:
    xalign 0.5
    yalign 0.5
    "mod/attacks/lasso.png"
    xoffset -300
    yoffset -20
    rotate -50
    easein 0.4 rotate 0 xoffset 0 yoffset 0
    linear 0.4 xzoom 0.5
    alpha 0

image knifeattack:
    contains:
        xalign 0.5
        yalign 0.5
        "mod/attacks/knife.png"
        rotate -30
        xoffset 225
        yoffset -130
        linear 0.25 xoffset 52 yoffset -30
        function playStab
        linear 0.25 alpha 0
    contains:
        0.25
        "blood"
        0.25
        linear 0.1 alpha 0

image shank:
    contains:
        xalign 0.5
        yalign 0.5
        "mod/attacks/knife.png"
        rotate -30
        block:
            xoffset 104
            yoffset -60
            0.05
            xoffset 52
            yoffset -30
            function playStab
            0.05
            repeat 5
        linear 0.25 alpha 0
    contains:
        0.05
        "blood"
        0.25
        linear 0.1 alpha 0
    contains:
        0.25
        "blood"
        0.25
        linear 0.1 alpha 0
    contains:
        0.45
        "blood"
        0.25
        linear 0.1 alpha 0

image panattack:
    xalign 0.5
    yalign 0.5
    "mod/attacks/pan.png"
    rotate 135
    offset (300,0)
    parallel:
        linear 0.4 offset (0,0) knot (150,-100)
    parallel:
        linear 0.4 rotate 45
    "mod/attacks/whip4.png"
    yoffset 0
    xalign 0.5
    yalign 0.5
    rotate 0
    linear 0.5 zoom 1.5 alpha 0

transform playerArea:
    xcenter 0.5
    ycenter 0.5
    xalign 0.5
    yalign 0.5
    xanchor 0.5
    yanchor 0.5
    xanchor 0.5
    yanchor 0.5
    xoffset 640
    yoffset 640

image souffleattack:
    contains:
        "mod/attacks/oven.png"
        0.75
        "mod/attacks/oven2.png"
        0.6
        linear 0.2 alpha 0
    contains:
        0.75
        "mod/attacks/souffle.png"
        parallel:
            easein 0.4 yoffset -200
            easeout 0.4 yoffset 0
        parallel:
            linear 0.8 rotate -120
        parallel:
            0.6
            linear 0.2 alpha 0

image cupcakeattack:
    xalign 0.5
    yalign 0.5
    contains:
        xalign 0.5
        yalign 0.5
        "mod/attacks/oven.png"
        0.75
        "mod/attacks/oven2.png"
        0.6
        linear 0.2 alpha 0
    contains:
        0.75
        xalign 0.5
        yalign 0.5
        "mod/attacks/cupcake.png"
        parallel:
            easein 0.4 yoffset -200
            easeout 0.4 yoffset 0
        parallel:
            linear 0.8 rotate -120
        parallel:
            0.6
            linear 0.2 alpha 0

image hand :
     "mod/enemies/hand.png"
     yalign 0
     yanchor 0

image constrict:
    "mod/attacks/constrict.png"


default persistent.first_battle = True
default persistent.hasSeenPHPRant = False
default persistent.timesHealedOpponent = 0

default persistent.s_satisfaction = 0.0
default persistent.s_firstThreshold = False
default persistent.m_satisfaction = 0.0
default persistent.m_firstThreshold = False
default persistent.n_satisfaction = 0.0
default persistent.n_firstThreshold = False
default persistent.y_satisfaction = 0.0
default persistent.y_firstThreshold = False
default persistent.sim_satisfaction = 0.0

default availableCharacters = {}

init -1 python :
    def playStab(trans,st,at):
        renpy.sound.play( renpy.random.choice(["<to 1>sfx/stab.ogg", "<from 1.941 to 3>sfx/stab.ogg", "<from 4.211 to 5>sfx/stab.ogg"]) )
        return None
    def playRetract(trans,st,at):
        renpy.sound.play( renpy.random.choice(["<from 1.194 to 1.941>sfx/stab.ogg", "<from 3.281 to 4.211>sfx/stab.ogg"]) )
        return None

image yuri stab_repeat:
    "yuri/stab/4.png"
    function playStab
    0.4
    "yuri/stab/5.png"
    function playRetract
    0.4
    repeat

define audio.t6g2 = "<from 4.619>bgm/6g.ogg"
define audio.stabloop = "mod/stabloop.ogg"
define audio.singlestab1 = "<to 1>stab.ogg"
define audio.singlestab2 = "<from 1.941 to 3>stab.ogg"
define audio.singlestab3 = "<from 4.211 to 5>stab.ogg"
define audio.singlestabretract1 = "<from 1.194 to 1.941>stab.ogg"
define audio.singlestabretract1 = "<from 3.281 to 4.211>stab.ogg"

define sim = DynamicCharacter('sim_name', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
default sim_name = "Bellevue"

define cid0 = 0
define cidy = 1
define cids = 2
define cidn = 3
define cidm = 4
define cidsim = 5

#sayori extensions : chr (but not any of the dokis, they're auto excluded) wants to return to status quo, meaning she wants to make her own doki doki
define sayori_extensions = [".chr",".db",".cab"]
#monika extensions : cs, cpp, py, lua, h, js, java, aka programming related tags
define monika_extensions = [".cs",".cpp",".py",".lua",".h",".js",".java"]
#natsuki extensions : pdf, txt, doc, docx, epub, elf    #takes various book and reading formats to represent manga and anime, also elf, because of course
define natsuki_extensions = [".pdf",".doc",".docx",".odt",".epub",".elf"]
#yuri extensions : pdf, txt, doc, docx, epub    #takes various book and reading formats to represent books
define yuri_extensions = [".pdf",".doc",".docx",".odt",".epub"]

#sayori tags : school fest(ival) poem
define sayori_tags = ["school","festive","festival","poem","happy","fun","happiness"]
#natsuki tags : cook bake cake doki manga naruto goku anime
define natsuki_tags = ["cook","bake","doki","cake","naruto","goku","anime","manga","parfait","cute","bun"]
#natsuki extensions : pdf, txt, doc, docx, epub, elf    #takes various book and reading formats to represent manga and anime, also elf, because of course
define monika_tags = ["script","code","literature","python","player","reality","love","truth"]
#yuri tags
define yuri_tags = ["dark","knife","brooding","evil","insanity","psychology","indescribable","imagination","obsession","darkness","blood","intoxicat"]#intoxicat can lead to intoxication, intoxicating, intoxicated, etc.
#sayori bulli : noose hang
define sayori_negatags = ["noose","hang"]


define null_bgpaths = ["bg/glitch.jpg"]
define null_bgids = ["bg glitch"]
#sayori room bgs - paths describe the path of the base image that will be displayed, ids will display what image will actually be the backdrop
define sayori_bgpaths = ["bg/sayori_bedroom.png","bg/house.png", "bg/class.png"]
define sayori_bgids = ["bg sayori_bedroom","bg house", "bg class_day"]
#natsuki room bgs
define natsuki_bgpaths = ["bg/kitchen.png","bg/closet.png"]
define natsuki_bgids = ["bg kitchen","bg closet"]
#natsuki room bgs
define monika_bgpaths = ["bg/club-skill.png","bg/residential.png"]
define monika_bgids = ["bg club_day2","bg residential_day"]
#yuri room bgs
define yuri_bgpaths = ["bg/bedroom.png","bg/corridor.png"]
define yuri_bgids = ["bg bedroom","bg corridor"]


init python:

    # Get ctypes library
    from ctypes import *
    # Gets the absolute file path of the DLL, then opens said DLL using Python.
    if(renpy.windows):
        lib = CDLL(renpy.loader.transfn('DDLCCDLL.dll'))
    elif(renpy.linux):
        lib = CDLL(renpy.loader.transfn('DDLCCDLL_Linux.so'))
    else:
        renpy.error("The platform you're trying to run this on does not yet support this mod")
    def UpdateFilesInRecycleBin():
        lib.UpdateFilesInRecycleBin()
    def GetFileCount():
        return lib.GetRecycleBinFileCount()
    def GetRecycleBinFiles():
        count = GetFileCount()
        returnval = []
        for i in range(count):
            # Probably the worst idea ever
            returnval.append( c_wchar_p(lib.GetRecycleBinFileAt(i)).value )
        return returnval
    def BinContainsFile(fileName):
        return lib.BinContainsFile(c_wchar_p(fileName))
    def VerifySize(fileName, fileSize):
        return lib.VerifySize(fileName, fileSize)

    def Lasso(m,s,t):
        DefaultApply(m,s,t)
        return s.name + " lasso'd " + t.name + " like a wild animal!"

    def Bake(m,s,t):
        truHeal = m.damage
        if(t != s):
            result = s.name + " baked a delicious cupcake for " + t.name + ", healing " + str(truHeal) + "HP."
        else:
            result = s.name + " baked a delicious cupcake for herself, healing " + str(truHeal) + "HP."
        if(t.team != s.team):
            result = AppendBadMove(result)
        return result;

    def Souffle(m,s,t):
        global characters
        truHeal = m.damage
        for c in characters:
            if(c.team == s.team):
                c.hp += truHeal
                if(c.hp > c.maxhp()): c.hp = c.maxhp()
        return s.name + " healed " + str(truHeal) + " to all party members!"

    atk_spark       = Attack("Spark",10,0, img_id = "spark", sfx_path = "mod/sfx/spark16.wav")
    atk_glitch      = Attack("Glitch",30,10,5, img_id = "glitch", sfx_path = "mod/sfx/glitch16.wav")
    atk_whip        = Attack("Whip",10,0, img_id="whipit", sfx_path = "mod/sfx/whipcrack16.wav")
    atk_lasso       = Attack("Lasso",20,5,3, ApplyFunc= Lasso, img_id="lassothecarp", sfx_path = "mod/sfx/lasso16.wav")
    atk_stab        = Attack("Stab",10,0, img_id = "knifeattack", sfx_path = "<silence .1>")
    atk_shank       = Attack("Shank",40,15,6, img_id = "shank", sfx_path = "<silence .1>")
    atk_pan         = Attack("Pan",10,0, img_id = "panattack", sfx_path = "mod/sfx/pan.wav")
    atk_bake        = Attack("Bake",20,5,2, ApplyFunc=Bake, icon_path = "mod/icons/heal.png", img_id = "cupcakeattack", sfx_path = "mod/sfx/oven.wav")
    atk_souffle     = Attack("Soufflé",40,20,0, ApplyFunc=Souffle, icon_path = "mod/icons/heal.png", img_id = "souffleattack", sfx_path = "mod/sfx/oven.wav", overrideTransform = Transform(xalign = 0.0, yalign = 0.0, xanchor = 0.0, yanchor = 0.0, xoffset = 515, yoffset = 500))
    atk_constrict   = Attack("Strangle",15, img_id="", sfx_path="constrict.wav")
