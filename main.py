import tetris_env
import pygame
import time
from settings import *
from agent import RandomAgent

class Main:
    def __init__(self, player=None, agent=None, render_mode=None, sfx=False):
        assert player in ["train", "human", "agent"], "unsupported player. Available: train, human, agent"
        
        self.sfx = sfx
        self.player = player
        self.isTraining = player=="train"
        self.agent = agent
        self.env = tetris_env.TetrisEnv(render_mode=render_mode)
        self.gameIsRunning = False
        self.restart = False
        
        self.keyHeld = [False] * 8 #Noop, left, right, rotleft, rotright, softdrop, harddrop, hold
        self.keyHeldFrame = [0] * 8

    def run(self):
        if self.player == "human":
            self.playHuman()
        elif self.player == "agent":
            self.playAgent()
        elif self.player == "train":
            self.train()
            
    
    def train(self):
        pass
    
    
    def playAgent(self, nEpisodes=5):
        assert self.player == "agent"
        self.gameIsRunning = True
        
        for episode in range(nEpisodes):
            if not self.gameIsRunning:
                break;
            
            done, info = self.env.reset()
            
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        self.gameIsRunning = False
                        break;
                    
                action = self.agent.getAction(done, info)
                done, info = self.env.step(action)
                
                if done:
                    break;
        
        self.gameIsRunning = False
        self.env.close()
         

    def playHuman(self):
        self.env.reset()
        self.gameIsRunning = True
        
        while self.gameIsRunning:
            if self.restart:
                self.gameIsRunning = False
                break;
            self.events()
            self.updateKeyHeldFrame()
            action = self.getAction()
            
            done, info = self.env.step(action)
            
            if self.sfx and info["locked"]:
                lockSFX.play()
                
            if done:
                self.gameIsRunning = False
                break;
            
        if self.restart:
            self.restart = False
            self.playHuman()
        self.env.close()
        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameIsRunning = False
                break;
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.sfx: tapSFX.play()
                    self.keyHeld[1] = True
                if event.key == pygame.K_RIGHT:
                    if self.sfx: tapSFX.play()
                    self.keyHeld[2] = True
                if event.key == pygame.K_z:
                    self.keyHeld[3] = True
                if event.key == pygame.K_x:
                    self.keyHeld[4] = True
                if event.key == pygame.K_DOWN:
                    self.keyHeld[5] = True
                if event.key == pygame.K_SPACE:
                    self.keyHeld[6] = True
                if event.key == pygame.K_r:
                    self.restart = True
                if event.key == pygame.K_c:
                    self.keyHeld[7] = True
                    
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.keyHeld[1] = False
                if event.key == pygame.K_RIGHT:
                    self.keyHeld[2] = False
                if event.key == pygame.K_z:
                    self.keyHeld[3] = False
                if event.key == pygame.K_x:
                    self.keyHeld[4] = False
                if event.key == pygame.K_DOWN:
                    self.keyHeld[5] = False
                if event.key == pygame.K_SPACE:
                    self.keyHeld[6] = False
                if event.key == pygame.K_c:
                    self.keyHeld[7] = False
                    
                    
    
    def updateKeyHeldFrame(self):
        for i in range(len(self.keyHeld)):
            if self.keyHeld[i]:
                self.keyHeldFrame[i] += 1
            else:
                self.keyHeldFrame[i] = 0
    
    
    def getDirection(self):
        direction = 0
        if self.keyHeld[1] and self.keyHeld[2]:
            direction = -1 if self.keyHeldFrame[1] < self.keyHeldFrame[2] else 1
        elif self.keyHeld[1] and not self.keyHeld[2]:
            direction = -1
        elif self.keyHeld[2] and not self.keyHeld[1]:
            direction = 1
            
        return direction
    
    
    def getRotation(self):
        rotation = 0 #counter clockwise
        if self.keyHeld[3] and self.keyHeldFrame[3] == 1:
            rotation = 1
        elif self.keyHeld[4] and self.keyHeldFrame[4] == 1:
            rotation = -1 
        return rotation
    
    
    def getDrop(self):
        drop = 0
        if self.keyHeld[5]:
            drop = 1
        if self.keyHeld[6] and self.keyHeldFrame[6] == 1:
            drop = 2
        return drop
    
    
    def getAction(self):
        direction = self.getDirection()
        rotation = self.getRotation()
        drop = self.getDrop()
        hold = False
        if self.keyHeld[7] and self.keyHeldFrame[7] == 1:
            hold = True
        return [direction, rotation, drop, hold]
    
            
        
    
if __name__ == '__main__':
    # main = Main(player="human", agent=RandomAgent, render_mode='human', sfx=True)
    main = Main(player="agent", agent=RandomAgent, render_mode='human', sfx=True)
    main.run()
    
    