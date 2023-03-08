import pygame
from tiles import AnimatedSprite
from settings import tile_size, screen_height, screen_width

class Player:
    def __init__(self, x, y):
        idle_image_path = "graphics/character/Owlet_Monster_Idle_4.png"
        walk_image_path = "graphics/character/Owlet_Monster_Walk_6.png"
        run_image_path = "graphics/character/Owlet_Monster_Run_6.png"
        jump_image_path = "graphics/character/Owlet_Monster_Jump_8.png"
        dust_image_path = "graphics/character/Walk_Run_Push_Dust_6.png"

        self.idle_animation = AnimatedSprite(idle_image_path, tile_size, x, y, 4, 10)
        self.walk_animation = AnimatedSprite(walk_image_path, tile_size, x, y, 6, 10)
        self.run_animation = AnimatedSprite(run_image_path, tile_size, x, y, 6, 10)
        self.jump_animation = AnimatedSprite(jump_image_path, tile_size, x, y, 8, 10)
        self.dust_animation = AnimatedSprite(dust_image_path, tile_size, x, y, 6, 10)

        self.animations = {"idle": self.idle_animation,
                           "walk": self.walk_animation,
                           "run": self.run_animation,
                           "jump": self.jump_animation}

        self.current_animation = self.idle_animation
        self.current_animation.play()
        self.rect = pygame.Rect(x, y, self.current_animation.width, self.current_animation.height)

        self.move_speed = 5
        self.jump_speed = -10
        self.gravity = 0.5
        self.velocity_y = 0
        self.on_ground = False

    def update(self, keys, dt):
        # Update the animation based on the player's state
        if self.on_ground:
            if keys[pygame.K_a] or keys[pygame.K_d]:
                if keys[pygame.K_LSHIFT]:
                    self.current_animation = self.run_animation
                    self.move_speed = 8
                else:
                    self.current_animation = self.walk_animation
                    self.move_speed = 5
            else:
                self.current_animation = self.idle_animation
                self.move_speed = 0
        else:
            self.current_animation = self.jump_animation

        # Update the current animation
        self.current_animation.update(dt)

        # Update the player's position based on keyboard input
        if keys[pygame.K_a]:
            self.rect.x -= self.move_speed
        if keys[pygame.K_d]:
            self.rect.x += self.move_speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.on_ground = False
            self.current_animation = self.jump_animation
            self.current_animation.play()
            self.velocity_y = self.jump_speed

				# Apply gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

				# Check for collision with the bottom of the screen
        if self.rect.bottom >= screen_height:
          self.rect.bottom = screen_height
          self.velocity_y = 0
          self.on_ground = True

				# Draw dust animation when moving
        if self.move_speed > 0:
          dust_pos = (self.rect.x - 20, self.rect.y + self.current_animation.height - 20)
          self.dust_animation.draw(surface, *dust_pos)

        # Draw hitbox
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

    def collide_with_obstacle(self, obstacle_rect):
        """
        Check if the player collides with an obstacle.
        """
        if self.rect.colliderect(obstacle_rect):
            # Check if the player is above the obstacle
            if self.rect.bottom <= obstacle_rect.top + 10:
                self.rect.bottom = obstacle_rect.top
                self.on_ground = True
                self.velocity_y = 0
            # Check if the player is below the obstacle
            elif self.rect.top >= obstacle_rect.bottom - 10:
                self.rect.top = obstacle_rect.bottom
                self.velocity_y = 0
            # Check if the player is to the left of the obstacle
            elif self.rect.right <= obstacle_rect.left + 10:
                self.rect.right = obstacle_rect.left
            # Check if the player is to the right of the obstacle
            elif self.rect.left >= obstacle_rect.right - 10:
                self.rect.left = obstacle_rect.right

    def check_for_collisions(self, obstacles):
        """
        Check for collisions with obstacles.
        """
        for obstacle in obstacles:
            self.collide_with_obstacle(obstacle.rect)
            
    def draw(self, surface):
			# Draw the current animation
      self.current_animation.draw(surface, self.rect.x, self.rect.y)
			
			# Draw dust animation when moving
      if self.move_speed > 0:
        dust_pos = (self.rect.x - 20, self.rect.y + self.current_animation.height - 20)
        self.dust_animation.draw(surface, *dust_pos)
					
			# Draw hitbox
      pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

			# Draw collision box for debugging
      collision_rect = pygame.Rect(self.rect.x, self.rect.y + self.current_animation.height - 10, self.rect.width, 10)
      pygame.draw.rect(surface, (0, 255, 0), collision_rect, 2)   
