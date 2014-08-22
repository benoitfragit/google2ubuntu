#include "kmeans.h"
#include <math.h>
#include <string.h>

static gboolean kmean_cluster_idx_is_valid(gint *idx, gint i)
{
	gint j;

	for(j = 0; j < i; ++j)
	{
		if(idx[j] == idx[i])
			return FALSE;
	}
	
	return TRUE;
}

static void kmean_cluster_init_idx(gint N, gint start, gint end, gint *idx)
{
	gint i;
	GRand* rng = g_rand_new();
	
	for(i = 0; i < N; ++i)
	{
		do
		{
			idx[i] = g_rand_int_range(rng, start, end);
		}while( kmean_cluster_idx_is_valid(idx, i) == FALSE && i >= 1 );	
	}
}


static gdouble kmean_cluster_distance(gint row, gint size, gdouble *centers, gdouble *w)
{
	gdouble res = 0.0f;
	gint i;
	
	for(i = 0; i < size; i++) res += pow(centers[ row*size + i] - w[i], 2);
	
	return res;
}

static void kmean_cluster_center_null(gpointer data, gpointer user_data)
{
	g_free((gdouble *)data);
}

void kmean_cluster_process(kmeanCluster *kmc, GList *vectors, GList* commands)
{
	gint i,j, k;
	gint iter = 0;
	gdouble *v;
	//les indices des centres initiaux
	gint *idx = (gint *)g_malloc0(kmc->num_class*sizeof(gint));
	
	
	//trouve les idx des centres initiaux
	kmean_cluster_init_idx(kmc->num_class, 0, kmc->num_vectors-1, idx);
	
	//initialiser les centres
	for(i=0; i < kmc->num_class; i++)
	{
		v = (gdouble *)g_list_nth_data(vectors, idx[i]);
		
		for(j=0; j < kmc->size_vectors; j++) kmc->centers[ i*kmc->size_vectors + j ] += v[j]/(gdouble)kmc->num_class;	
		
		idx[i] = 0;
	}
	
	
	do
	{
		//pour tous les vecteurs, on cherche le 
		for(i = 0; i < kmc->num_vectors; i++)
		{
			v = (gdouble *)g_list_nth_data(vectors, i);
			
			gdouble min_dist = kmean_cluster_distance(0, kmc->size_vectors, kmc->centers, v);
			gdouble dist;
			
			kmc->etiq[i] = 0;				
			
			for( j = 1; j < kmc->num_class; j++)
			{				
				dist = kmean_cluster_distance(j, kmc->size_vectors, kmc->centers, v);
				 
				if(dist < min_dist)
				{
					min_dist = dist;
					
					kmc->etiq[i] = j;
				}
			}
			
			idx[kmc->etiq[i]]++;
		}
		
		memset(kmc->centers, 0.0f, kmc->size_vectors*kmc->num_class*sizeof(gdouble));
		
		for(i=0;i<kmc->num_vectors; i++)
		{
			v = (gdouble *)g_list_nth_data(vectors, i);
			
			for(j=0;j<kmc->size_vectors; j++)
			{
				kmc->centers[kmc->etiq[i]*kmc->size_vectors+j] += v[j]/(gdouble)idx[kmc->etiq[i]];
			}
		}
		
		iter ++;	
	}while(iter < kmc->max_iters);
	
	//project the vectors
	for(i = 0; i < kmc->num_vectors; i++)
	{
		gchar *cmd  = (gchar *)g_list_nth_data(commands, i);
		gdouble *pj = (gdouble *)g_malloc0(kmc->num_class*sizeof(gdouble));
		v			= (gdouble *)g_list_nth_data(vectors, i);
		
		for(j = 0; j < kmc->num_class; j++)
		{
			for (k = 0; k < kmc->size_vectors; k++)
			{
				pj[j] += v[k] * kmc->centers[j*kmc->size_vectors+k];
			}
		}

		g_hash_table_insert(kmc->projections, g_strdup(cmd), pj);
	}	
}

kmeanCluster* kmean_cluster_new(gint max_iters, gint num_vectors, gint size_vectors, gint num_class)
{
	kmeanCluster *kmc 	= (kmeanCluster *)g_malloc0(sizeof(kmeanCluster));
	
	kmc->centers		= (gdouble *)g_malloc0(num_class*size_vectors*sizeof(gdouble));
	kmc->projections	= g_hash_table_new(g_str_hash, g_str_equal); 
	kmc->etiq			= (gint *)g_malloc0(num_vectors*sizeof(gint));
	
	kmc->max_iters		= max_iters;
	kmc->num_vectors	= num_vectors;
	kmc->size_vectors	= size_vectors;
	kmc->num_class		= num_class;
		
	return kmc;
}

gchar* kmean_cluster_process_request(kmeanCluster *kmc, gdouble* tab)
{
	gint i, j, idx;
	GList* keys = g_hash_table_get_keys(kmc->projections);
	GList* values = g_hash_table_get_values(kmc->projections);
	gdouble *t = (gdouble *)g_malloc0(kmc->num_class*sizeof(gdouble));
	gdouble p, minp;
	gchar *res = NULL;
	
	//get the projection
	for(i = 0; i < kmc->num_class; i++ )
	{
		for(j = 0;  j < kmc->size_vectors; j++) t[i] += kmc->centers[i*kmc->size_vectors + j] * tab[j];
		g_print(" %.10f", t[i]);
	}
	
	//find the nearest projections
	for(i = 0; i < kmc->num_vectors; i++)
	{
		p = 0;
		gdouble *tt = (gdouble *)g_list_nth_data(values, i);
		
		for(j = 0; j < kmc->num_class; j++)
			p += pow(tt[j] - t[j], 2);
	
		if( i == 0 || minp > p)
		{
			minp = p;
			idx = i;
		}		
	}

	res = g_strdup(g_list_nth_data(keys, idx));
		
	return res;	
}

void kmean_cluster_display(kmeanCluster *kmc)
{
	GList* keys = g_hash_table_get_keys(kmc->projections);
	GList* values = g_hash_table_get_values(kmc->projections);
	gint i, j;
			
	for(i = 0; i < kmc->num_vectors; i++)
	{
		g_print("%d %s:\t", kmc->etiq[i], (gchar *)g_list_nth_data(keys, i));
		gdouble *tab = (gdouble *)g_list_nth_data(values, i);
		
		for(j=0; j< kmc->num_class; j++) g_print(" %.10f", tab[j]);
		
		g_print("\n");
	}	
	
	g_list_free(keys);
	g_list_free(values);
}
