import math


def check_enemy_collision(enemy, enemy_sprites):
    for enemy2 in enemy_sprites:
        if enemy.rect.colliderect(enemy2) and enemy != enemy2:

            x_dist = enemy.rect.x - enemy2.rect.x
            y_dist = (enemy.rect.y - enemy2.rect.y) * -1
            distance_radius = math.sqrt((x_dist ** 2) + (y_dist ** 2))
            distance_limit = 30

            if distance_radius < distance_limit:
                distance_needed = distance_limit - distance_radius
                if x_dist == 0:
                    if y_dist > 0:
                        angle_needed = 90
                    else:
                        angle_needed = -90
                else:
                    angle_needed = math.degrees(math.atan(y_dist / x_dist))
                    if x_dist < 0 and y_dist < 0:
                        angle_needed += 180

                cos_x = math.cos(math.radians(angle_needed))
                sin_y = math.sin(math.radians(angle_needed))
                x_dist_needed = cos_x * distance_needed
                y_dist_needed = sin_y * distance_needed

                enemy.rect.y += y_dist_needed * -1
                enemy.rect.x += x_dist_needed
