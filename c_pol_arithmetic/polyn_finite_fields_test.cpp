#include <iostream>
#include <string>

#include "polyn_arithmetic.h"

using namespace std;

int main(int argc, char * argv[]){

    typedef pol::Polynomial polyn;

    polyn p("10110");
    polyn p2("1011111");

    polyn p3 = p * p2;

    cout << (string) (p3) << endl;
    

    return 0;
}