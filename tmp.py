import random
from pathlib import Path


# Output folder and number of half-step field positions to generate.
OUTPUT_DIR = Path(__file__).with_name("fields")
IMAGE_COUNT = 21


# Small SVG shape helpers used to build the field scenes.
def make_cloud(randomizer: random.Random, x: int, y: int) -> str:
	##Build one cloud from three overlapping circles at the given position.
	width = randomizer.randint(25, 48)
	return (
		f'<g fill="#ffffff" opacity="0.8"><circle cx="{x}" cy="{y}" '
		f'r="{width}"/><circle cx="{x + width}" cy="{y - 12}" '
		f'r="{width + 8}"/><circle cx="{x + width * 2}" cy="{y}" '
		f'r="{width}"/></g>'
	)


def make_tree(randomizer: random.Random, x: int, ground_y: int) -> str:
	##"""Build a tree with a randomized height and canopy color."""
	height = randomizer.randint(45, 100)
	canopy = randomizer.choice(["#4d8c5c", "#66a86d", "#7ebc73", "#548f6f"])
	return (
		f'<rect x="{x - 6}" y="{ground_y - height}" width="12" '
		f'height="{height}" fill="#7b563c" stroke="none"/>'
		f'<circle cx="{x}" cy="{ground_y - height}" r="{height * 0.38:.1f}" '
		f'fill="{canopy}" stroke="none"/>'
		f'<circle cx="{x - 18}" cy="{ground_y - height + 16}" '
		f'r="{height * 0.25:.1f}" fill="{canopy}" stroke="none"/>'
		f'<circle cx="{x + 19}" cy="{ground_y - height + 14}" '
		f'r="{height * 0.24:.1f}" fill="{canopy}" stroke="none"/>'
	)


def make_finder(x: int, y: int) -> str:
	##"""Build the striped finder figure and mark it for the game to locate."""
	return f'''<g id="finder" stroke="none">
  <ellipse cx="{x}" cy="{y + 58}" rx="26" ry="8" fill="#2d6b3d" opacity="0.30"/>
  <path d="M{x - 18} {y + 30} L{x - 24} {y + 62} L{x - 7} {y + 62} L{x - 3} {y + 42} L{x + 10} {y + 62} L{x + 26} {y + 62} L{x + 19} {y + 30}Z" fill="#2d4d82"/>
  <path d="M{x - 14} {y + 4} Q{x} {y - 12} {x + 14} {y + 4} L{x + 12} {y + 34} Q{x} {y + 46} {x - 12} {y + 34}Z" fill="#d94340"/>
  <path d="M{x - 12} {y + 10} Q{x} {y + 18} {x + 12} {y + 10} M{x - 12} {y + 18} Q{x} {y + 27} {x + 12} {y + 18} M{x - 11} {y + 28} Q{x} {y + 35} {x + 11} {y + 28}" fill="none" stroke="#f8f1e1" stroke-width="4.5" stroke-linecap="round"/>
  <circle cx="{x}" cy="{y - 14}" r="17" fill="#e8b692"/>
  <path d="M{x - 12} {y - 11} Q{x - 15} {y - 31} {x - 2} {y - 36} Q{x + 12} {y - 31} {x + 13} {y - 12}Z" fill="#2b2f35"/>
  <path d="M{x - 7} {y - 19} Q{x} {y - 15} {x + 7} {y - 19}" fill="none" stroke="#f7e7d9" stroke-width="3" stroke-linecap="round"/>
  <circle cx="{x - 5}" cy="{y - 14}" r="2.4" fill="#17191c"/>
  <circle cx="{x + 5}" cy="{y - 14}" r="2.4" fill="#17191c"/>
  <path d="M{x - 5} {y - 8} Q{x} {y - 4} {x + 5} {y - 8}" fill="none" stroke="#2a2a2a" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M{x - 11} {y + 35} L{x - 18} {y + 62} M{x + 11} {y + 35} L{x + 18} {y + 62}" stroke="#392c2a" stroke-width="6" stroke-linecap="round"/>
</g>'''


# Scene assembly: each call randomizes the landscape while keeping its field label.
def make_field_image(position_index: int, finder: bool, randomizer: random.Random) -> str:
	"""Create one SVG; position_index selects its label and finder selects the person."""
	sky = randomizer.choice(["#a9dff2", "#b8e4d0", "#c4ddf4", "#f4d8a8", "#c5e7ec"])
	far_grass = randomizer.choice(["#8fb66c", "#91bd76", "#82ad78", "#a2bd70"])
	near_grass = randomizer.choice(["#568b51", "#628f4b", "#4f8455", "#72964a"])
	clouds = "".join(
		make_cloud(randomizer, randomizer.randint(35, 650), randomizer.randint(55, 145))
		for _ in range(randomizer.randint(1, 4))
	)
	horizon = randomizer.randint(205, 260)
	far_hill = randomizer.randint(275, 320)
	trees = "".join(
		make_tree(randomizer, x, far_hill)
		for x in sorted(randomizer.sample(range(35, 765), randomizer.randint(3, 8)))
	)
	flowers = "".join(
		f'<circle cx="{randomizer.randint(12, 788)}" cy="{randomizer.randint(350, 490)}" r="{randomizer.randint(2, 5)}" fill="{randomizer.choice(["#f6dd77", "#f4f0df", "#e8a3a0"])}"/>'
		for _ in range(45)
	)
	person = make_finder(randomizer.randint(90, 710), randomizer.randint(345, 410)) if finder else ""
	position = position_index / 2

	# SVG layers are drawn from sky to hills, then trees, flowers, and the finder.
	return f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500">
  <rect width="800" height="500" fill="{sky}"/>
  <circle cx="{randomizer.randint(70, 730)}" cy="{randomizer.randint(48, 115)}" r="{randomizer.randint(25, 44)}" fill="#ffda76"/>
  {clouds}
  <path d="M0 {horizon} Q130 {horizon - 55} 265 {horizon} T530 {horizon - 10} T800 {horizon - 20} V340 H0Z" fill="{far_grass}"/>
  <rect y="{far_hill}" width="800" height="{500 - far_hill}" fill="{near_grass}"/>
  <path d="M0 390 Q170 340 340 395 T800 370 V500 H0Z" fill="#78a95b" opacity="0.78"/>
  {trees}
  {flowers}
  <text x="30" y="42" fill="#234332" font-family="sans-serif" font-size="22" font-weight="700">FIELD {position:.1f}</text>
  {person}
</svg>
'''


# Generate the image set and save the finder's index for the game.
def main() -> None:
	"""Write twenty randomized SVGs and record which one contains the finder."""
	OUTPUT_DIR.mkdir(exist_ok=True)
	randomizer = random.Random()
	finder_index = randomizer.randrange(IMAGE_COUNT)

	# Remove obsolete generated field images if the image count or spacing changed.
	expected_names = {
		f"field_{position_index / 2:.1f}".replace(".", "_") + ".svg"
		for position_index in range(IMAGE_COUNT)
	}
	for old_image in OUTPUT_DIR.glob("field_*.svg"):
		if old_image.name not in expected_names:
			old_image.unlink()

	# Each index is a position from 0.0 to 9.5 in 0.5 steps.
	for position_index in range(IMAGE_COUNT):
		position = position_index / 2
		filename_position = f"{position:.1f}".replace(".", "_")
		image_path = OUTPUT_DIR / f"field_{filename_position}.svg"
		image = make_field_image(position_index, position_index == finder_index, randomizer)
		image_path.write_text(image, encoding="utf-8")

	# The game reads this index to check the player's guess.
	(OUTPUT_DIR / "finder_position.txt").write_text(str(finder_index), encoding="utf-8")
	print(f"Created {IMAGE_COUNT} randomized field images in {OUTPUT_DIR}")


if __name__ == "__main__":
	main()
