#ifndef __CORE_H__
#define __CORE_H__
#include <glib.h>
#include "kmeans.h"


typedef struct Dictionnary {
	GList	   *allwords;
	GHashTable *projections;
	kmeanCluster *kmeans;
}Dictionnary;

typedef struct Word {
	gint 	occurence;
	gchar  *w;
}Word; 

Dictionnary* dictionnary_new(const gchar *path);

void dictionnary_display(Dictionnary *dico);

void dictionnary_project(Dictionnary *dico, GHashTable *table);

void dictionnary_free(Dictionnary *dico);

gchar* dictionnary_process_request(Dictionnary *dico, gchar *input, gboolean use_clusters);

void dictionnary_clustering(Dictionnary *dico, gint num_class, gint max_iters);
#endif
