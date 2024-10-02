#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

typedef unsigned char* pointer;

bool is64bit() {
    return true; // 64bit 
}

bool isBigEndian() {
    unsigned int x = 1;
    return *((unsigned char*)&x) == 0;
}

void le_show_bytes(unsigned int a) {
    for (int i = 0; i < sizeof(unsigned int); i++) {
        printf("%02X", (a >> (8 * i)) & 0xFF);
    }
}

void be_show_bytes(unsigned int a) {
    for (int i = sizeof(unsigned int) - 1; i >= 0; i--) {
        printf("%02X", (a >> (8 * i)) & 0xFF);
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage: ./a.out number\n");
        exit(0);
    }
    
    unsigned int a = atoi(argv[1]);

    printf("ARCH=%d\n", is64bit() ? 64 : 32);
    printf("ORDERING=%s\n", isBigEndian() ? "BIG_ENDIAN" : "LITTLE_ENDIAN");

    // Print MYANS
    printf("MYANS: DEC=%d HEX=", a);
    le_show_bytes(a);
    printf("\n");

    // Print CHECK with padded hex output
    printf("CHECK: DEC=%d HEX=%08X\n", a, a);
    return 0;
}
