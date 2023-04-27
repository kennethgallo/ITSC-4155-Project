import pygame
from projectile import Projectile


class UpgradeMenu:
    def __init__(self, player, projectile):
        self.player = player
        self.projectile = projectile
        self.upgrade_items = {
            "Health Upgrade": {"cost":30, "effect": 10, "stat": "health"},
            "Damage Upgrade": {"cost": 100, "effect": 20, "stat": "damage"},
            "Speed Upgrade": {"cost": 50, "effect": 2, "stat": "speed"},
            "Projectile Upgrade": {"cost": 150, "effect": 1, "stat": "max_hits"}
        }

    def display_menu(self, screen):
        font = pygame.font.Font(None, 30)
        header = font.render("Upgrade Menu", True, (255, 255, 255))
        screen.blit(header, (300, 50))

        # Display current player money value
        money_text = font.render(f"Money: {self.player.money}", True, (255, 255, 255))
        screen.blit(money_text, (100, 100))

        x, y = 100, 150
        for item, data in self.upgrade_items.items():
            upgrade_name = font.render(item, True, (255, 255, 255))
            upgrade_cost = font.render(f"Cost: {data['cost']}", True, (255, 255, 255))
            screen.blit(upgrade_name, (x, y))
            screen.blit(upgrade_cost, (x, y + 30))
            y += 100

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
                        upgrade_rect = pygame.Rect(100, 150 + (100 * list(self.upgrade_items.keys()).index(item)), 200, 50)
                        if upgrade_rect.collidepoint(mouse_pos) and self.player.money >= data["cost"]:
                            self.player.money -= data["cost"]
                            Projectile.max_hits += data["effect"]
                            pygame.time.delay(500)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
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
