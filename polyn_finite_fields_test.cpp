#include <iostream>
#include <string>

#include "polyn_field.h"
#include "polyn_arithmetic.h"

using namespace std;

int main(int argc, char * argv[]){

    polyn::Polynomial p, p2, p4, p5;
    string pstring = "01110011010"; // 03 9a
    string p2string = "110000111010000"; // 61 d0 

    p = pstring; // 11

    p2 = p2string;  // 15 

    cout << endl << (string) (p2) << endl;
    cout << endl << (string) (p)  << endl;

    polyn::Polynomial p3 = p + p2;

    cout << endl << p3 << endl;

    // for (int i = 0; i < p3.numBits; i++) {
    //     cout << (char) (p3[i] + '0') << endl;
    // }


    p4 = "01101";
    p5 = "1101";

    cout << endl;
    cout << p4 * p5 << endl;


    return 0;
}