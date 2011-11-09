import json
import heatmap

file="data.json"

i = open(file,'rb')

points =[]
for tweet in i:
    js=json.loads(tweet)
    
    place=''
    try:
        place=js['coordinates']
    except KeyError:
        pass      
    try:        
        if place is None: place=js['geo']
    except KeyError:
        pass  
    try:    
        if place is None: place=js['place']
    except KeyError:
        pass
    
    if place is not None:   
        print place    
        if 'bounding_box' in place:
            if place['bounding_box'] is not None:
                for p in place['bounding_box']['coordinates']:
                    for point in p:
                        points.append(point)
                
        if 'coordinates' in place:
            points.append(place['coordinates'])
    


hm = heatmap.Heatmap()
hm.heatmap(points, "hm.png", dotsize=10)
hm.saveKML("geo.kml")

