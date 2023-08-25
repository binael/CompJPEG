#ifndef PICTURE_H
#define PICTURE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFSIZE 1024
#define PIXSIZE 16

/**
 * endian_to_int - A union to convert Endian (big) for short bytes to integer
 * @num: integer value of the endian
 * @byte: the endian
*/
typedef union endian_to_int {
	short num;
	unsigned char byte[2];
} Endian2Int;

long int picture_size_int(char *image_file);
char *picture_size_str(char *image_file);
char *picture_resolution(char *image_file);
char *res_to_string(short int height, short int width);

#endif /*End of Header*/
