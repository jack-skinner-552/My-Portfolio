import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.mp3')
        self.npc_pain = pg.mixer.Sound(self.path + 'DSPOPAIN.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'DSPODTH3.wav')
        self.npc_shot = pg.mixer.Sound(self.path + 'DSPISTOL.wav')
        self.player_pain = pg.mixer.Sound(self.path + 'DSPLPAIN.wav')
        self.player_death = pg.mixer.Sound(self.path + 'doomguy death sound effect.mp3')
        self.demon_pain = pg.mixer.Sound(self.path + 'DSDMPAIN.wav')
        self.cacodemon_death = pg.mixer.Sound(self.path + 'DSCACDTH.wav')
        self.cyberdemon_death = pg.mixer.Sound(self.path + 'DSCYBDTH.wav')

