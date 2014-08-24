#include "processor.h"

void task_manager_process(gpointer data, gpointer user_data)
{
	gchar* c = (gchar *)data;
	
	system(c);
	
	g_free(c);
}

TaskManager* task_manager_new(gint num_thread)
{
	TaskManager* tm 		= (TaskManager *)g_malloc0(sizeof(TaskManager));
	
	tm->max_threads 	  	= num_thread;
	tm->pool 				= g_thread_pool_new(task_manager_process, NULL, num_thread, TRUE, NULL); 
	
	return tm;
}

void task_manager_add_new(TaskManager* manager, gchar *new_command)
{
	g_return_if_fail(manager 		!= NULL);
	g_return_if_fail(new_command 	!= NULL);
		
	g_thread_pool_push(manager->pool, g_strdup(new_command), NULL);
	g_print("Launching new command: %s\n", new_command);
}
