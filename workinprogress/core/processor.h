#ifndef __PROCESSOR_H__
#define __PROCESSOR_H__
#include <glib.h>


typedef struct TaskManager {
	GThreadPool *pool;
	gint max_threads;
}TaskManager;

TaskManager* task_manager_new(gint num_thread);
void task_manager_add_new(TaskManager* manager, gchar *new_command);

#endif
