from factory.dataFactory import DataFactory
from utils import Utils

def main():
    data_factory = DataFactory()
    utilities = Utils()
    points = data_factory.generate_terrain(num_points=40, size_map=(50,50), num_clusters=3)
    print("==== PLOTTING POINTS ====")
    utilities.show_points_on_map(points)
    # for point in points:
    #     print(point.x, point.y, point.terrain_type)




if __name__ == "__main__":
    main()
