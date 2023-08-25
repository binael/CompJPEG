#include "picture.h"

/**
 * main - entry point
 *
 * Return: 0 for ok or 1 or not
*/
int main()
{
	int i;
	char myList3[][20] = {"blue-sea.jpg", "cockroach.jpg", "fruits.jpg",
          "nature2.jpg", "blur-office.jpg", "coin.jpg",
          "landscape.jpg", "nature3.jpg", "blur-stain.jpg",
          "dental-implants.jpg", "leaf.jpg", "rat.jpg",
          "car-key.jpg", "example1.jpg", "mountain.jpeg",
          "cloud.jpg", "example_small.jpg", "nature1.jpg",
          "screenshot1.png", "screenshot2.png"};


	for (i = 0; i < 18; i++)
	{
		printf("%ld:\t", picture_size_int(myList3[i]));
		printf("%s:\t", picture_size_str(myList3[i]));
		printf("%s\n", picture_resolution(myList3[i]));
	}

	return (0);
}
