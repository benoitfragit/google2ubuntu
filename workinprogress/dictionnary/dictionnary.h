#ifndef __DICTIONNARY_H__
#define __DICTIONNARY_H__
#include <glib.h>


typedef struct Dictionnary {
	GList	   *allwords;
	GHashTable *projections;
}Dictionnary;


Dictionnary* dictionnary_new(const gchar *path);

void dictionnary_display(const Dictionnary *dico);

void dictionnary_project(Dictionnary *dico, GHashTable *table);

void dictionnary_free(Dictionnary *dico);

gchar* dictionnary_process_request(const Dictionnary *dico, const gchar *input);

Dictionnary* dictionnary_new_from_file(const gchar *file);

void dictionnary_to_file(const Dictionnary *dico, const gchar *dicFile);

#endif
