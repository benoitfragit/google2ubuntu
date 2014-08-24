#ifndef __CORE_H__
#define __CORE_H__
#include <glib.h>


typedef struct Dictionnary {
	GList	   *allwords;
	GHashTable *projections;
}Dictionnary;


Dictionnary* dictionnary_new(const gchar *path);

void dictionnary_display(Dictionnary *dico);

void dictionnary_project(Dictionnary *dico, GHashTable *table);

void dictionnary_free(Dictionnary *dico);

gchar* dictionnary_process_request(Dictionnary *dico, gchar *input);

Dictionnary* dictionnary_new_from_file(const gchar *file);

void dictionnary_to_file(Dictionnary *dico, gchar *dicFile);

#endif
