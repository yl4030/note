#define _CRT_SECURE_NO_WARNINGS
#include<iostream>
#include "cJSON.h"
typedef struct DOC_type3_info_s
{
	int PcharsLx;
	int PcharsLy;
	int PcharsRx;
	int PcharsRy;
	char PcharsText[3];
	char PcharsText1[3];
	char PcharsText2[3];
	char PcharsText3[3];
	char PcharsText4[3];
	int Pcharsconf;

} DOC_type3_info_t;
char* json_get_value_string(cJSON *item, char *key)
{
	cJSON *json_value = cJSON_GetObjectItem(item, key);
	if (json_value == NULL)
	{
		return NULL;
	}
	return json_value->valuestring;
}

int json_get_value_num(cJSON *item, char *key)
{
	cJSON *json_value = cJSON_GetObjectItem(item, key);
	if (json_value == NULL)
	{
		return 0xFFFFFFFF;
	}
	return json_value->valueint;
}

char *read(const char * filename) {
	FILE * fp;
	long lSize;
	char * buffer;
	//char * result;
	size_t len = 0;
	if ((fp = fopen(filename, "rb")) == 0)
	{
		printf("Error:Open input.c file fail!\n");
		return 0;
	}
	else
	{
		fseek(fp, 0, SEEK_END);
		lSize = ftell(fp);
		fseek(fp, 0, SEEK_SET);
		buffer = (char *)malloc(sizeof(char)*lSize + 1);
		memset(buffer, 0, sizeof(char)*lSize + 1);
		len = fread(buffer, 1, lSize, fp);
		fclose(fp);
		return buffer;
	}
}

int parse_DOC(const char * buf)
{
	char write_buf[10240] = { 0 };

	cJSON *root = cJSON_Parse(buf);
	//	printf("%s",buf);
	if (root == NULL)
	{
		return -1;
	}
	

	cJSON *json_childs_array = cJSON_GetObjectItem(root, "childs");
	if (json_childs_array == NULL)
	{
		cJSON_Delete(root);
		return -1;
	}
	cJSON *item1 = cJSON_GetArrayItem(json_childs_array, 0);

	int number = json_get_value_num(item1, "NumChild");
	while (number != 0) 
	{
		json_childs_array = cJSON_GetObjectItem(item1, "childs");
		if (json_childs_array == NULL)
		{
			cJSON_Delete(root);
			return -1;
		}
		item1 = cJSON_GetArrayItem(json_childs_array, 0);
		number = json_get_value_num(item1, "NumChild");
	}
		int childs_size = cJSON_GetArraySize(json_childs_array);
		
		int fileNo = 0;
		for (int j = 0; j < childs_size; j++)
		{
			cJSON *item = cJSON_GetArrayItem(json_childs_array, j);


			if (item == NULL)
			{
				continue;
			}

			int size2 = cJSON_GetArraySize(item);
			if (size2 <= 0)
			{
				continue;
			}


			//获取行所在的位置
			int Left = json_get_value_num(item, "Left");
			int Right = json_get_value_num(item, "Right");
			int Top = json_get_value_num(item, "Top");
			int Bottom = json_get_value_num(item, "Bottom");
			char *Text = json_get_value_string(item, "Text");

			//行的坐标和字
			//printf("%d %d %d %d %s\n", Left, Right, Top, Bottom, Text);

			//每个字的坐标和text
			cJSON *json_childs2 = cJSON_GetObjectItem(item, "childs");
			//cJSON *json_key_value = cJSON_GetArrayItem(json_childs2, 0);
			//char *value = json_get_value_string(json_key_value, "PcharsText");

			///////////////////////////////////////////////////////////////////
			if (json_childs2 == NULL)
			{
				continue;
			}

			int child2_size = cJSON_GetArraySize(json_childs2);
			if (child2_size <= 0)
			{
				continue;
			}
			cJSON *pJsonData = cJSON_CreateArray();
			cJSON *roottemp = cJSON_CreateArray();

			for (int i = 0; i < child2_size; i++)
			{
				cJSON *json_key_value = cJSON_GetArrayItem(json_childs2, i);

				DOC_type3_info_t dti;
				memset(&dti, 0, sizeof(dti));
				int value_int = json_get_value_num(json_key_value, "PcharsLx");
				if (value_int != NULL)
				{
					dti.PcharsLx = value_int;
				}

				value_int = json_get_value_num(json_key_value, "PcharsLy");
				if (value_int != NULL)
				{
					dti.PcharsLy = value_int;
				}

				value_int = json_get_value_num(json_key_value, "PcharsRx");
				if (value_int != NULL)
				{
					dti.PcharsRx = value_int;
				}

				value_int = json_get_value_num(json_key_value, "PcharsRy");
				if (value_int != NULL)
				{
					dti.PcharsRy = value_int;
				}

				value_int = json_get_value_num(json_key_value, "Pcharsconf");
				if (value_int != NULL)
				{
					dti.Pcharsconf = value_int;
				}

				char *value = json_get_value_string(json_key_value, "PcharsText");
				if (value != NULL)
				{
					strcpy(dti.PcharsText, value);
				}

				value = json_get_value_string(json_key_value, "PcharsText1");
				if (value != NULL)
				{
					strcpy(dti.PcharsText1, value);
				}

				value = json_get_value_string(json_key_value, "PcharsText2");
				if (value != NULL)
				{
					strcpy(dti.PcharsText2, value);
				}

				value = json_get_value_string(json_key_value, "PcharsText3");
				if (value != NULL)
				{
					strcpy(dti.PcharsText3, value);
				}

				value = json_get_value_string(json_key_value, "PcharsText4");
				if (value != NULL)
				{
					strcpy(dti.PcharsText4, value);
				}

				//printf("%d %d %d %d %d %s %s %s %s %s \n", dti.PcharsLx, dti.PcharsLy, dti.PcharsRx, dti.PcharsRy, dti.Pcharsconf, dti.PcharsText, dti.PcharsText1, dti.PcharsText2, dti.PcharsText3, dti.PcharsText4);

				roottemp = cJSON_CreateObject();

				cJSON *int_arry = NULL;
				cJSON *array = NULL;

				cJSON_AddItemToObject(roottemp, "rect", int_arry = cJSON_CreateArray());
				cJSON_AddItemToArray(int_arry, cJSON_CreateNumber(dti.PcharsLx));
				cJSON_AddItemToArray(int_arry, cJSON_CreateNumber(dti.PcharsLy));
				cJSON_AddItemToArray(int_arry, cJSON_CreateNumber(dti.PcharsRx));
				cJSON_AddItemToArray(int_arry, cJSON_CreateNumber(dti.PcharsRy));
				cJSON_AddItemToArray(int_arry, cJSON_CreateNumber(dti.Pcharsconf));

				cJSON_AddItemToObject(roottemp, "text", array = cJSON_CreateArray());
				cJSON_AddItemToArray(array, cJSON_CreateString(dti.PcharsText));
				cJSON_AddItemToArray(array, cJSON_CreateString(dti.PcharsText1));
				cJSON_AddItemToArray(array, cJSON_CreateString(dti.PcharsText2));
				cJSON_AddItemToArray(array, cJSON_CreateString(dti.PcharsText3));
				cJSON_AddItemToArray(array, cJSON_CreateString(dti.PcharsText4));

				cJSON_AddItemToArray(pJsonData, roottemp);

			}
			cJSON *int_arry1 = NULL;
			cJSON *array1 = NULL;

			cJSON* lin_json = cJSON_CreateArray();
			cJSON* pJsonData1 = cJSON_CreateArray();

			lin_json = cJSON_CreateObject();

			cJSON_AddItemToObject(lin_json, "rect", int_arry1 = cJSON_CreateArray());
			cJSON_AddItemToArray(int_arry1, cJSON_CreateNumber(Left));
			cJSON_AddItemToArray(int_arry1, cJSON_CreateNumber(Right));
			cJSON_AddItemToArray(int_arry1, cJSON_CreateNumber(Left + Top));
			cJSON_AddItemToArray(int_arry1, cJSON_CreateNumber(Right + Bottom));

			cJSON_AddItemToObject(lin_json, "text", array1 = cJSON_CreateArray());
			cJSON_AddItemToArray(array1, cJSON_CreateString(Text));

			cJSON_AddItemToObject(lin_json, "childs", pJsonData);
			//cJSON_AddItemToArray(array, cJSON_CreateString(Text));

			char *buf = cJSON_Print(lin_json);
			/*cJSON_Delete(pJsonData);
			cJSON_Delete(pJsonData1);
			cJSON_Delete(lin_json);
			cJSON_Delete(roottemp);*/

			static char filename[512] = { 0 };
			memset(filename, 0, 10);
			sprintf(filename, "./%d.txt", fileNo);

			FILE *fp = fopen(filename, "w");
			fwrite(buf, 1, strlen(buf), fp);
			free(buf);
			fclose(fp);
			fileNo++;
		}

		cJSON_Delete(root);
		return 1;
	}
		
int main()
{
	char *add;
	char *result;
	add = "D:/MyData/Desktop/json/2.json";
	result = read(add);
	//printf("%s\n\n\n", result);
	int re = parse_DOC(result);
	if (re == -1)
	{
		printf("parse error!\n");
	}

	getchar();
	system("pause");
	return 0;
}