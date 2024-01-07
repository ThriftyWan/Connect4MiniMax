import matplotlib.pyplot as plt
from pathlib import Path

plot_folder = Path("./")

fig = plt.figure()
xpoints = [0, 1, 2]
ypoints_a = [970.6, 11821.6, 130753.6]
ypoints_b = [970.6, 3718.9, 11785.8]
plt.ylabel('Average Nodes Expanded')
plt.xlabel('Extra rows/columns')
plt.plot(xpoints, ypoints_a, color='#ff9933', marker='o', linestyle='dashed', label="3 Rows, 3+x Columns")
plt.plot(xpoints, ypoints_b, color='#009999', marker='o', linestyle='dotted', label="3+x Rows, 3 Columns")


plt.xticks(range(min(xpoints), max(xpoints) + 1, 1))

plt.legend(loc='upper left')
filename = plot_folder / "Columns vs Rows" ".pdf"
# uncomment the following to show the plot before saving it
# plt.show()
plt.savefig(filename)
plt.close(fig)
