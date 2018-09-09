import arcade
import os
import random
    
SCREEN_WIDTH  = 1200 #800
SCREEN_HEIGHT = 800 #600

SPRITE_SCALING_PLAYER = 0.5 #0.5
SPRITE_SCALING_COIN = 0.2 #0.2
SPRITE_SCALING_BOX  = 0.5
MOVEMENT_SPEED = 5

COIN_COUNT = 80
BOX_COUNT  = 2
PATH_IMAGES_ROOT = "images/"

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "the Game")
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.player_list = None
        self.player_2_list = None
        self.score = 0
        self.score_2 = 0
        self.physics_engine = None
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.player_list   = arcade.SpriteList()
        self.player_2_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.box_list = arcade.SpriteList()

        self.score   = 0
        self.score_2 = 0

        self.player_sprite = arcade.Sprite("images/player_01a.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 25
        self.player_sprite.center_y = SCREEN_HEIGHT-25
        self.player_list.append(self.player_sprite)

        self.player_2_sprite = arcade.Sprite("images/player_02a.png", SPRITE_SCALING_PLAYER)
        self.player_2_sprite.center_x = SCREEN_WIDTH - 25
        self.player_2_sprite.center_y = SCREEN_HEIGHT - 25
        self.player_2_list.append(self.player_2_sprite)

#.......add box
        for i in range(BOX_COUNT):
            box_v = arcade.Sprite("images/box_02a.png", SPRITE_SCALING_BOX)
            box_v.center_x = SCREEN_WIDTH / 2 
            box_v.center_y = SCREEN_HEIGHT * ((1+i)/4)
            self.box_list.append(box_v)
        for k in range(BOX_COUNT):
            box_h = arcade.Sprite("images/box_02a.png", SPRITE_SCALING_BOX)
            box_h.center_x = SCREEN_WIDTH * ((1+k)/3)
            box_h.center_y = SCREEN_HEIGHT / 2
            self.box_list.append(box_h)

#...... add coins
        for i in range(COIN_COUNT):
            coin = arcade.Sprite("images/coin_02a.png", SPRITE_SCALING_COIN)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            self.coin_list.append(coin)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.box_list)
        self.physics_engine_2 = arcade.PhysicsEngineSimple(self.player_2_sprite, self.box_list)

    def isCollision(self, lCoin, lBox):
        #print(f"lc: {len(lCoin)} | lb: {len(lBox)}")
        lll = arcade.SpriteList()
        for b in lBox:
            ll = arcade.check_for_collision_with_list(b, lCoin)
            if(len(ll)>0):
                for l in ll:
                    lll.append(l)
                for c in lll:
                    c.center_x = random.randrange(SCREEN_WIDTH)
                    c.center_y = random.randrange(SCREEN_HEIGHT)
                self.isCollision(lll, self.box_list)



    def on_draw(self):
        arcade.start_render()
        self.coin_list.draw()
        self.box_list.draw()
        self.player_list.draw()
        self.player_2_list.draw()
        output = f"Player 1: {self.score}"
        out_2  = f"Player 2: {self.score_2}" 
        outWin = "Game Over!\n"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 22)
        arcade.draw_text(out_2, SCREEN_WIDTH - 250, 20, arcade.color.WHITE, 22)
        if((self.score + self.score_2)>=COIN_COUNT):
            if(self.score > self.score_2):
                outWin += "Player 1 - Winner"
            elif(self.score == self.score_2):
                outWin += "Draw"
            elif(self.score_2 > self.score):
                outWin += "Player 2 - Winner"
            arcade.draw_text(outWin, SCREEN_WIDTH/2, SCREEN_HEIGHT*(2/3), arcade.color.WHITE, 32)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED        

        if key == arcade.key.UP:
            self.player_2_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_2_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_2_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_2_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or arcade.key.D:
            self.player_sprite.change_x = 0

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_2_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_2_sprite.change_x = 0

    def update(self, delta_Time):
        self.coin_list.update()
        coins_hit_list   = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        coins_hit_list_2 = arcade.check_for_collision_with_list(self.player_2_sprite, self.coin_list)
        for coin in coins_hit_list:
            coin.kill()
            self.score += 1
        for coin_2 in coins_hit_list_2:
            coin_2.kill()
            self.score_2 += 1
        self.physics_engine.update()
        self.physics_engine_2.update()

    def isBeyond(self, player):
        if(player.center_x >= SCREEN_WIDTH):
            player.center_x = 0 + 4
        if(player.center_x <= 0):
            player.center_x = SCREEN_WIDTH - 4
 
def main():
    window = MyGame()
    window.setup()
    window.isCollision(window.coin_list, window.box_list)
    arcade.run()

if __name__ == "__main__":
    main()

