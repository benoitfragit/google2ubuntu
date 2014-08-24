#include "core.h"
#include "processor.h"

int main(int argc, char **argv)
{
	/*Dictionnary *dico = dictionnary_new("test.txt");
	TaskManager *manager = task_manager_new(4);
	//dictionnary_display(dico);

	dictionnary_to_file(dico, "/home/benoit/Bureau/tt.ini");

	gchar* s = dictionnary_process_request(dico, "mes message");



	task_manager_add_new(manager, s);
	*/
	Dictionnary* dico = dictionnary_new_from_file( "/home/benoit/Bureau/tt.ini");
	dictionnary_display(dico);

	dictionnary_free(dico);

	
	return 0;
}
