transform sticker_hop:
    yoffset 80
    easein_quad .24 yoffset -60
    easeout_quad .18 yoffset 0

image tos2g = "mod/warning2g.png"

#[TODO] Maybe add mod versions of these
image m_sticker:
    "gui/poemgame/m_sticker_1.png"

image s_sticker:
    "gui/poemgame/s_sticker_1.png"

image n_sticker:
    "gui/poemgame/n_sticker_1.png"

image y_sticker:
    "gui/poemgame/y_sticker_1.png"

image s_sticker hop:
    "gui/poemgame/s_sticker_2.png"
    sticker_hop
    "s_sticker"

image n_sticker hop:
    "gui/poemgame/n_sticker_2.png"
    sticker_hop
    "n_sticker"

image y_sticker hop:
    "gui/poemgame/y_sticker_2.png"
    sticker_hop
    "y_sticker"

transform hagusuki:
    tcommon(300)

image m_sticker hop:
    "gui/poemgame/m_sticker_2.png"
    sticker_hop
    "m_sticker"

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
    "gui/invis.png"

image hand :
     "mod/enemies/hand.png"
     yalign 0
     yanchor 0

default persistent.first_battle = True
default persistent.hasSeenPHPRant = False


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

image yuri stab_repeat:
    "yuri/stab/4.png"
    0.4
    "yuri/stab/5.png"
    0.4
    repeat

define audio.t6g2 = "<from 4.619>bgm/6g.ogg"
define audio.stabloop = "mod/stabloop.ogg"

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

    def Souffle(m,s,t):
        global characters
        truHeal = m.damage
        for c in characters:
            if(c.team == s.team):
                c.hp += truDmg
                if(c.hp > c.maxhp()): c.hp = c.maxhp()
        return s.name + " healed " + str(truHeal) + " to all party members!"

    atk_spark    = Attack("Spark",10,0)
    atk_glitch   = Attack("Glitch",30,10,5)
    atk_whip     = Attack("Whip",10,0)
    atk_lasso    = Attack("Lasso",20,5,3, ApplyFunc= Lasso)
    atk_stab     = Attack("Stab",10,0)
    atk_shank    = Attack("Shank",40,15,6)
    atk_pan      = Attack("Pan",10,0)
    atk_bake     = Attack("Bake",20,5,2, ApplyFunc=DefaultHeal, icon_path = "mod/icons/heal.png")
    atk_souffle  = Attack("Soufflé",40,20,0, ApplyFunc=Souffle, icon_path = "mod/icons/heal.png")
