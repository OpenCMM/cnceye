from cnceye.edge import find
from tests.config import MYSQL_CONFIG

process_id = 1

measured_edges = find.find_edges(process_id, MYSQL_CONFIG)
model_id = 1
edge_data = find.get_edge_data(model_id, MYSQL_CONFIG)
update_list = find.identify_close_edge(edge_data, measured_edges)
find.add_measured_edge_coord(update_list, MYSQL_CONFIG)
