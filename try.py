import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os
import anuga
import anuga_tools.animate as animate

rc('animation', html='jshtml')

cwd = os.getcwd()
data_dir = cwd+'/data/york'

# Polygon defining broad area of interest
bounding_polygon = anuga.read_polygon(os.path.join(data_dir,'extent.csv'))

# Polygon defining particular area of interest
york_polygon = anuga.read_polygon(os.path.join(data_dir,'york_selection.csv'))

# Elevation Data
topography_file = os.path.join(data_dir,'se6051_dtm_1m.asc')

# Resolution for most of the mesh
base_resolution = 100.0  # m^2

# Resolution in particular area of interest
york_resolution = 50.0 # m^2

interior_regions = [[york_polygon, york_resolution]]

##

domain = anuga.create_domain_from_regions(
            bounding_polygon,
            boundary_tags={'bottom': [0],
                           'right':  [1],
                           'top':    [2],
                           'left':   [3]},
            maximum_triangle_area=base_resolution,
            interior_regions=interior_regions)

domain.set_name('york1') # Name of sww file
dplotter = animate.Domain_plotter(domain)
plt.triplot(dplotter.triang, linewidth = 0.4);
plt.show()

##

domain.set_quantity('elevation', filename=topography_file, location='centroids') # Use function for elevation
domain.set_quantity('friction', 0.01, location='centroids')                        # Constant friction
domain.set_quantity('stage', expression='elevation', location='centroids')         # Dry Bed

plt.tripcolor(dplotter.triang,
              facecolors = dplotter.elev,
              cmap='Greys_r')
plt.colorbar();
plt.title("Elevation");
plt.show()

##

Br = anuga.Reflective_boundary(domain)
Bt = anuga.Transmissive_boundary(domain)

domain.set_boundary({'bottom':   Br,
                     'right':    Bt, # outflow
                     'top':      Bt, # outflow
                     'left':     Br})

##

# Setup inlet flow
center = (460000, 451920)
radius = 10.0
region0 = anuga.Region(domain, center=center, radius=radius)
fixed_inflow = anuga.Inlet_operator(domain, region0 , Q=400)

##

for t in domain.evolve(yieldstep=20, duration=300):

    #dplotter.plot_depth_frame()
    dplotter.save_depth_frame()
    domain.print_timestepping_statistics()

# Read in the png files stored during the evolve loop
dplotter.make_depth_animation()

##

# Create a wrapper for contents of sww file
swwfile = 'york1.sww'
splotter = animate.SWW_plotter(swwfile)


# Plot Depth and Speed at the last time slice
plt.subplot(121)
splotter.triang.set_mask(None)
plt.tripcolor(splotter.triang,
              facecolors = splotter.depth[-1,:],
              cmap='viridis')

plt.title("Depth")


plt.subplot(122)
splotter.triang.set_mask(None)
plt.tripcolor(splotter.triang,
              facecolors = splotter.speed[-1,:],
              cmap='viridis')

plt.title("Speed");
plt.show()
##
"""
##

# Read in house polygons from data directory and retain those of area > 60 m^2

import glob
house_files = glob.glob(os.path.join(data_dir,'house*.csv'))

house_polygons = []
for hf in house_files:
  house_poly = anuga.read_polygon(hf)
  poly_area = anuga.polygon_area(house_poly)

  # Leave out some small houses
  if poly_area > 60:
    house_polygons.append(house_poly)

##

domain = anuga.create_domain_from_regions(
            bounding_polygon,
            boundary_tags={'bottom': [0],
                           'right':  [1],
                           'top':    [2],
                           'left':   [3]},
            maximum_triangle_area=base_resolution,
            interior_holes=house_polygons,
            interior_regions=interior_regions)


domain.set_name('york2') # Name of sww file
dplotter = animate.Domain_plotter(domain)
plt.triplot(dplotter.triang, linewidth = 0.4);
plt.show()

# Setup Initial Conditions
domain.set_quantity('elevation', filename=topography_file, location='centroids') # Use function for elevation
domain.set_quantity('friction', 0.01, location='centroids')                        # Constant friction
domain.set_quantity('stage', expression='elevation', location='centroids')         # Dry Bed

# Setup BC
Br = anuga.Reflective_boundary(domain)
Bt = anuga.Transmissive_boundary(domain)


# NOTE: We need to assign a BC to the interior boundary region.
domain.set_boundary({'bottom':   Br,
                     'right':    Bt, # outflow
                     'top':      Bt, # outflow
                     'left':     Br,
                     'interior': Br})

# Setup inlet flow
center = (382270.0, 6354285.0)
radius = 10.0
region0 = anuga.Region(domain, center=center, radius=radius)
fixed_inflow = anuga.Inlet_operator(domain, region0 , Q=19.7)


dplotter = animate.Domain_plotter(domain)
plt.triplot(dplotter.triang, linewidth = 0.4);

##

for t in domain.evolve(yieldstep=20, duration=300):

    #dplotter.plot_depth_frame()
    dplotter.save_depth_frame()

    domain.print_timestepping_statistics()


# Read in the png files stored during the evolve loop
dplotter.make_depth_animation()

##

# Create a wrapper for contents of sww file
swwfile2 = 'york2.sww'
splotter2 = animate.SWW_plotter(swwfile2)

plt.subplot(121)
splotter2.triang.set_mask(None)
plt.tripcolor(splotter2.triang,
              facecolors = splotter2.depth[-1,:],
              cmap='viridis')

plt.title("Depth")


plt.subplot(122)
splotter2.triang.set_mask(None)
plt.tripcolor(splotter2.triang,
              facecolors = splotter2.speed[-1,:],
              cmap='viridis')

plt.title("Speed");
plt.show()
"""
