import folium

class MapService:
    def get_map(self):
        m = folium.Map(location=[55.75583, 37.61778], zoom_start=15)
        folium.Marker([55.783360, 37.564782], popup='<i>Шок-цена</i>').add_to(m)
        return m
