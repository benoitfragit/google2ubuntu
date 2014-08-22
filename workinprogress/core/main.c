#include "core.h"
#include "processor.h"

int main(int argc, char **argv)
{
	Dictionnary *dico = dictionnary_new("test.txt");
	TaskManager *manager = task_manager_new(4);
	//dictionnary_display(dico);	
	//dictionnary_clustering(dico, 4, 300);	
	
	
	gchar* s = dictionnary_process_request(dico, "quelle heure", FALSE);

	task_manager_add_new(manager, s);
		
	dictionnary_free(dico);
	

	return 0;
}
