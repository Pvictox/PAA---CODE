from factory.data_factory import DataFactory
from utils import Utils
from model.radar_instance import RadarInstance
def main():
    factory = DataFactory()
    points = factory.generate_terrain(100, (100, 100), 9)
    radar_instance = RadarInstance(points, 15)

    points_radar = [10, 35, 60, 85]  # 4 radares

    print(radar_instance.get_covered_area(points_radar))


    #print("==== PLOTTING POINTS ====")
    #utilities.show_points_on_map(points)
    # for point in points:
    #     print(point.x, point.y, point.terrain_type)




if __name__ == "__main__":
    main()
