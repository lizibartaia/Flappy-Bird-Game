import pygame,random



class App:





    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.bkg_img = None
        self.base_img = None
        self.bird_img = None
        self.bird_rect = None
        self.color = 0
        self.x = 0
        self.y = None
        self.g_force = 0.25
        self.bird_new_pos = 0
        self.pipe_height = [200, 250, 300, 350, 400]
        self.list_of_pipes = []
        self.SPAWNPIPE = pygame.USEREVENT
        self.pipe_surface = pygame.image.load("pipe-green.png")
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)
        self.pipes = self.pipe_surface.get_rect(midtop = (360/2, 512/2)) #288/2 512/2
        self.top = self.pipe_surface.get_rect(midbottom=(300, 512/2)) #300 512/2
        self.random_pipe_pos = None
        self.game_active = True


    def create_pipe(self):
         self.random_pipe_pos = random.choice(self.pipe_height)
         self.pipes = self.pipe_surface.get_rect(midtop=(500,  self.random_pipe_pos))

         self.top =  self.pipe_surface.get_rect(midbottom=(500, self.random_pipe_pos - 150))
         return self.pipes,self.top

    def move_pipe(self,list_of_pipes):
        for pipe in self.list_of_pipes:
            pipe.centerx -= 5
        return self.list_of_pipes

    def draw_pipe( self,  list_of_pipes):
        for pipe in self.list_of_pipes:
            if pipe.bottom  >= 512: #512
                self.screen.blit(self.pipe_surface,pipe)
            else:
                self.flip_pipe = pygame.transform.flip(self.pipe_surface,False,True)
                self.screen.blit(self.flip_pipe ,pipe)

    def check_collision(self,list_of_pipes):
        for pipe in self.list_of_pipes:
            if self.bird_rec.colliderect(pipe):
                return False
        if self.bird_rec.top <= -50 or self.bird_rec.bottom >= 445:
            return False
        return True




    def run(self):
        self.init()
        while self.running:

            self.update()
            self.render()
        self.cleanUp()



    def init(self):
        pygame.init() #288,512
        self.screen = pygame.display.set_mode((288, 512))
        self.bkg_img = pygame.image.load("bg_5.png")
        pygame.display.set_caption("Flappy Bird")
        self.base_img = pygame.image.load("ground.png")
        self.bird_img = pygame.image.load("redbird-midflap.png")
        self.bird_rec = self.bird_img.get_rect(center = (100,212)) #birdrect
        self.pipe_surface = pygame.image.load("pipe-green.png")
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)
        self.SPAWNPIPE = pygame.USEREVENT
        self.random_pipe_height = [200,250,300,350,400]
        self.list_of_pipes = []
        self.flip_pipe = pygame.transform.flip(self.screen, False, True)
        pygame.time.set_timer(self.SPAWNPIPE, 1200)
        self.g_force = 0.25
        self.bird_new_pos = 0
        pygame.mixer.init()
        pygame.mixer.music.load("Fluffing-a-Duck.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_active = True
        self.game_over_surface = pygame.transform.scale2x(pygame.image.load('gameover.png').convert_alpha())
        self.game_over_rect = self.game_over_surface.get_rect(center=(180,150)) #half

    def update(self):
        self.events()




    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.bird_new_pos = 0
                    self.bird_new_pos -= 5
                if event.key == pygame.K_SPACE and self.game_active == False:
                    self.game_active = True
                    self.list_of_pipes.clear()
                    self.bird_rec.center = (100,212)
                    self.bird_new_pos = 0



            if event.type == self.SPAWNPIPE:
                print("pipe")
                self.list_of_pipes.extend(self.create_pipe())
                print(self.list_of_pipes)







    def render(self):
        self.screen.fill((0,0,0))


        self.screen.blit(self.bkg_img, (0, 0))

        if self.game_active:
            self.bird_new_pos += self.g_force
            #self.new_bird = self.rotate_bird(self.bird_img)
            self.bird_rec.centery += self.bird_new_pos
            self.screen.blit(self.bird_img,self.bird_rec)
            self.game_active = self.check_collision(self.list_of_pipes)

            self.list_of_pipes = self.move_pipe(self.list_of_pipes)
            self.draw_pipe(self.list_of_pipes)
        else:
            self.screen.blit(self.game_over_surface,self.game_over_rect)


        self.x -= 1
        self.screen.blit(self.base_img, (self.x, 512 - 60))
        self.screen.blit(self.base_img, (self.x + 288, 512 - 60))
        if self.x <= -288:
            self.x = 0








        pygame.display.flip()
        self.clock.tick(60)


    def cleanUp(self):
        pass


if __name__ == "__main__":
    app = App()
    app.run()

