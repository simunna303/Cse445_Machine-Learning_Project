# Cse445_Machine-Learning_Project

Background:
Within the past two decades, the number of resident space objects (RSOs - artificial objects that are in orbit around the Earth) has nearly doubled, from around 11000 objects in the year 2000 to around 19500 objects in 2019. This number is expected to rise even higher as more satellites are put into space, thanks to improvements in satellite technology and lower costs of production. On the other hand, the increase in the number of RSOs also indirectly increases the risk of collision between them. The important issue here is the reliable and accurate orbit tracking of satellites over sufficiently long periods of time.
Failure to address this issue has led to incidents such as the collision between the active US Iridium-33 communication satellite, and the inactive Russian Kosmos-2251 communication satellite in February 2009. More accidents will result in more debris being produced, and through a chain reaction of collisions (if left unchecked), may lead to a dire situation in which it becomes difficult or downright impossible to put a satellite into orbit due to the large accumulation of space debris surrounding the Earth. This scenario is known as the Kessler Syndrome. Thus, considering the gravity of the situation at hand, it is imperative to prevent such catastrophic collisions from ever happening again.

Context: 
The aim is to use machine learning or other forecasting algorithms to predict the positions and speeds of 600 satellites in orbit around the Earth. The original datasets were obtained from the International Data Analytics Olympiad 2020 (IDAO 2020) Competition, provided by the Russian Astronomical Science Centre.
Satellite positions and speeds (henceforth, they will be collectively referred to as the "kinematic states") can be measured using different methods, including simulations. In this dataset, there are two kinds of simulators: the precise simulator and the imprecise simulator. We refer to measurements made using the precise simulator as the "true" kinematic states of the satellite and measurements made using the imprecise simulator as the "simulated" kinematic states.

Variables Description: 
id (integer): unique row identifier
epoch (datetime): datetime (at the instant of measurement) in "%Y-%m-%d %H:%M:%S.%f" format (e.g. 2014-01-27 18:28:18.284)
sat_id (integer): unique satellite identifier, ranging from 0 to 599
x, y, z (float): the true position coordinates of a satellite (km)
Vx, Vy, Vz (float): the true speeds of a satellite, measured along the respective axes (km/s)
x_sim, y_sim, z_sim (float): the simulated position coordinates of a satellite (km)
Vx_sim, Vy_sim, Vz_sim (float): the simulated speeds of a satellite, measured along the respective axes (km/s)

Acknowledgements:
Original Owner of Datasets (IDAO 2020): https://idao.world/
License (Yandex Disk): https://yandex.com/legal/disk_termsofuse/
Database (where original data is stored): https://yadi.sk/d/0zYx00gSraxZ3w
