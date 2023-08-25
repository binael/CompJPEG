#include "picture.h"

/**
 * picture_size_int - function that determines the size of picture
 * @image_file: the image file path
 *
 * Return: image size or -1 if failure
*/
long int picture_size_int(char *image_file)
{
	FILE *image;
	long int size;

	image = fopen(image_file, "rb");
	if (image == NULL)
	{
		return (-1);
	}
	fseek(image, 0, SEEK_END); /*Set read pointer to last position*/
	size = ftell(image); /* Get the position value of the pointer*/

	fclose(image);

	return (size);
}


/**
 * picture_resolution - function that determines the resolution of a picture
 * @image_file: the image file path
 *
 * Return: the resolution in string format or null if failure
*/
char *picture_resolution(char *image_file)
{
	FILE *image;
	unsigned char *buff;
	Endian2Int width, height;
	long int im_size, i, position, count = 0;

	char *img_resolution = NULL;

	im_size = picture_size_int(image_file);
	image = fopen(image_file, "rb");
	buff = malloc(sizeof(unsigned char) * (im_size + 1));

	if (image == NULL || buff == NULL || im_size == -1)
	{
		return (NULL);
	}

	fread(buff, 1, im_size, image);

	for (i = 0; i < (im_size - 2); i++)
	{
		if (buff[i] == 0xFF &&
		(buff[i + 1] == 0xC0 || buff[i + 1] == 0xC2 || buff[i + 1] == 0xC1))
		{
			position = i;
			count++;
		}
	}
	height.byte[0] = buff[position + 8];
	height.byte[1] = buff[position + 7];
	width.byte[0] = buff[position + 6];
	width.byte[1] = buff[position + 5];

	img_resolution = res_to_string(height.num, width.num);

	free(buff);
	fclose(image);

	return (img_resolution);
}


/**
 * res_to_string - Converts the width and height resolution to
 * string in the for ('H X W')
 * @height: the height of the image file
 * @width: the width of the image file
 *
 * Return: Resolution in string ('H X W') or NULL
*/
char *res_to_string(short int height, short int width)
{
	char *res_in_string;
	char dimension[6];

	res_in_string = malloc(sizeof(char) * PIXSIZE);
	if (res_in_string == NULL)
	{
		return (NULL);
	}

	sprintf(dimension, "%d", height);
	strcpy(res_in_string, dimension);
	strcat(res_in_string, " X ");
	sprintf(dimension, "%d", width);
	strcat(res_in_string, dimension);

	return (res_in_string);
}


/**
 * picture_size_str - the string version of picture_size_int
 * @image_file: the image path of the file
 *
 * Return: NULL if failure or ([num]B, [num]KB, [num]MB)
*/
char *picture_size_str(char *image_file)
{
	char *size_in_str, buff[PIXSIZE];
	long int im_size, remainder;
	int index = 0, n = 0;
	char identifier[][3] = {"B", "KB", "MB", "GB"};
	long int one_thousand = 1000;

	im_size = picture_size_int(image_file);
	size_in_str = malloc(sizeof(char) * PIXSIZE);

	if (size_in_str == NULL || im_size == -1)
		return (NULL);

	while (im_size > (one_thousand - 1))
	{
		remainder = im_size % one_thousand;
		im_size = im_size / one_thousand;
		index++;
	}
	sprintf(buff, "%lu", im_size);
	strcpy(size_in_str, buff);

	if (im_size < 10 && index >= 1)
		n = 2;
	else if (im_size < 100 && index >= 1)
		n = 1;

	if (n >= 1)
		strcat(size_in_str, ".");

	sprintf(buff, "%lu", remainder);
	strncat(size_in_str, buff, n);
	strcat(size_in_str, identifier[index]);

	return (size_in_str);
}
