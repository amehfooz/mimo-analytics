import matplotlib.pyplot as plt

color_options = [
    "#ff0000", "#00ff00", "#0000ff", "#4a0055", "#552200", "#9999ff", "#ffff00", 
    "#ff00ff", "#10333a", "#ff9900", "#ff0099", "#00ff99", "#0099ff", "#99ff00",
    "#9900ff", "#990000", "#009900", "#000099", "#555555", "#ff9999", "#114400"
]

width = 0.9
height = 10
index = 0

for c in color_options:
	plt.bar(index, height, width, color=c)
	index += 1
plt.show()