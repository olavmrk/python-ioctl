#include <stdio.h>

#include <linux/input.h>
#include <linux/fs.h>
#include <linux/random.h>

int main(void) {
  printf("{\n");
  printf("  'sizeof_int': %zu,\n", sizeof(int));
  printf("  'sizeof_ff_effect': %zu,\n", sizeof(struct ff_effect));
  printf("  'EVIOCSFF': 0x%08x,\n", EVIOCSFF);
  printf("  'BLKRRPART': 0x%08x,\n", BLKRRPART);
  printf("  'RNDGETENTCNT': 0x%08x,\n", RNDGETENTCNT);
  printf("  'RNDADDTOENTCNT': 0x%08x,\n", RNDADDTOENTCNT);
  printf("  'FIFREEZE': 0x%08x,\n", FIFREEZE);
  printf("}\n");
  return 0;
}
