import pygame


audioInit = False

soundDBnames = ['door','drink','hit','inventory','magic','walk','miss','pickup','fire','glass']
soundDB =  {};

def initAudio():
	pygame.mixer.pre_init(44100, -16, 1, 512)
	pygame.mixer.init()
	for el in soundDBnames:
		soundDB[el] = pygame.mixer.Sound('audio/'+el+'.wav')
	 


if audioInit == False:
	audioInit = True
	initAudio();


def PlaySound(str):
	#pygame.mixer.music.load('audio/drink.wav')
	print str
	sound = soundDB[str]
	sound.play()


