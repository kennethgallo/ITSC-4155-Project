import pygame
from projectile import Projectile


class UpgradeMenu:
    def __init__(self, player, projectile, window_width, window_height):
        self.player = player
        self.projectile = projectile
        self.window_width = window_width
        self.window_height = window_height
        self.upgrade_items = {
            "Health Upgrade": {"cost":30, "effect": 10, "stat": "health"},
            "Damage Upgrade": {"cost": 100, "effect": 20, "stat": "damage"},
            "Speed Upgrade": {"cost": 50, "effect": 2, "stat": "speed"},
            "Projectile Upgrade": {"cost": 150, "effect": 1, "stat": "max_hits"}
        }

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
            upgrade_name = upgrade_font.render(item, True, (0, 0, 0))
            upgrade_cost = upgrade_font.render(f"Cost: {data['cost']}", True, (50, 50, 50))
            name_location = upgrade_name.get_rect(center=(x, y))
            cost_location = upgrade_cost.get_rect(center=(x, y + 30))

            background_width = upgrade_name.get_size()[0] + upgrade_cost.get_size()[0]
            background_height = (upgrade_name.get_size()[1] + upgrade_cost.get_size()[1]) * 2
            background_size = (background_width, background_height)
            background = pygame.surface.Surface(background_size)
            background.fill('LightGray')
            background_location = background.get_rect(center=(x, y + 15))

            screen.blit(background, background_location)
            screen.blit(upgrade_name, name_location)
            screen.blit(upgrade_cost, cost_location)
            y += 100

        # tell user how to leave the menu
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
                        upgrade_rect = pygame.Rect(self.window_width / 2, 200 + (100 * list(self.upgrade_items.keys()).index(item)), 200, 50)
                        if upgrade_rect.collidepoint(mouse_pos) and self.player.money >= data["cost"]:
                            self.player.money -= data["cost"]
                            Projectile.max_hits += data["effect"]

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    # Check if key pressed corresponds to an upgrade, then update player stats and money
                    elif event.key == pygame.K_1:
                        if self.player.money >= self.upgrade_items["Health Upgrade"]["cost"]:
                            self.player.money -= self.upgrade_items["Health Upgrade"]["cost"]
                            self.player.health += self.upgrade_items["Health Upgrade"]["effect"]
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
