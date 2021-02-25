


#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int test_point(bool* in){
    if (*in == true){
        *in = false;
        return 1;
    } else {
        return 2;
    }
}


int main(int argc, char const *argv[]){
    bool h = true;
    bool* hello  = &h;
    int output = test_point(hello);
    printf("%d", output);   
    output = test_point(hello);
    printf("%d", output);   
}