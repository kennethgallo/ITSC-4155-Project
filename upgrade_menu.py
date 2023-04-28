import pygame
from projectile import Projectile
from button import ShopButton


class UpgradeMenu:
    def __init__(self, player, projectile, window_width, window_height):
        self.player = player
        self.projectile = projectile
        self.window_width = window_width
        self.window_height = window_height
        self.upgrade_items = {
            "Health Upgrade": {"cost": 60, "effect": 10, "stat": "start_health"},
            "Damage Upgrade": {"cost": 120, "effect": 20, "stat": "damage"},
            "Speed Upgrade": {"cost": 50, "effect": 1.25, "stat": "speed"},
            "Projectile Upgrade": {"cost": 80, "effect": 1, "stat": "max_hits"}
        }
        self.upgrade_buttons = {}

    def display_menu(self, screen):
        header_font = pygame.font.Font(None, 45)
        header = header_font.render("Upgrade Menu", True, (255, 255, 255))
        header_location = header.get_rect(center=(self.window_width / 2, 50))
        screen.blit(header, header_location)

        # Display current player money value
        money_font = pygame.font.Font(None, 35)
        money_text = money_font.render(f"Money: {self.player.money}", True, (255, 255, 255))
        money_text_location = money_text.get_rect(center=(self.window_width / 2, 100))
        screen.blit(money_text, money_text_location)

        upgrade_font = pygame.font.Font(None, 28)
        x, y = self.window_width / 2, 200
        for item, data in self.upgrade_items.items():

            button = ShopButton(item, f'Cost: {data["cost"]}')
            button.rect.center = (x, y)
            self.upgrade_buttons[item] = button

            screen.blit(button.image, button.rect)
            y += 100

        # Prompt to tell the user how to leave the menu
        smaller_font = pygame.font.Font(None, 25)
        close_menu_text = smaller_font.render('Press Escape to close', True, (200, 200, 200))
        close_menu_text_location = close_menu_text.get_rect(center=(self.window_width / 2, self.window_height - 100))
        screen.blit(close_menu_text, close_menu_text_location)

    def run_menu(self):
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()

        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if selected upgrade is affordable, then update player stats and money
                    for item, data in self.upgrade_items.items():

                        # grab the button corresponding to the item
                        button = self.upgrade_buttons[item]

                        # check for collision with button and if player has enough money
                        if button.rect.collidepoint(mouse_pos) and self.player.money >= data["cost"]:
                            self.player.money -= data["cost"]
                            if data["stat"] == 'max_hits':
                                Projectile.max_hits += data["effect"]
                            else:
                                setattr(self.player, data["stat"], getattr(self.player, data["stat"]) + data["effect"])
                                if data["stat"] == 'start_health':
                                    self.player.health = self.player.start_health

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    # Check if key pressed corresponds to an upgrade, then update player stats and money
                    elif event.key == pygame.K_1:
                        if self.player.money >= self.upgrade_items["Health Upgrade"]["cost"]:
                            self.player.money -= self.upgrade_items["Health Upgrade"]["cost"]
                            self.player.start_health += self.upgrade_items["Health Upgrade"]["effect"]
                            self.player.health = self.player.start_health
                    elif event.key == pygame.K_2:
                        if self.player.money >= self.upgrade_items["Damage Upgrade"]["cost"]:
                            self.player.money -= self.upgrade_items["Damage Upgrade"]["cost"]
                            self.player.damage += self.upgrade_items["Damage Upgrade"]["effect"]
                    elif event.key == pygame.K_3:
                        if self.player.money >= self.upgrade_items["Speed Upgrade"]["cost"]:
                            self.player.money -= self.upgrade_items["Speed Upgrade"]["cost"]
                            self.player.speed += self.upgrade_items["Speed Upgrade"]["effect"]
                    elif event.key == pygame.K_4:
                        if self.player.money >= self.upgrade_items["Projectile Upgrade"]["cost"]:
                            self.player.money -= self.upgrade_items["Projectile Upgrade"]["cost"]
                            Projectile.max_hits += self.upgrade_items["Projectile Upgrade"]["effect"]

            # Draw menu and update display
            screen.fill((0, 0, 0))
            self.display_menu(screen)
            pygame.display.flip()
            clock.tick(60)
