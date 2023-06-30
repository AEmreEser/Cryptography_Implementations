#include <iostream>
#include <string>

#include "polyn_arithmetic.h"

using namespace std;

int main(int argc, char * argv[]){

    typedef pol::Polynomial polyn;

    polyn p("101");
    polyn p2("110100111");

    polyn p3 = p2 % p;

    cout << (string) (p3) << endl;
    

    return 0;
}