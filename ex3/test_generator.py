from displayEpisode import DisplayEpisode
from generator import Generator

g = Generator(random_state=42)

for _ in range(0, 5):
    track = g.generate_racetrack(size=50, n_edges=3, kernel_size=7)
    vis = DisplayEpisode()
    vis.displayEpisode(track, [])
