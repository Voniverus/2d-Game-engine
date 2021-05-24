import numpy as np
import math

import Entities
import Globals
import Collider


class RigidBody:
	def __init__(self, position, mass, drag):
		self.type = "dynamic"
		self.position = position
		self.velocity = np.array([0.0, 0.0])
		self.previousVelocity = self.velocity
		self.acceleration = np.array([0.0, 0.0])
		self.coefficientOfFriction = 0.4
		self.mass = mass
		self.drag = drag
		
class RigidBodyStatic:
	def __init__(self, position):
		self.type = "static"
		self.position = position
		self.velocity = np.array([0.0, 0.0])
		self.acceleration = np.array([0.0, 0.0])
		self.coefficientOfFriction = 0.4

class CollisionDetails:
	def __init__(self, collides, collisionDistance, collisionPointObject1, collisionPointObject2, reactionVectorObject1, reactionVectorObject2):
		self.collides = collides
		self.collisionDistance = collisionDistance
		self.collisionPointObject1 = collisionPointObject1
		self.collisionPointObject2 = collisionPointObject2
		self.reactionVectorObject1 = reactionVectorObject1
		self.reactionVectorObject2 = reactionVectorObject2

	def swapObjects(self):
		aux = 0
		
		aux = self.collisionPointObject1[0]
		self.collisionPointObject1[0] = self.collisionPointObject2[0]
		self.collisionPointObject2[0] = aux
		aux = self.collisionPointObject1[1]
		self.collisionPointObject1[1] = self.collisionPointObject2[1]
		self.collisionPointObject2[1] = aux

		aux = self.reactionVectorObject1[0]
		self.reactionVectorObject1[0] = self.reactionVectorObject2[0]
		self.reactionVectorObject2[0] = aux
		aux = self.reactionVectorObject1[1]
		self.reactionVectorObject1[1] = self.reactionVectorObject2[1]
		self.reactionVectorObject2[1] = aux

	def swappedObjects(self):
		return CollisionDetails(self.collides, self.collisionDistance, self.collisionPointObject2, self.collisionPointObject1, self.reactionVectorObject2, self.reactionVectorObject1)


class RayCastDetails:
	def __init__(self, collides, intercept, distance):
		self.collides = collides
		self.intercept = intercept
		self.distance = distance


class ShapeCastDetails:
	def __init__(self, collides, collisionPoint):
		self.collides = collides
		self.collisionPoint = collisionPoint


def rayCast(position, direction, maxDistance, player):
	direction = direction / np.linalg.norm(direction)

	#Debug
	Globals.objects.append(Entities.SpriteLine(position[0], position[1], position[0] + direction[0] * maxDistance, position[1] + direction[1] * maxDistance, (200, 0, 0)))
	
	targets = []
	collisionPoints = []
	
	type = "angled"

	if direction[0] != 0 and direction[1] != 0:
		
		for obj in Globals.gameObjects:			
			if obj != player:
				if obj.shape == "poly":
					
					if direction[0] < 0:
						
						if direction[1] < 0:
							if obj.rigidBody.position[0] + obj.collider.mostLeftPoint()[0] < position[0] and obj.rigidBody.position[1] + obj.collider.mostUpPoint()[1] < position[1]:
								targets.append(obj)

						elif direction[1] > 0:
							if obj.rigidBody.position[0] + obj.collider.mostLeftPoint()[0] < position[0] and obj.rigidBody.position[1] + obj.collider.mostDownPoint()[1] > position[1]:
								targets.append(obj)

					elif direction[0] > 0:
						if direction[1] < 0:
							if obj.rigidBody.position[0] + obj.collider.mostRightPoint()[0] > position[0] and obj.rigidBody.position[1] + obj.collider.mostUpPoint()[1] < position[1]:
								targets.append(obj)

						elif direction[1] > 0:
							if obj.rigidBody.position[0] + obj.collider.mostRightPoint()[0] > position[0] and obj.rigidBody.position[1] + obj.collider.mostDownPoint()[1] > position[1]:
								targets.append(obj)


				elif obj.shape == "circle":
					if direction[0] < 0:
						if direction[1] < 0:
							if obj.rigidBody.position[0] - obj.collider.radius < position[0] and obj.rigidBody.position[1] - obj.collider.radius < position[1]:
								targets.append(obj)

						elif direction[1] > 0:
							if obj.rigidBody.position[0] - obj.collider.radius < position[0] and obj.rigidBody.position[1] + obj.collider.radius > position[1]:
								targets.append(obj)

					elif direction[0] > 0:
						if direction[1] < 0:
							if obj.rigidBody.position[0] + obj.collider.radius > position[0] and obj.rigidBody.position[1] - obj.collider.radius < position[1]:
								targets.append(obj)

						elif direction[1] > 0:
							if obj.rigidBody.position[0] + obj.collider.radius > position[0] and obj.rigidBody.position[1] + obj.collider.radius > position[1]:
								targets.append(obj)


	elif direction[1] == 0:
		for obj in Globals.gameObjects:
			if obj != player:
				if obj.shape == "poly":
					if (direction[0] < 0 and position[0] >= obj.rigidBody.position[0] + obj.collider.mostLeftPoint()[0]):
						type = "horizontal"
						targets.append(obj)

					elif (direction[0] > 0 and position[0] <= obj.rigidBody.position[0] + obj.collider.mostRightPoint()[0]):
						type = "horizontal"
						targets.append(obj)

				elif obj.shape == "circle":
					if (direction[0] < 0 and position[0] >= obj.rigidBody.position[0] - obj.collider.radius):
						type = "horizontal"
						targets.append(obj)

					elif (direction[0] > 0 and position[0] <= obj.rigidBody.position[0] + obj.collider.radius):
						type = "horizontal"
						targets.append(obj)

	elif direction[0] == 0:
		for obj in Globals.gameObjects:
			if obj != player:
				if obj.shape == "poly":
					if (direction[1] < 0 and position[1] >= obj.rigidBody.position[1] + obj.collider.mostUpPoint()[1]):
						type = "vertical"
						targets.append(obj)
					elif (direction[1] > 0 and position[1] <= obj.rigidBody.position[1] + obj.collider.mostDownPoint()[1]):
						type = "vertical"
						targets.append(obj)

				elif obj.shape == "circle":
					if (direction[1] < 0 and position[1] >= obj.rigidBody.position[1] - obj.collider.radius):
						type = "vertical"
						targets.append(obj)
					elif (direction[1] > 0 and position[1] <= obj.rigidBody.position[1] + obj.collider.radius):
						type = "vertical"
						targets.append(obj)


	if len(targets) == 0:
		return RayCastDetails(False, np.array([0.0, 0.0]), 0.0)

	if type == "angled":
		a1 = direction[1]
		b1 = -direction[0]
		c1 = (direction[1] * position[0] + -position[1] * direction[0])
		
		for obj in targets:
			if obj.shape == "poly":
				for i in range(len(obj.collider.getCollisionPoints())):
					j = (i + 1) if i != (len(obj.collider.getCollisionPoints()) - 1) else 0
					x1 = obj.rigidBody.position[0] + obj.collider.points[i][0]
					y1 = obj.rigidBody.position[1] + obj.collider.points[i][1]
					x2 = obj.rigidBody.position[0] + obj.collider.points[j][0]
					y2 = obj.rigidBody.position[1] + obj.collider.points[j][1]

					determinant = 0

					if obj.collider.points[i][0] != obj.collider.points[j][0] and obj.collider.points[i][1] != obj.collider.points[j][1]:
						a2 = y2 - y1
						b2 = x1 - x2
						c2 = a2 * x1 + b2 * y1
						determinant = a1 * b2 - a2 * b1

						if determinant != 0:
							x = (b2 * c1 - b1 * c2) / determinant
							y = (a1 * c2 - a2 * c1) / determinant

					elif obj.collider.points[i][1] != obj.collider.points[j][1]: 
						determinant = 1
						x = x1
						y = (direction[1] / direction[0]) * (x - position[0]) + position[1]

					elif obj.collider.points[i][0] != obj.collider.points[j][0]:
						determinant = 1	
						y = y1
						x = (direction[0] / direction[1]) * (y - position[1]) + position[0]

					if determinant != 0:
						if ((x1 <= x <= x2 or x2 <= x <= x1) and (y1 <= y <= y2 or y2 <= y <= y1)):
							collisionPoints.append(np.array([x, y]))

			elif obj.shape == "circle":
				center = obj.rigidBody.position    # Centre of circle
				radius = obj.collider.radius       # Radius of circle

				a = np.dot(direction, direction)
				b = 2 * np.dot(direction, position - center)
				c = np.dot(position, position) + np.dot(center, center) - 2 * np.dot(position, center) - radius ** 2

				discriminant = b ** 2 - 4 * a * c

				if discriminant >= 0:
					sqrtDiscriminant = math.sqrt(discriminant)
					t1 = (-b + sqrtDiscriminant) / (2 * a)
					t2 = (-b - sqrtDiscriminant) / (2 * a)

					if 0 <= t1 <= 1 or 0 <= t2 <= 1:
						t = max(0, min(1, - b / (2 * a)))
						collisionPoints.append(np.array([position[0] + t * direction[0], position[1] + t * direction[1]]))

	elif type == "horizontal":
		for obj in targets:
			if obj.shape == "poly":
				for i in range(len(obj.collider.getCollisionPoints())):
					j = (i + 1) if i != (len(obj.collider.getCollisionPoints()) - 1) else 0
					x1 = obj.rigidBody.position[0] + obj.collider.points[i][0]
					y1 = obj.rigidBody.position[1] + obj.collider.points[i][1]
					x2 = obj.rigidBody.position[0] + obj.collider.points[j][0]
					y2 = obj.rigidBody.position[1] + obj.collider.points[j][1]

					if (y1 <= position[1] <= y2 or
						y2 <= position[1] <= y1):
						if x1 != x2 and y1 != y2:
							x = (x2 - x1) / (y2 - y1) * (position[1] - y1) + x1
						else:
							x = x1
						collisionPoints.append(np.array([x, position[1]]))

			elif obj.shape == "circle":
				center = obj.rigidBody.position    # Centre of circle
				radius = obj.collider.radius       # Radius of circle

				a = np.dot(direction, direction)
				b = 2 * np.dot(direction, position - center)
				c = np.dot(position, position) + np.dot(center, center) - 2 * np.dot(position, center) - radius ** 2

				discriminant = b ** 2 - 4 * a * c

				if discriminant >= 0:
					sqrtDiscriminant = math.sqrt(discriminant)
					t1 = (-b + sqrtDiscriminant) / (2 * a)
					t2 = (-b - sqrtDiscriminant) / (2 * a)

					if 0 <= t1 <= 1 or 0 <= t2 <= 1:
						t = max(0, min(1, - b / (2 * a)))
						collisionPoints.append(np.array([position[0] + t * direction[0], position[1] + t * direction[1]]))

	elif type == "vertical":
		for obj in targets:
			if obj.shape == "poly":
				for i in range(len(obj.collider.getCollisionPoints())):
					j = (i + 1) if i != (len(obj.collider.getCollisionPoints()) - 1) else 0
					x1 = obj.rigidBody.position[0] + obj.collider.points[i][0]
					y1 = obj.rigidBody.position[1] + obj.collider.points[i][1]
					x2 = obj.rigidBody.position[0] + obj.collider.points[j][0]
					y2 = obj.rigidBody.position[1] + obj.collider.points[j][1]
					
					if (x1 <= position[0] <= x2 or
						x2 <= position[0] <= x1):
						y = (y2 - y1) / (x2 - x1) * (position[0] - x1) + y1
						collisionPoints.append(np.array([position[0], y]))

			elif obj.shape == "circle":
				center = obj.rigidBody.position    # Centre of circle
				radius = obj.collider.radius       # Radius of circle

				a = np.dot(direction, direction)
				b = 2 * np.dot(direction, position - center)
				c = np.dot(position, position) + np.dot(center, center) - 2 * np.dot(position, center) - radius ** 2

				discriminant = b ** 2 - 4 * a * c

				if discriminant >= 0:
					sqrtDiscriminant = math.sqrt(discriminant)
					t1 = (-b + sqrtDiscriminant) / (2 * a)
					t2 = (-b - sqrtDiscriminant) / (2 * a)

					if 0 <= t1 <= 1 or 0 <= t2 <= 1:
						t = max(0, min(1, - b / (2 * a)))
						collisionPoints.append(np.array([position[0] + t * direction[0], position[1] + t * direction[1]]))


	toReturn = RayCastDetails(False, np.array([0.0, 0.0]), 0.0)

	lowestDistance = float('inf')
	for point in collisionPoints:
		if math.hypot(position[0] - point[0], position[1] - point[1]) < lowestDistance and math.hypot(position[0] - point[0], position[1] - point[1]) < maxDistance:
			toReturn.collides = True
			lowestDistance = math.hypot(position[0] - point[0], position[1] - point[1])
			toReturn.intercept = point
	
	return toReturn


def circleCast(position, direction, maxDistance, radius, player):
	direction = direction / np.linalg.norm(direction)

	toReturn = ShapeCastDetails(False, np.array([0, 0]))
	collisionDetails = CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))
	collider = Entities.CollisionCircle(position[0], position[1], radius)

	#Debug
	Globals.objects.append(Entities.SpriteCircle("circle cast", collider.rigidBody.position[0], collider.rigidBody.position[1], radius, (200, 0, 0)))

	while(not toReturn.collides and math.hypot(position[0] - collider.rigidBody.position[0], position[1] - collider.rigidBody.position[1]) <= maxDistance):
		collider.rigidBody.position += direction
		Globals.objects.append(Entities.SpriteCircle("circle cast", collider.rigidBody.position[0], collider.rigidBody.position[1], radius, (200, 0, 0)))
		for obj in Globals.gameObjects:
			if obj != player:
				collisionDetails = objectsCollide(collider, obj)
				if collisionDetails.collides:
					toReturn.collides = True
					
					toReturn.collisionPoint = collisionDetails.collisionPointObject1
					break
	
	return toReturn


def PolyCast(position, direction, points, maxDistance, player):
	direction = direction / np.linalg.norm(direction)


	toReturn = ShapeCastDetails(False, np.array([0, 0]))
	collisionDetails = CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))
	collider = Entities.CollisionPoly(np.array([position[0], position[1]]), points, Collider.Tag.BARRIER)

	while(not toReturn.collides and math.hypot(position[0] - collider.rigidBody.position[0], position[1] - collider.rigidBody.position[1]) <= maxDistance):
		Globals.objects.append(Entities.SpritePoly(collider.rigidBody.position, points, (200, 0, 0)))
		for obj in Globals.gameObjects:
			if obj != player:
				collisionDetails = objectsCollide(collider, obj)
				if collisionDetails.collides:
					toReturn.collides = True
					
					toReturn.collisionPoint = collisionDetails.collisionPointObject1
					break	
		
		collider.rigidBody.position += direction

	return toReturn


def getProjectedPointOnLine(point, line):
	x = ((point[0] * line[0] + point[1] * line[1]) / (line[0] * line[0] + line[1] * line[1])) * line[0]
	y = ((point[0] * line[0] + point[1] * line[1]) / (line[0] * line[0] + line[1] * line[1])) * line[1]

	return np.array([x, y])


def dotProduct(point1, point2):
	return point1[0] * point2[0] + point1[1] * point2[1]


def collidesOnAxisPolyPoly(lineVector, obj1Points, obj2Points, positionDifference):
	obj1Min = float('inf')
	obj1Max = float('-inf')
	obj2Min = float('inf')
	obj2Max = float('-inf')

	obj1Distances = np.empty(16, dtype = float)
	obj2Distances = np.empty(16, dtype = float)

	for i in range(0, len(obj1Points)):
		projected = getProjectedPointOnLine(obj1Points[i], lineVector)
		
		distanceOnLine = math.sqrt(projected[0] * projected[0] + projected[1] * projected[1])
		if projected[0] + projected[1] < 0:
			distanceOnLine = -distanceOnLine

		obj1Distances[i] = distanceOnLine

		if obj1Min > distanceOnLine:
			obj1Min = distanceOnLine
			obj1MinPoint = i

		if obj1Max < distanceOnLine:
			obj1Max = distanceOnLine
			obj1MaxPoint = i


	for i in range(0, len(obj2Points)):
		adjustedPoint = np.array([obj2Points[i][0] + positionDifference[0],
								  obj2Points[i][1] + positionDifference[1]])

		projected = getProjectedPointOnLine(adjustedPoint, lineVector)

		distanceOnLine = math.sqrt(projected[0] * projected[0] + projected[1] * projected[1])
		if projected[0] + projected[1] < 0:
			distanceOnLine = -distanceOnLine

		obj2Distances[i] = distanceOnLine

		if obj2Min > distanceOnLine:
			obj2Min = distanceOnLine
			obj2MinPoint = i

		if obj2Max < distanceOnLine:
			obj2Max = distanceOnLine
			obj2MaxPoint = i

	toReturn = CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))

	if obj1Max <= obj2Min or obj2Max <= obj1Min:
		toReturn.collides = False
	else:
		toReturn.collides = True
		toReturn.collisionDistance = min(abs(obj1Max - obj2Min), abs(obj1Min - obj2Max))
		toReturn.collisionPointObject1[0] = 0
		toReturn.collisionPointObject1[1] = 0
		toReturn.collisionPointObject2[0] = 0
		toReturn.collisionPointObject2[1] = 0

		vectorLength = math.sqrt(lineVector[0] * lineVector[0] + lineVector[1] * lineVector[1])

		if abs(obj1Max - obj2Min) < abs(obj1Min - obj2Max):
			minDistanceToOtherObject = float('inf')
			noObj1LinePoints = 0
			closestObj1Point = np.array([0.0, 0.0])

			for i in range(0, len(obj1Points)):
				if abs(obj1Distances[i] - obj1Distances[obj1MaxPoint]) < 0.01:
					distanceToOtherObject = math.sqrt(((obj1Points[i][0] - positionDifference[0]) ** 2) + ((obj1Points[i][1] - positionDifference[1]) ** 2))
					if minDistanceToOtherObject > distanceToOtherObject:
						minDistanceToOtherObject = distanceToOtherObject
						closestObj1Point = obj1Points[i]

					noObj1LinePoints += 1

			minDistanceToOtherObject = float('inf')
			noObj2LinePoints = 0
			closestObj2Point = np.array([0.0, 0.0])

			for i in range(0, len(obj2Points)):
				if abs(obj2Distances[i] - obj2Distances[obj2MinPoint]) < 0.01:
					distanceToOtherObject = math.sqrt(((obj2Points[i][0] + positionDifference[0]) ** 2) + ((obj2Points[i][1] + positionDifference[1]) ** 2))
					if minDistanceToOtherObject > distanceToOtherObject:
						minDistanceToOtherObject = distanceToOtherObject
						closestObj2Point = obj2Points[i]

					noObj2LinePoints += 1

			if noObj1LinePoints == 1 and noObj2LinePoints > 1:
				toReturn.collisionPointObject1[0] = obj1Points[obj1MaxPoint][0]
				toReturn.collisionPointObject1[1] = obj1Points[obj1MaxPoint][1]
				toReturn.reactionVectorObject1[0] = lineVector[0] / vectorLength * toReturn.collisionDistance
				toReturn.reactionVectorObject1[1] = lineVector[1] / vectorLength * toReturn.collisionDistance
				
				if dotProduct(toReturn.reactionVectorObject1, toReturn.collisionPointObject1) > 0:
					toReturn.reactionVectorObject1[0] = -toReturn.reactionVectorObject1[0]
					toReturn.reactionVectorObject1[1] = -toReturn.reactionVectorObject1[1]

				toReturn.collisionPointObject2[0] = toReturn.collisionPointObject1[0] - positionDifference[0] + toReturn.reactionVectorObject1[0]
				toReturn.collisionPointObject2[1] = toReturn.collisionPointObject1[1] - positionDifference[1] + toReturn.reactionVectorObject1[1]
				toReturn.reactionVectorObject2[0] = -toReturn.reactionVectorObject1[0]
				toReturn.reactionVectorObject2[1] = -toReturn.reactionVectorObject1[1]
			

			if noObj1LinePoints > 1 and noObj2LinePoints == 1:
				toReturn.collisionPointObject2[0] = obj2Points[obj2MinPoint][0]
				toReturn.collisionPointObject2[1] = obj2Points[obj2MinPoint][1]
				toReturn.reactionVectorObject2[0] = lineVector[0] / vectorLength * toReturn.collisionDistance
				toReturn.reactionVectorObject2[1] = lineVector[1] / vectorLength * toReturn.collisionDistance
				
				if dotProduct(toReturn.reactionVectorObject2, toReturn.collisionPointObject2) > 0:
					toReturn.reactionVectorObject2[0] = -toReturn.reactionVectorObject2[0]
					toReturn.reactionVectorObject2[1] = -toReturn.reactionVectorObject2[1]
				
				toReturn.collisionPointObject1[0] = toReturn.collisionPointObject2[0] + positionDifference[0] + toReturn.reactionVectorObject2[0]
				toReturn.collisionPointObject1[1] = toReturn.collisionPointObject2[1] + positionDifference[1] + toReturn.reactionVectorObject2[1]
				toReturn.reactionVectorObject1[0] = -toReturn.reactionVectorObject2[0]
				toReturn.reactionVectorObject1[1] = -toReturn.reactionVectorObject2[1]
			

			if noObj1LinePoints > 1 and noObj2LinePoints > 1:
				toReturn.collisionPointObject1[0] = closestObj1Point[0]
				toReturn.collisionPointObject1[1] = closestObj1Point[1]
				toReturn.reactionVectorObject1[0] = lineVector[0] / vectorLength * toReturn.collisionDistance
				toReturn.reactionVectorObject1[1] = lineVector[1] / vectorLength * toReturn.collisionDistance

				if dotProduct(toReturn.reactionVectorObject1, toReturn.collisionPointObject1) > 0:
					toReturn.reactionVectorObject1[0] = -toReturn.reactionVectorObject1[0]
					toReturn.reactionVectorObject1[1] = -toReturn.reactionVectorObject1[1]
				
				toReturn.collisionPointObject2[0] = closestObj2Point[0]
				toReturn.collisionPointObject2[1] = closestObj2Point[1]
				toReturn.reactionVectorObject2[0] = lineVector[0] / vectorLength * toReturn.collisionDistance
				toReturn.reactionVectorObject2[1] = lineVector[1] / vectorLength * toReturn.collisionDistance

				if dotProduct(toReturn.reactionVectorObject2, toReturn.collisionPointObject2) > 0:
					toReturn.reactionVectorObject2[0] = -toReturn.reactionVectorObject2[0]
					toReturn.reactionVectorObject2[1] = -toReturn.reactionVectorObject2[1]
				
		else:
			minDistanceToOtherObject = float('inf')
			noObj1LinePoints = 0
			closestObj1Point = np.array([0.0, 0.0])
			for i in range(0, len(obj1Points)):
				if abs(obj1Distances[i] - obj1Distances[obj1MinPoint]) < 0.01:
					distanceToOtherObject = math.sqrt(((obj1Points[i][0] - positionDifference[0]) ** 2) + ((obj1Points[i][1] - positionDifference[1]) ** 2))

					if minDistanceToOtherObject > distanceToOtherObject:
						minDistanceToOtherObject = distanceToOtherObject
						closestObj1Point = obj1Points[i]
					
					noObj1LinePoints += 1
				
			minDistanceToOtherObject = float('inf')
			noObj2LinePoints = 0
			closestObj2Point = np.array([0.0, 0.0])

			for i in range(0, len(obj2Points)):
				if abs(obj2Distances[i] - obj2Distances[obj2MaxPoint]) < 0.01:
					distanceToOtherObject = math.sqrt(((obj2Points[i][0] + positionDifference[0]) ** 2) + ((obj2Points[i][1] + positionDifference[1]) ** 2))
					if minDistanceToOtherObject > distanceToOtherObject:
						minDistanceToOtherObject = distanceToOtherObject
						closestObj2Point = obj2Points[i]
					
					noObj2LinePoints += 1
				
			if (noObj1LinePoints == 1 and noObj2LinePoints > 1):
				toReturn.collisionPointObject1[0] = obj1Points[obj1MinPoint][0]
				toReturn.collisionPointObject1[1] = obj1Points[obj1MinPoint][1]
				toReturn.reactionVectorObject1[0] = lineVector[0] / vectorLength * toReturn.collisionDistance
				toReturn.reactionVectorObject1[1] = lineVector[1] / vectorLength * toReturn.collisionDistance

				if (dotProduct(toReturn.reactionVectorObject1, toReturn.collisionPointObject1) > 0):
					toReturn.reactionVectorObject1[0] = -toReturn.reactionVectorObject1[0]
					toReturn.reactionVectorObject1[1] = -toReturn.reactionVectorObject1[1]
				

				toReturn.collisionPointObject2[0] = toReturn.collisionPointObject1[0] - positionDifference[0] + toReturn.reactionVectorObject1[0]
				toReturn.collisionPointObject2[1] = toReturn.collisionPointObject1[1] - positionDifference[1] + toReturn.reactionVectorObject1[1]
				toReturn.reactionVectorObject2[0] = -toReturn.reactionVectorObject1[0]
				toReturn.reactionVectorObject2[1] = -toReturn.reactionVectorObject1[1]
			

			if (noObj1LinePoints > 1 or noObj2LinePoints == 1):
				toReturn.collisionPointObject2[0] = obj2Points[obj2MaxPoint][0]
				toReturn.collisionPointObject2[1] = obj2Points[obj2MaxPoint][1]
				toReturn.reactionVectorObject2[0] = lineVector[0] / vectorLength * toReturn.collisionDistance
				toReturn.reactionVectorObject2[1] = lineVector[1] / vectorLength * toReturn.collisionDistance

				if (dotProduct(toReturn.reactionVectorObject2, toReturn.collisionPointObject2) > 0):
					toReturn.reactionVectorObject2[0] = -toReturn.reactionVectorObject2[0]
					toReturn.reactionVectorObject2[1] = -toReturn.reactionVectorObject2[1]
			
				toReturn.collisionPointObject1[0] = toReturn.collisionPointObject2[0] + positionDifference[0] + toReturn.reactionVectorObject2[0]
				toReturn.collisionPointObject1[1] = toReturn.collisionPointObject2[1] + positionDifference[1] + toReturn.reactionVectorObject2[1]
				toReturn.reactionVectorObject1[0] = -toReturn.reactionVectorObject2[0]
				toReturn.reactionVectorObject1[1] = -toReturn.reactionVectorObject2[1]
			
			if noObj1LinePoints > 1 and noObj2LinePoints > 1:
				toReturn.collisionPointObject1[0] = closestObj1Point[0]
				toReturn.collisionPointObject1[1] = closestObj1Point[1]
				toReturn.reactionVectorObject1[0] = lineVector[0] / vectorLength * toReturn.collisionDistance
				toReturn.reactionVectorObject1[1] = lineVector[1] / vectorLength * toReturn.collisionDistance

				if dotProduct(toReturn.reactionVectorObject1, toReturn.collisionPointObject1) > 0:
					toReturn.reactionVectorObject1[0] = -toReturn.reactionVectorObject1[0]
					toReturn.reactionVectorObject1[1] = -toReturn.reactionVectorObject1[1]
				
				toReturn.collisionPointObject2[0] = closestObj2Point[0]
				toReturn.collisionPointObject2[1] = closestObj2Point[1]
				toReturn.reactionVectorObject2[0] = lineVector[0] / vectorLength * toReturn.collisionDistance
				toReturn.reactionVectorObject2[1] = lineVector[1] / vectorLength * toReturn.collisionDistance

				if dotProduct(toReturn.reactionVectorObject2, toReturn.collisionPointObject2) > 0:
					toReturn.reactionVectorObject2[0] = -toReturn.reactionVectorObject2[0]
					toReturn.reactionVectorObject2[1] = -toReturn.reactionVectorObject2[1]

	return toReturn


def collidesOnAxisPolyCircle(lineVector, obj1Points, obj2Radius, positionDifference):
	obj1Min = float('inf')
	obj1Max = float('-inf')
	obj2Min = float('inf')
	obj2Max = float('-inf')

	for i in range(0, len(obj1Points)):
		projected = getProjectedPointOnLine(obj1Points[i], lineVector)

		distanceOnLine = math.sqrt(projected[0] * projected[0] + projected[1] * projected[1])
		if projected[0] + projected[1] < 0:
			distanceOnLine = -distanceOnLine

		if obj1Min > distanceOnLine:
			obj1Min = distanceOnLine

		if obj1Max < distanceOnLine:
			obj1Max = distanceOnLine

	projected = getProjectedPointOnLine(positionDifference, lineVector)
	distanceOnLine = math.sqrt(projected[0] * projected[0] + projected[1] * projected[1])

	if projected[0] + projected[1] < 0:
		distanceOnLine = -distanceOnLine

	obj2Min = distanceOnLine - obj2Radius
	obj2Max = distanceOnLine + obj2Radius

	if obj1Max < obj2Min or obj2Max < obj1Min:
		toReturn = CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))
		toReturn.collides = False
		return toReturn

	vectorLength = math.sqrt(lineVector[0] * lineVector[0] + lineVector[1] * lineVector[1])
	collX = lineVector[0] / vectorLength * obj2Radius
	collY = lineVector[1] / vectorLength * obj2Radius

	if dotProduct(positionDifference, np.array([collX, collY])) > 0:
		collX = -collX
		collY = -collY

	toReturn = CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))
	toReturn.collides = True
	toReturn.collisionDistance = min(abs(obj1Max - obj2Min), abs(obj1Min - obj2Max))

	toReturn.collisionPointObject2[0] = collX
	toReturn.collisionPointObject2[1] = collY
	toReturn.reactionVectorObject2[0] = lineVector[0] / vectorLength * toReturn.collisionDistance
	toReturn.reactionVectorObject2[1] = lineVector[1] / vectorLength * toReturn.collisionDistance

	if (dotProduct(toReturn.reactionVectorObject2, np.array([collX - positionDifference[0], collY - positionDifference[1]])) > 0):
		toReturn.reactionVectorObject2[0] = -toReturn.reactionVectorObject2[0]
		toReturn.reactionVectorObject2[1] = -toReturn.reactionVectorObject2[1]

	toReturn.collisionPointObject1[0] = collX + positionDifference[0] + toReturn.reactionVectorObject2[0]
	toReturn.collisionPointObject1[1] = collY + positionDifference[1] + toReturn.reactionVectorObject2[1]
	toReturn.reactionVectorObject1[0] = -toReturn.reactionVectorObject2[0]
	toReturn.reactionVectorObject1[1] = -toReturn.reactionVectorObject2[1]

	return toReturn


def objectsCollide(object1, object2):

	if object2.collider.tag not in Globals.tagValues[object1.collider.tag]:
		return CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))



	if object1.shape == "none" or object2.shape == "none":
		return CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))


	# Poly to Poly
	if object1.shape == "poly" and object2.shape == "poly":

		point1 = object1.rigidBody.position
		point2 = object2.rigidBody.position

		positionDiff = np.array([point2[0] - point1[0], point2[1] - point1[1]])

		if object1.collider.getCollisionCircleRadius() > 0 and object2.collider.getCollisionCircleRadius() > 0:
			radii = object1.collider.getCollisionCircleRadius() + object2.collider.getCollisionCircleRadius()
			distance = math.sqrt(positionDiff[0] ** 2 + positionDiff[1] ** 2)

			if distance > radii:
				return CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))

		obj1Points = object1.collider.getCollisionPoints()
		obj2Points = object2.collider.getCollisionPoints()

		minColDet = CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))

		# Axis of first object
		for i in range(0, len(obj1Points)):
			j = i + 1
			if j == len(obj1Points):
				j = 0

			lineVector = np.array([0.0, 0.0])
			
			lineVector[0] =  obj1Points[j][1] - obj1Points[i][1]
			lineVector[1] = -obj1Points[j][0] + obj1Points[i][0]

			cDet = collidesOnAxisPolyPoly(lineVector, obj1Points, obj2Points, positionDiff)

			if not cDet.collides:
				return cDet
			else:
				if (not minColDet.collides) or minColDet.collisionDistance > cDet.collisionDistance:
					minColDet = cDet

		# Axis of second object
		for i in range(0, len(obj2Points)):
			j = i + 1
			if j == len(obj2Points):
				j = 0

			lineVector = np.array([0.0, 0.0])
			
			lineVector[0] =  obj2Points[j][1] - obj2Points[i][1]
			lineVector[1] = -obj2Points[j][0] + obj2Points[i][0]

			cDet = collidesOnAxisPolyPoly(lineVector, obj1Points, obj2Points, positionDiff)
			if not cDet.collides:
				return cDet
			else:
				if (not minColDet.collides) or minColDet.collisionDistance > cDet.collisionDistance:
					minColDet = cDet

		return minColDet

	# Poly to Circle
	if (object1.shape == "circle" and object2.shape == "poly" or
		object1.shape == "poly" and object2.shape == "circle"):
		# If possible, we do a stage 1 collision detection, using radiuses
		point1 = object1.rigidBody.position
		point2 = object2.rigidBody.position

		positionDiff = np.array([point2[0] - point1[0], point2[1] - point1[1]])

		if object1.collider.getCollisionCircleRadius() > 0 and object2.collider.getCollisionCircleRadius() > 0:
			radii = object1.collider.getCollisionCircleRadius() + object2.collider.getCollisionCircleRadius()
			distance = math.sqrt(positionDiff[0] ** 2 + positionDiff[1] ** 2)

			if distance > radii:
				return CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))
			

		swapped = False
		# Swap them (if necessary) so object1 is always poly and object2 is circle
		if (object1.shape == "circle" and object2.shape == "poly"):
			obj1 = object2
			obj2 = object1
			swapped = True # Remember if it's swapped so we do the same in the collision details
		else:
			obj1 = object1
			obj2 = object2
		
		obj1Points = obj1.collider.getCollisionPoints()
		

		point1 = obj1.rigidBody.position
		point2 = obj2.rigidBody.position
		positionDiff = np.array([point2[0] - point1[0], point2[1] - point1[1]])

		minColDet = CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))
		minColDet.collisionDistance = 0
		minColDet.collides = False

		# axis of the first object (poly)
		closest = np.array([0.0, 0.0]) # + find closest point
		minDistance = float('inf')
		for i in range(0, len(obj1Points)):
			j = i + 1
			if j == len(obj1Points):
				j = 0

			lineVector = np.array([0.0, 0.0])

			lineVector[0] =  obj1Points[j][1] - obj1Points[i][1]
			lineVector[1] = -obj1Points[j][0] + obj1Points[i][0]

			cDet = collidesOnAxisPolyCircle(lineVector, obj1Points, obj2.collider.getCollisionCircleRadius(), positionDiff)
			if not cDet.collides:
				return cDet
			
			else:
				if not minColDet.collides or minColDet.collisionDistance > cDet.collisionDistance:
					minColDet = cDet

			# closest point
			distance = math.sqrt((obj1Points[i][0] - positionDiff[0]) ** 2 + (obj1Points[i][1] - positionDiff[1])** 2)
			if distance < minDistance:
				minDistance = distance
				closest = obj1Points[i]
		

		# axis of the second object (circle)
		lineVector = np.array([0.0, 0.0])
		lineVector[0] = closest[0] - positionDiff[0]
		lineVector[1] = closest[1] - positionDiff[1]

		cDet = collidesOnAxisPolyCircle(lineVector, obj1Points, obj2.collider.getCollisionCircleRadius(), positionDiff)
		if not cDet.collides:
			return cDet

		else:
			if not minColDet.collides or minColDet.collisionDistance > cDet.collisionDistance:
				minColDet = cDet

		if swapped:
			return minColDet.swappedObjects()

		return minColDet


	# Circle to Circle
	if object1.shape == "circle" and object2.shape == "circle":
		point1 = object1.rigidBody.position
		point2 = object2.rigidBody.position

		radii = object1.collider.getCollisionCircleRadius() + object2.collider.getCollisionCircleRadius()
		distance = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

		if (distance < radii):
			toReturn = CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))
			toReturn.collides = True
			toReturn.collisionDistance = radii - distance

			toReturn.collisionPointObject1[0] = (point2[0] - point1[0]) / distance * object1.collider.getCollisionCircleRadius()
			toReturn.collisionPointObject1[1] = (point2[1] - point1[1]) / distance * object1.collider.getCollisionCircleRadius()

			toReturn.collisionPointObject2[0] = (point1[0] - point2[0]) / distance * object2.collider.getCollisionCircleRadius()
			toReturn.collisionPointObject2[1] = (point1[1] - point2[1]) / distance * object2.collider.getCollisionCircleRadius()

			toReturn.reactionVectorObject1[0] = (point2[0] - point1[0]) - toReturn.collisionPointObject1[0] + toReturn.collisionPointObject2[0]
			toReturn.reactionVectorObject1[1] = (point2[1] - point1[1]) - toReturn.collisionPointObject1[1] + toReturn.collisionPointObject2[1]

			toReturn.reactionVectorObject2[0] = (point1[0] - point2[0]) - toReturn.collisionPointObject2[0] + toReturn.collisionPointObject1[0]
			toReturn.reactionVectorObject2[1] = (point1[1] - point2[1]) - toReturn.collisionPointObject2[1] + toReturn.collisionPointObject1[1]

			# print(distance)
			# temp = vars(toReturn)
			# for item in temp:
			# 	print(item, ':', temp[item])

			# print()

			return toReturn

		else:
			return CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))


	return CollisionDetails(False, 0, np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))
