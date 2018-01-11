import hlt
import collections

def are_all_planets_full(planets_status):
	for planet_id, value in planets_status.items():
		if value[1] == False:
			return False
	return True
	
def get_free_planet(planets_status):
	for planet_id, value in planets_status.items():
		if value[1] == False:
			return value[0]
	return None

def closest_enemies(game_map, ship):
	closest_enemy_ships = []
	closest_enemy_planets = []
	free_planets = []
	owned_not_full_planets = []
	entities_by_distance = game_map.nearby_entities_by_distance(ship)
	for distance in sorted(entities_by_distance):
		if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in game_map.get_me().all_ships():
			closest_enemy_ships.append(entities_by_distance[distance][0])
		elif isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].get_planet_owner() == None:
			free_planets.append(entities_by_distance[distance][0])
		elif isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned():
			closest_enemy_planets.append(entities_by_distance[distance][0])
		elif isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and entities_by_distance[distance][0].get_planet_owner() == game_map.get_me() and not entities_by_distance[distance][0].is_full():
			owned_not_full_planets.append(entities_by_distance[distance][0])
	return [closest_enemy_ships, closest_enemy_planets, free_planets, owned_not_full_planets]
	
def best_planet(owned_not_full_planets, percentage):
	for planet in owned_not_full_planets:
		if planet.percentage_full() < percentage:
			return planet
	return None

def best_planet_selection(owned_not_full_planets, ship_planet_assignment, ship_id, target_percentage):
	if ship_planet_assignment == None:
		return None
	
	best_planets = []
	for planet in owned_not_full_planets:
		score = planet.percentage_full_adjustment(ships_headed_to_planet(ship_planet_assignment, planet.get_id()))
		if score <= target_percentage:
			best_planets.append([planet,score])
			
	return best_planets[0][0] if len(best_planets) > 0 else None
		
def ships_headed_to_planet(ship_planet_assignment, planet_id):
	i = 0
	for key, value in ship_planet_assignment.items():
		if value[0] == planet_id:
			i+=1
	return i