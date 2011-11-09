import json
import heatmap
import networkx as net
import matplotlib.pyplot as plot

def trim_degrees(g, degree=1):
    """
    Trim the graph by removing nodes with degree less then value of the degree parameter
    Returns a copy of the graph, so it's non-destructive.
    """
    g2=g.copy()
    d=net.degree(g2)
    for n in g2.nodes():
        if d[n]<=degree: g2.remove_node(n)
    return g2

def sorted_degree(g):
    d=net.degree(g)
    ds = sorted(d.iteritems(), key=lambda (k,v): (-v,k))
    return ds

def add_or_inc_edge(g,f,t):
    """
    Adds an edge to the graph IF the edge does not exist already. 
    If it does exist, increment the edge weight.
    Used for quick-and-dirty calculation of projected graphs from 2-mode networks.
    """
    if g.has_edge(f,t):
        g[f][t]['weight']+=1
    else:
        g.add_edge(f,t,weight=1)

file="data.json"
i = open(file,'rb')

retweets=net.DiGraph()
hashtag_net=net.Graph()

for tweet in i:
    js=json.loads(tweet)
    
    ### process tweet to extract information
    try:
        author=js['user']['screen_name']
        entities=js['entities']
        mentions=entities['user_mentions']
        hashtags=entities['hashtags']
    
        for rt in mentions:
            alter=rt['screen_name']
            retweets.add_edge(author,alter)
        
        tags=[str.lower(tag['text']) for tag in hashtags]
        for t1 in tags:
            for t2 in tags:
                if t1 is not t2:
                    add_or_inc_edge(hashtag_net,t1,t2)      
    except KeyError:
        print ':-('
        continue
    
    
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

points =[]
