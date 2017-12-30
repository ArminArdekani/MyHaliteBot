import hlt
import collections

def are_all_planets_full(planets_status):
	for planet_id, value in planets_status.items():
		if value[1] == False:
			return False
	return True

def closest_enemies(game_map, ship):
	closest_enemy_ships = []
	closest_enemy_planets = []
	free_planets = []
	entities_by_distance = game_map.nearby_entities_by_distance(ship)
	for distance in sorted(entities_by_distance):
		if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in game_map.get_me().all_ships():
			closest_enemy_ships.append(entities_by_distance[distance][0])
		elif isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].get_planet_owner() == None:
			free_planets.append(entities_by_distance[distance][0])
		elif isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned():
			closest_enemy_planets.append(entities_by_distance[distance][0])
	return [closest_enemy_ships, closest_enemy_planets, free_planets]