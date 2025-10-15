import pgzrun
from level_data import level
from pgzero.builtins import Actor, Rect, keyboard, sounds, music
# Game Configuration
WIDTH, HEIGHT, TILE_SIZE = 1000, 800, 64
TITLE = "Platformer Game"

# Game State
game_state = "MENU"  
music_on = True

# Camera Position
camera_x = 0
camera_y = 0

# Physics Constants
GRAVITY = 0.8
JUMP_STRENGTH = -15
ANIMATION_SPEED = 10

# Tile Types
SOLID_TILES = ['b', 'p', 'c', 'g']

# Parent Entity Class
class Entity:
    def __init__(self, x, y, image):
        self.actor = Actor(image)
        self.actor.x, self.actor.y = x, y
        self.velocity_y = 0
        self.on_ground = False
        self.speed = 5
        
    def apply_physics(self):
        """Apply gravity and ground collision"""
        # Apply gravity
        self.velocity_y += GRAVITY
        self.actor.y += self.velocity_y
        
        # Check ground collision with smaller hitbox for more precise detection
        self.on_ground = False
        
        # Create a smaller hitbox for the feet (bottom portion of the entity)
        feet_hitbox = Rect(
            int(self.actor.x - self.actor.width // 4),      # Narrower width
            int(self.actor.y + self.actor.height // 4),      # Start from center, go to bottom
            int(self.actor.width // 2),                      # Half the width
            int(self.actor.height // 4)                      # Quarter of the height
        )
        
        # Create a smaller hitbox for the head (top portion of the entity)
        head_hitbox = Rect(
            int(self.actor.x - self.actor.width // 4),      # Narrower width
            int(self.actor.y - self.actor.height // 2),      # Top of the entity
            int(self.actor.width // 2),                      # Half the width
            int(self.actor.height // 4)                      # Quarter of the height
        )
        
        for tile in tiles:
            if tile.type in SOLID_TILES:  
                # Get the tile's rect for collision detection
                tile_rect = Rect(tile.left, tile.top, tile.width, tile.height)
                
                # Check for landing on top of tile (moving down)
                if feet_hitbox.colliderect(tile_rect) and self.velocity_y > 0:
                    # Additional check: only land if we're coming from above
                    if self.actor.bottom > tile.top and self.actor.bottom - self.velocity_y <= tile.top + 5:
                        self.actor.bottom = tile.top
                        self.velocity_y = 0
                        self.on_ground = True
                        break
                
                # Check for hitting bottom of tile (jumping into block from below)
                if head_hitbox.colliderect(tile_rect) and self.velocity_y < 0:
                    # Additional check: only hit if we're coming from below
                    if self.actor.top < tile.bottom and self.actor.top - self.velocity_y >= tile.bottom - 5:
                        self.actor.top = tile.bottom
                        self.velocity_y = 0  # Stop upward movement
                        break

    def check_horizontal_collision(self):
        """Prevent walking through walls with precise hitbox"""
        # Create a body hitbox (excludes top and bottom portions)
        body_hitbox = Rect(
            int(self.actor.x - self.actor.width // 4),
            int(self.actor.y - self.actor.height // 4),
            int(self.actor.width // 2),
            int(self.actor.height // 2)
        )
        
        for tile in tiles:
            if tile.type in SOLID_TILES:  
                # Get the tile's rect for collision detection
                tile_rect = Rect(tile.left, tile.top, tile.width, tile.height)
                
                if body_hitbox.colliderect(tile_rect):
                    # Check if collision is horizontal (not just touching top/bottom)
                    if abs(self.actor.centery - tile.centery) < TILE_SIZE:
                        if self.actor.x < tile.x:
                            self.actor.right = tile.left + self.actor.width // 4
                            return 'left'
                        else:
                            self.actor.left = tile.right - self.actor.width // 4
                            return 'right'
        return None

# Player Class
class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 'character_beige_idle')
        self.jumping = False
        self.animation_timer = 0
        self.animation_frame = 0
        self.walking_sound_playing = False 
        
    def handle_input(self):
        is_moving = False
        
        # Handle left/right movement
        if keyboard.left:
            self.actor.x -= self.speed
            self.check_horizontal_collision()
            is_moving = True
        elif keyboard.right:
            self.actor.x += self.speed
            self.check_horizontal_collision()
            is_moving = True
        if is_moving:
            if not self.walking_sound_playing:
                sounds.walking.play(-1) 
                self.walking_sound_playing = True
        else:
            if self.walking_sound_playing:
               sounds.walking.stop()
               self.walking_sound_playing = False
        # Animate walking or idle
        if is_moving:
            self.animation_timer += 1
            if self.animation_timer >= ANIMATION_SPEED:
                self.animation_timer = 0
                self.animation_frame = 1 - self.animation_frame
                self.actor.image = 'character_beige_walk_a' if self.animation_frame == 0 else 'character_beige_walk_b'
        else:
            self.animation_timer += 1
            if self.animation_timer >= ANIMATION_SPEED * 2:
                self.animation_timer = 0
                self.animation_frame = 1 - self.animation_frame
                self.actor.image = 'character_beige_idle' if self.animation_frame == 0 else 'character_beige_front'
        
        # Jump
        if keyboard.space and not self.jumping:
            self.velocity_y = JUMP_STRENGTH
            self.jumping = True
            sounds.jump.play() 
            self.actor.image = 'character_beige_jump'
    
    def apply_physics(self):
        """Override to track jumping state"""
        super().apply_physics()
        self.jumping = not self.on_ground
    
    def check_collisions(self):
        global game_state
        # Collect coins
        for coin in coins[:]:
            if self.actor.colliderect(coin):
                sounds.coincollect.play()
                coins.remove(coin)
        # Check flag
        for tile in tiles:
            if tile.type == 'F' and self.actor.colliderect(tile):
                game_state = "WIN"
                sounds.winsound.play()
                break
        
    def check_enemy_collision(self):
        """Check if player touches enemy - game over if true"""
        global game_state
        for enemy in enemies:
            # Create smaller hitboxes for more precise collision
            player_hitbox = Rect(self.actor.x - self.actor.width // 4, 
                                self.actor.y - self.actor.height // 4,
                                self.actor.width // 2, self.actor.height // 2)
            enemy_hitbox = Rect(enemy.actor.x - enemy.actor.width // 4,
                               enemy.actor.y - enemy.actor.height // 4,
                               enemy.actor.width // 2, enemy.actor.height // 2)
            
            if player_hitbox.colliderect(enemy_hitbox):
                game_state = "GAME_OVER"
                sounds.losesound.play()
                break
    
    def reset(self, x, y):
        self.actor.x, self.actor.y = x, y
        self.velocity_y = 0
        self.jumping = False
        self.on_ground = False
        self.animation_timer = 0
        self.animation_frame = 0
        self.actor.image = 'character_beige_idle'

# Enemy Class
class Enemy(Entity):
    def __init__(self, x, y, enemy_type):
        self.type = enemy_type
        self.animation_timer = 0
        self.animation_frame = 0
        self.direction = 1  # 1 = right, -1 = left
        
        # Set enemy properties based on type
        if enemy_type == 'snail':
            super().__init__(x, y, 'snail_walk_a')
            self.speed = 1.5
            self.detection_range = 200
            self.patrol_distance = 100
            self.images_left = ['snail_walk_a', 'snail_walk_b']
            self.images_right = ['snail_walk_left_a', 'snail_walk_left_b']
            self.uses_physics = True
        else:  # fly
            super().__init__(x, y, 'fly_a')
            self.speed = 2.5
            self.detection_range = 250
            self.patrol_distance = 150
            self.images_left = ['fly_a', 'fly_b']
            self.images_right = ['fly_left_a', 'fly_left_b']
            self.uses_physics = False
            
        
        self.start_x = x  # Remember starting position for patrol
        self.start_y = y
    
    def apply_physics(self):
        """Only apply physics for ground-based enemies"""
        if self.uses_physics:
            super().apply_physics()
    
    def check_horizontal_collision(self):
        """Override to turn around when hitting walls"""
        if not self.uses_physics:
            return  # Flies can pass through
        
        collision_side = super().check_horizontal_collision()
        if collision_side:
            self.direction *= -1  # Turn around when hitting wall
    
    def check_edge(self):
        """Turn around at ledges (only for ground-based enemies)"""
        if not self.uses_physics or not self.on_ground:
            return
        
        # Check if there's ground ahead
        check_x = self.actor.x + (TILE_SIZE * self.direction)
        check_y = self.actor.bottom + 10
        
        ground_ahead = False
        for tile in tiles:
            if tile.type in SOLID_TILES:  
                if (abs(tile.top - check_y) < 20 and 
                    abs(tile.x - check_x) < TILE_SIZE):
                    ground_ahead = True
                    break
        
        # Turn around if no ground ahead (at edge)
        if not ground_ahead:
            self.direction *= -1
        
    def update(self):
        # Apply physics first (for ground-based enemies)
        self.apply_physics()
        
        distance_to_player = abs(player.actor.x - self.actor.x)
        
        # Chase player if close enough, otherwise patrol
        if distance_to_player < self.detection_range:
            # Chase mode
            self.direction = -1 if player.actor.x < self.actor.x else 1
            self.actor.x += self.speed * self.direction
        else:
            # Patrol mode - move back and forth
            if abs(self.actor.x - self.start_x) > self.patrol_distance:
                self.direction *= -1
            self.actor.x += self.speed * self.direction
        
        # Check collisions after movement
        self.check_horizontal_collision()
        self.check_edge()
        
        # Animate enemy
        self.animation_timer += 1
        if self.animation_timer >= 8:
            self.animation_timer = 0
            self.animation_frame = 1 - self.animation_frame
            current_images = self.images_right if self.direction > 0 else self.images_left
            self.actor.image = current_images[self.animation_frame]
    
    def reset(self):
        """Reset enemy to starting position"""
        self.actor.x = self.start_x
        self.actor.y = self.start_y
        self.velocity_y = 0
        self.on_ground = False
        self.direction = 1
        self.animation_timer = 0
        self.animation_frame = 0

player = Player(100, 200)

# Tile mapping
TILES = {
    ' ': None,
    'g': 'terrain_grass_block_top',
    'p': 'block_green',
    'c': 'block_coin',
    'F': 'flag_red_a',
    'b': 'terrain_grass_block_center',
}

# Build world from level design
tiles = []
coins = []
for row_index, row in enumerate(level):
    for col_index, cell in enumerate(row):
        if cell in TILES and TILES[cell]:
            tile = Actor(TILES[cell])
            tile.x = col_index * TILE_SIZE + TILE_SIZE // 2
            tile.y = row_index * TILE_SIZE + TILE_SIZE // 2
            tile.type = cell
            tiles.append(tile)
            
            # Add coins above coin blocks
            if cell == 'c':
                coin = Actor('coin_gold')
                coin.x = tile.x
                coin.y = tile.y - TILE_SIZE
                coins.append(coin)
total_coins = len(coins)
# Create enemies
enemies = [
    Enemy(800, 480, 'snail'),
    Enemy(1200, 350, 'fly'),
    Enemy(1800, 480, 'snail'),
    Enemy(3413, 192, 'snail'),
    Enemy(4129, 20, 'snail'),
]

# Menu buttons
button_start = Rect((WIDTH // 2 - 100, 300), (200, 60))
button_music = Rect((WIDTH // 2 - 100, 400), (200, 60))
button_exit = Rect((WIDTH // 2 - 100, 500), (200, 60))

# Main draw function
def draw():
    screen.clear()
    if game_state == "MENU":
        draw_menu()
    elif game_state == "PLAYING":
        draw_game()
    elif game_state == "GAME_OVER":
        draw_game_over()
    elif game_state == "WIN":
        draw_win()

def draw_end_screen(bg_color, title, title_color):
    """Helper function to draw game over or win screen"""
    screen.fill(bg_color)
    screen.draw.text(title, center=(WIDTH // 2, HEIGHT // 2 - 50),
                     fontsize=80, color=title_color)
    screen.draw.text("Press SPACE to play again", center=(WIDTH // 2, HEIGHT // 2 + 50),
                     fontsize=40, color="white")
    
    if keyboard.space:
        global game_state
        game_state = "PLAYING"
        reset_game()

def draw_win():
    """Draw win screen"""
    draw_end_screen((50, 200, 50), "YOU WIN!", "yellow")

def draw_game_over():
    """Draw game over screen"""
    draw_end_screen((50, 50, 50), "GAME OVER", "red")

def draw_menu():
    screen.fill((135, 206, 235))
    screen.draw.text("PLATFORMER GAME", center=(WIDTH // 2, 150),
                     fontsize=60, color="black")
    
    # Draw start button
    screen.draw.filled_rect(button_start, (100, 200, 100))
    screen.draw.rect(button_start, (0, 0, 0))
    screen.draw.text("Start Game", center=button_start.center, fontsize=40, color="white")
    
    # Draw music button
    music_text = f"Music: {'ON' if music_on else 'OFF'}"
    screen.draw.filled_rect(button_music, (100, 150, 200))
    screen.draw.rect(button_music, (0, 0, 0))
    screen.draw.text(music_text, center=button_music.center, fontsize=40, color="white")
    
    # Draw exit button
    screen.draw.filled_rect(button_exit, (200, 100, 100))
    screen.draw.rect(button_exit, (0, 0, 0))
    screen.draw.text("Exit", center=button_exit.center, fontsize=40, color="white")

def draw_game():
    # Draw tiled background
    bg_size = 512
    start_x = int(-(camera_x % bg_size))
    start_y = int(-(camera_y % bg_size))
    for x in range(start_x, WIDTH + bg_size, bg_size):
        for y in range(start_y, HEIGHT + bg_size, bg_size):
            screen.blit('background_fade_desert', (x, y))
    
    # Draw tiles
    for tile in tiles:
        screen_x = tile.x - camera_x
        screen_y = tile.y - camera_y
        if -TILE_SIZE < screen_x < WIDTH + TILE_SIZE and -TILE_SIZE < screen_y < HEIGHT + TILE_SIZE:
            screen.blit(tile.image, (screen_x - TILE_SIZE//2, screen_y - TILE_SIZE//2))
    
    # Draw coins
    for coin in coins:
        screen_x = coin.x - camera_x
        screen_y = coin.y - camera_y
        if -TILE_SIZE < screen_x < WIDTH + TILE_SIZE and -TILE_SIZE < screen_y < HEIGHT + TILE_SIZE:
            screen.blit(coin.image, (screen_x - TILE_SIZE//2, screen_y - TILE_SIZE//2))
    
    # Draw enemies
    for enemy in enemies:
        screen_x = enemy.actor.x - camera_x
        screen_y = enemy.actor.y - camera_y
        if -TILE_SIZE < screen_x < WIDTH + TILE_SIZE and -TILE_SIZE < screen_y < HEIGHT + TILE_SIZE:
            screen.blit(enemy.actor.image, (screen_x - enemy.actor.width//2, screen_y - enemy.actor.height//2))
    
    # Draw player
    original_x, original_y = player.actor.x, player.actor.y
    player.actor.pos = (player.actor.x - camera_x, player.actor.y - camera_y)
    player.actor.draw()
    player.actor.x, player.actor.y = original_x, original_y
    
    #Draw Coins collected at the top right corner
    coins_collected = total_coins - len(coins)
    coin_text = f"Coins: {coins_collected}/{total_coins}"
    screen.draw.text(coin_text, 
                 topleft=(20, 20),
                 fontsize=30, 
                 color="#FFD700",  # Gold
                 background="#2C1810")  # Dark brown
    

# Main update function
def update():
    global camera_x, camera_y
    
    if game_state == "PLAYING":
        if music_on and not music.is_playing('background_music'):
            music.play('background_music')
        player.handle_input()
        player.apply_physics()
        player.check_collisions()
        player.check_enemy_collision()
        
        # Update camera to follow player
        camera_x = max(0, player.actor.x - WIDTH // 2)
        camera_y = 0
        
        # Only update enemies that are near the camera view (with some buffer)
        update_range = WIDTH + 200  # Extra buffer beyond screen width
        for enemy in enemies:
            # Calculate distance from camera center
            distance_from_camera = abs(enemy.actor.x - (camera_x + WIDTH // 2))
            
            # Only update if enemy is within range
            if distance_from_camera < update_range:
                enemy.update()

# Handle mouse clicks
def on_mouse_down(pos):
    global game_state, music_on
    
    if game_state == "MENU":
        if button_start.collidepoint(pos):
            game_state = "PLAYING"
            reset_game()
            if music_on:
                music.play('background_music')
        elif button_music.collidepoint(pos):
            music_on = not music_on
        elif button_exit.collidepoint(pos):
            exit()

# Reset game to starting state
def reset_game():
    global camera_x, camera_y
    player.reset(100, 200)
    for enemy in enemies:
        enemy.reset()
    camera_x = 0
    camera_y = 0

pgzrun.go()