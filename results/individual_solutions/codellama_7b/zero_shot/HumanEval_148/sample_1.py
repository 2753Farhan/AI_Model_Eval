"""
AI Generated Solution
Task ID: HumanEval/148
Model: codellama:7b
Strategy: zero_shot
Sample ID: 1
Generated: 2026-01-11T00:13:26.331160
"""

def bf(planet1, planet2):
    planets = {"Mercury": 0, "Venus": 1, "Earth": 2, "Mars": 3, "Jupiter": 4, "Saturn": 5, "Uranus": 6, "Neptune": 7}
    if planet1 not in planets or planet2 not in planets:
        return ()
    else:
        sorted_planets = sorted(planets.keys(), key=lambda x: planets[x])
        index1 = sorted_planets.index(planet1)
        index2 = sorted_planets.index(planet2)
        return tuple(sorted_planets[index1+1:index2+1])