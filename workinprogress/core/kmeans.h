#ifndef __KMEAN_H__
#define __KMEAN_H__
#include <glib.h>

typedef struct kmeanCluster 
{
	GHashTable 	*projections;
	gdouble 	*centers;
	
	gint 		*etiq;
	gint 		max_iters;
	gint 		num_vectors;
	gint 		size_vectors;
	gint 		num_class;
}kmeanCluster;

kmeanCluster* kmean_cluster_new(gint max_iters, gint num_vectors, gint size_vectors, gint num_class);

void kmean_cluster_process(kmeanCluster *kmc, GList *vectors, GList* command);

gchar* kmean_cluster_process_request(kmeanCluster *kmc, gdouble* tab);

void kmean_cluster_display(kmeanCluster *kmc);
#endif
