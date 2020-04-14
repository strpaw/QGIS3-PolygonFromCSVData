import csv


def print_polygon(polygon_id, vertices):
    """ Prints polygon id and vertices (coordinate pairs)
    :param polygon_id: str,
    :param vertices: list of tuples (lon, lat)
    """
    if polygon_id is not None and len(vertices) < 3:
        # Need ad least 3 vertices to create polygon, print error message
        print('Polygon ident {} has less than 3 vertices'.format(polygon_id))
    else:
        # Print polygon vertices
        if polygon_id is not None:
            print(polygon_id, vertices)


def gen_polygon_from_csv(input_file):
    """ Generate polygons from CSV data file.
    :param input_file: str: file name (full path) to csv file.
    :return:
    """

    curr_poly_id = None  # Current polygon ident which is created, column POL_ID
    vertices_list = []  # List of vertices for current polygon

    with open(input_file, 'r') as data_file:
        reader = csv.DictReader(data_file, delimiter=';')
        while True:
            try:
                # Read data from csv row. Note: CSV fields POL_ID,LON,LAT
                row = next(reader)
                fetched_poly_id = row['POL_ID']  # Polygon ID read from CSV file
                vertex = (row['LON'], row['LAT'])

                if curr_poly_id == fetched_poly_id:  # Continue current polygon
                    vertices_list.append(vertex)
                else:
                    print_polygon(curr_poly_id, vertices_list)
                    # Fetched polygon id becomes current polygon id
                    curr_poly_id = fetched_poly_id
                    vertices_list.clear()  # Reset vertices list
                    vertices_list.append(vertex)  # Add fetched longitude and latitude

            except StopIteration:  # Reached end of file, try to create polygon from fetched data
                print_polygon(curr_poly_id, vertices_list)
                break
