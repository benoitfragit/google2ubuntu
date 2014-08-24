#include "dictionnary.h"
#include "processor.h"

int main(int argc, char **argv)
{
	Dictionnary *dico = dictionnary_new("test.txt");
	TaskManager *manager = task_manager_new(4);
	dictionnary_display(dico);

	dictionnary_to_file(dico, "dico.dic");

	gchar* s = dictionnary_process_request(dico, "sur internet");

	task_manager_add_new(manager, s);

	dictionnary_free(dico);

	
	return 0;
}
