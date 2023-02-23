from displayEpisode import DisplayEpisode
from generator import Generator

g = Generator(random_state=42)

tracks = []
for _ in range(0, 5):
    track = g.generate_racetrack_safely(size=50, n_edges=2, kernel_size=7)
    tracks.append(track)

for i, track in enumerate(tracks):
    vis = DisplayEpisode()
    vis.displayEpisode(track, [])
