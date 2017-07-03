def attack(game, tile_acting, tile_effected):
    tile_effected.units -= 1
    if tile_effected.units == 0:
        tile_effected.owner = tile_acting.owner
    tile_acting.save()
    tile_effected.save()
    return tile_acting, tile_effected

def move(game, tile_acting, tile_effected, units_to_move):
    if tile_acting.owner == tile_effected.owner:
        tile_acting.units -= units_to_move
        tile_effected.units += units_to_move
        tile_acting.save()
        tile_effected.save()
        return tile_acting, tile_effected
    else:
        raise Exception('Units can only be moved between tiles of the same owner')
