#include <cstdio>
int main() {
   int *a = new int[10000000];
   int i;
   for (i = 0; i < 10000000; i++)
      a[i] = i;
   printf("successfully Allocated and used\n");
   return 0;
}
