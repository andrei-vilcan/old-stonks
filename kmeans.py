import kmeans1d

x = [4.0, 4.1, 4.2, -50, 200.2, 200.4, 200.9, 80, 100, 102]
k = 4

clusters, centroids = kmeans1d.cluster(x, k)

print(clusters)
print(centroids)
